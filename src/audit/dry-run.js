require('dotenv').config();
const https = require('https');
const { getValidToken, hasValidAuth } = require('../feishu/oauth');
const { resolveUsers } = require('../feishu/resolver');
const { generateRunId } = require('./runner');

function httpsGet(path, token) {
  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'open.feishu.cn',
      path,
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` },
    }, res => {
      let data = '';
      res.on('data', d => { data += d; });
      res.on('end', () => { try { resolve(JSON.parse(data)); } catch (e) { reject(e); } });
    });
    req.on('error', reject);
    req.end();
  });
}

/**
 * Scan message metadata (sender_id + timestamp only — no body content).
 * Used by dry-run to enumerate who is in scope without reading content.
 */
async function scanMessageSenders({ chatId, startMs, endMs, maxCount = 200 }) {
  if (!hasValidAuth()) throw new Error('No valid user token. Run: node cli-boss.js auth-url');
  const token = await getValidToken();
  const senderCounts = {};
  let total = 0;
  let pageToken;

  while (total < maxCount) {
    let qs = `container_id_type=chat&container_id=${chatId}&page_size=50&sort_type=ByCreateTimeDesc`;
    if (pageToken) qs += `&page_token=${encodeURIComponent(pageToken)}`;

    const res = await httpsGet(`/open-apis/im/v1/messages?${qs}`, token);
    if (res.code !== 0) throw new Error(`Feishu API error ${res.code}: ${res.msg}`);

    const items = res.data?.items || [];
    if (items.length === 0) break;

    let reachedOlder = false;
    for (const item of items) {
      const ts = parseInt(item.create_time, 10);
      if (ts < startMs) { reachedOlder = true; break; }
      if (ts > endMs) continue;

      const senderId = item.sender?.id || 'unknown';
      senderCounts[senderId] = (senderCounts[senderId] || 0) + 1;
      total++;
      if (total >= maxCount) break;
    }

    if (reachedOlder) break;
    pageToken = res.data?.page_token;
    if (!pageToken) break;
  }

  return { total, senderCounts };
}

/**
 * Preview what a distill command would access, without reading any content.
 * Returns a DryRunResult that can be shown to the boss for confirmation.
 *
 * @param {object} opts  Same opts as distill()
 * @returns {Promise<DryRunResult>}
 */
async function dryRun(opts) {
  const { chatId, startMs, endMs = Date.now(), keyword, docToken, minutesToken, targetFile, reason } = opts;
  const runId = generateRunId();
  const result = { runId, opts, chatPreview: null, docPreview: null, minutesPreview: null, riskFlags: [] };

  const bossOpenId = process.env.BOSS_OPEN_ID;

  if (!targetFile) result.riskFlags.push('未指定 --file，无法确认更新目标');

  if (chatId && startMs) {
    try {
      const { total, senderCounts } = await scanMessageSenders({ chatId, startMs, endMs });
      const openIds = Object.keys(senderCounts);
      const names = await resolveUsers(openIds);
      result.chatPreview = {
        chatId,
        estimatedMessages: total,
        senderCounts,
        senderNames: names,
        timeRange: {
          from: new Date(startMs).toISOString(),
          to: new Date(endMs).toISOString(),
        },
        keyword: keyword || null,
      };
      const unknownCount = openIds.filter(id => (names[id] || '').startsWith('unknown_user')).length;
      if (unknownCount > 0) result.riskFlags.push(`包含 ${unknownCount} 个无法解析姓名的用户`);
      if (total > 100) result.riskFlags.push(`消息量较大（${total} 条），请确认范围合理`);
      const nonBossCount = openIds
        .filter(id => id !== bossOpenId)
        .reduce((s, id) => s + (senderCounts[id] || 0), 0);
      if (nonBossCount > 0) result.riskFlags.push(`包含非老板用户数据（${nonBossCount} 条消息）`);
    } catch (err) {
      result.riskFlags.push(`无法预览群消息：${err.message}`);
    }
  }

  if (docToken) {
    result.docPreview = { docToken };
    result.riskFlags.push('文档正文需在正式读取阶段获取，dry-run 阶段仅记录 token');
  }

  if (minutesToken) {
    try {
      const client = getFeishuClient();
      const res = await client.minutes.minute.get({ path: { minute_token: minutesToken } });
      if (res.code === 0 && res.data?.minute) {
        const m = res.data.minute;
        result.minutesPreview = {
          minutesToken,
          topic: m.topic || '未命名会议',
          startTime: m.start_time
            ? new Date(parseInt(m.start_time, 10) * 1000).toISOString()
            : null,
        };
      } else {
        result.minutesPreview = { minutesToken };
      }
    } catch {
      result.minutesPreview = { minutesToken };
    }
  }

  if (!chatId && !docToken && !minutesToken) {
    result.riskFlags.push('未指定任何数据来源（--chat / --doc / --minutes）');
  }

  return result;
}

/**
 * Format a DryRunResult into a Feishu message string ready to send.
 * @param {object} result  Return value of dryRun()
 * @returns {string}
 */
function formatDryRunMessage(result) {
  const lines = [];
  lines.push('📋 蒸馏前访问清单');
  lines.push(`run_id: ${result.runId}`);
  lines.push(`目标文件: boss-soul/${result.opts.targetFile || '未指定'}.md`);
  lines.push(`原因: ${result.opts.reason || '未填写'}`);
  lines.push('');
  lines.push('本次计划访问范围：');

  if (result.chatPreview) {
    const cp = result.chatPreview;
    lines.push(`• 群聊: ${cp.chatId}`);
    lines.push(`• 时间范围: ${cp.timeRange.from.slice(0, 10)} → ${cp.timeRange.to.slice(0, 10)}`);
    if (cp.keyword) lines.push(`• 关键词过滤: "${cp.keyword}"`);
    lines.push(`• 预计消息数: ${cp.estimatedMessages} 条`);
    lines.push('• 涉及用户：');
    for (const [openId, count] of Object.entries(cp.senderCounts)) {
      const name = cp.senderNames[openId] || openId;
      lines.push(`  - ${name}（...${openId.slice(-6)}）：${count} 条`);
    }
  }

  if (result.docPreview) {
    lines.push(`• 文档 token: ${result.docPreview.docToken}`);
  }

  if (result.minutesPreview) {
    const mp = result.minutesPreview;
    lines.push(`• 会议纪要: ${mp.topic || mp.minutesToken}`);
    if (mp.startTime) lines.push(`  开始时间: ${mp.startTime.slice(0, 10)}`);
  }

  if (result.riskFlags.length > 0) {
    lines.push('');
    lines.push('⚠️ 风险提示：');
    result.riskFlags.forEach(f => lines.push(`• ${f}`));
  }

  lines.push('');
  lines.push('回复「确认」执行，或「取消」中止。（5 分钟内有效）');
  return lines.join('\n');
}

module.exports = { dryRun, formatDryRunMessage, scanMessageSenders };
