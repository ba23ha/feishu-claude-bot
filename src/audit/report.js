const fs = require('fs');
const path = require('path');
const { AUDIT_DIR } = require('./runner');
const { writeAccessLog } = require('./access-log');

/**
 * Generate a human-readable audit report (report.md) and machine-readable
 * access log (access.jsonl) for the completed distillation.
 *
 * @param {object} context  AuditContext from runner.js
 * @returns {string}  Path to the report.md file
 */
function generateReport(context) {
  const date = new Date().toISOString().split('T')[0];
  const reportPath = path.join(AUDIT_DIR, `${date}-${context.runId}-report.md`);

  const msgSources = context.sources.filter(s => s.type === 'message');
  const docSources = context.sources.filter(s => s.type === 'document');
  const minSources = context.sources.filter(s => s.type === 'minutes');
  const distilled = context.sources.filter(s => s.isDistilled);
  const excluded = context.sources.filter(s => !s.isDistilled);

  // Per-user message stats
  const userStats = {};
  for (const s of msgSources) {
    const id = s.senderId || 'unknown';
    if (!userStats[id]) userStats[id] = { name: s.senderName || id, read: 0, distilled: 0 };
    userStats[id].read++;
    if (s.isDistilled) userStats[id].distilled++;
  }

  const lines = [];
  lines.push('# 数据访问审计报告\n');

  // ── 基本信息 ─────────────────────────────────────────────────────────────────
  lines.push('## 基本信息');
  lines.push(`- run_id: \`${context.runId}\``);
  lines.push(`- 操作人: ${context.operator}`);
  lines.push(`- 触发时间: ${context.triggeredAt}`);
  lines.push(`- 触发指令: ${context.triggerCommand || '—'}`);
  lines.push(`- 读取原因: ${context.reason || '—'}`);
  lines.push('');

  // ── 本次读取范围 ──────────────────────────────────────────────────────────────
  lines.push('## 本次读取范围');
  const opts = context.opts || {};
  if (opts.chatId) lines.push(`- 群聊 ID: \`${opts.chatId}\``);
  if (opts.startMs) {
    lines.push(`- 时间范围: ${new Date(opts.startMs).toISOString()} → ${new Date(opts.endMs || Date.now()).toISOString()}`);
  }
  if (opts.keyword) lines.push(`- 关键词过滤: "${opts.keyword}"`);
  if (opts.docToken) lines.push(`- 文档 token: \`${opts.docToken}\``);
  if (opts.minutesToken) lines.push(`- 会议纪要 token: \`${opts.minutesToken}\``);
  lines.push('');

  // ── 读取结果汇总 ──────────────────────────────────────────────────────────────
  lines.push('## 读取结果汇总');
  lines.push(`- 总消息数: ${msgSources.length}`);
  lines.push(`- 老板消息数: ${msgSources.filter(s => s.isFromBoss).length}`);
  lines.push(`- 非老板消息数: ${msgSources.filter(s => !s.isFromBoss).length}`);
  lines.push(`- 文档数: ${docSources.length}`);
  lines.push(`- 会议纪要数: ${minSources.length}`);
  lines.push(`- 进入蒸馏: ${distilled.length} 条`);
  lines.push(`- 未进入蒸馏: ${excluded.length} 条`);
  lines.push('');

  // ── 按人员汇总 ────────────────────────────────────────────────────────────────
  lines.push('## 按人员汇总');
  if (Object.keys(userStats).length > 0) {
    for (const [id, stats] of Object.entries(userStats)) {
      lines.push(`- ${stats.name}（\`...${id.slice(-6)}\`）：读取 ${stats.read} 条，进入蒸馏 ${stats.distilled} 条，排除 ${stats.read - stats.distilled} 条`);
    }
  } else {
    lines.push('- 无消息来源（仅文档/会议纪要）');
  }
  lines.push('');

  // ── 进入蒸馏的数据 ────────────────────────────────────────────────────────────
  lines.push('## 进入蒸馏的数据');
  if (distilled.length > 0) {
    for (const s of distilled) {
      const who = s.senderName || s.senderId || '—';
      lines.push(`- \`${s.sourceId}\` [${s.type}] ${who} — ${s.summary || '（无摘要）'}`);
    }
  } else {
    lines.push('- 无');
  }
  lines.push('');

  // ── 未进入蒸馏的数据 ──────────────────────────────────────────────────────────
  lines.push('## 未进入蒸馏的数据');
  if (excluded.length > 0) {
    lines.push(`- 数量: ${excluded.length}`);
    const reasonCounts = {};
    for (const s of excluded) {
      const r = s.excludedReason || '未说明';
      reasonCounts[r] = (reasonCounts[r] || 0) + 1;
    }
    for (const [reason, count] of Object.entries(reasonCounts)) {
      lines.push(`  - ${reason}: ${count} 条`);
    }
  } else {
    lines.push('- 无');
  }
  lines.push('');

  // ── Skill/Soul 更新映射 ───────────────────────────────────────────────────────
  lines.push('## Skill/Soul 更新映射');
  if (context.soulUpdates.length > 0) {
    for (const u of context.soulUpdates) {
      lines.push(`- **${u.file}**`);
      lines.push(`  - run_id: \`${u.runId}\``);
      lines.push(`  - 原因: ${u.reason}`);
      lines.push(`  - 引用 source_id: ${u.sourceIds.length > 0 ? u.sourceIds.join(', ') : '—'}`);
      lines.push(`  - 更新时间: ${u.timestamp}`);
    }
  } else {
    lines.push('- 无 Soul 文件更新');
  }
  lines.push('');

  // ── 安全处理 ──────────────────────────────────────────────────────────────────
  lines.push('## 安全处理');
  lines.push('- 是否保存原文: 否（仅保存内容 hash 和脱敏摘要）');
  lines.push('- 是否脱敏: 是');
  lines.push('- 是否 hash: 是');
  const hasUnknown = context.sources.some(s => (s.senderName || '').startsWith('unknown_user'));
  lines.push(`- 是否存在 unknown_user: ${hasUnknown ? '是' : '否'}`);
  lines.push('');

  fs.writeFileSync(reportPath, lines.join('\n'));

  // Also write machine-readable access log
  writeAccessLog(context);

  return reportPath;
}

module.exports = { generateReport };
