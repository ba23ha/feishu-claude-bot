const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { readMessages } = require('../feishu/messages');
const { readDoc } = require('../feishu/docs');
const { readMinutes } = require('../feishu/minutes');
const { resolveUsers } = require('../feishu/resolver');
const { generate } = require('../llm/client');
const { appendChangelog } = require('./changelog');
const { recordSourceAccess, recordSoulUpdate } = require('../audit/runner');

const SOUL_DIR = path.join(__dirname, '..', '..', 'boss-soul');

function hashContent(text) {
  return 'sha256:' + crypto.createHash('sha256').update(text || '').digest('hex').slice(0, 16);
}

/**
 * Run a distillation task with full audit trail.
 *
 * Flow:
 *  1. Fetch specified Feishu data — record every source in auditContext
 *  2. Ask LLM to extract relevant soul insights
 *  3. Append insights to boss-soul file (never replace, raw data discarded)
 *  4. Record soul update in auditContext
 *  5. Write changelog entry with run_id
 *  6. Return summary string
 *
 * @param {object} opts
 * @param {string}   opts.targetFile     Which boss-soul file to update (e.g. 'decision')
 * @param {string}   opts.reason         Why we're distilling (logged in changelog)
 * @param {string}   [opts.chatId]       Feishu group ID to read messages from
 * @param {number}   [opts.startMs]      Start of time range (ms)
 * @param {number}   [opts.endMs]        End of time range (ms, defaults to now)
 * @param {string}   [opts.keyword]      Keyword filter for messages
 * @param {string}   [opts.docToken]     Doc token to read
 * @param {string}   [opts.minutesToken] Minutes token to read
 * @param {string}   [opts.extraContext] Additional context to pass to LLM
 * @param {object}   auditContext        Required — from createAuditContext()
 * @returns {Promise<string>}  Summary of the update
 */
async function distill(opts, auditContext) {
  if (!auditContext) throw new Error('auditContext is required — call createAuditContext() first');

  const { targetFile, reason, chatId, startMs, endMs = Date.now(), keyword, docToken, minutesToken, extraContext } = opts;
  const bossOpenId = process.env.BOSS_OPEN_ID;

  const validFiles = ['identity', 'style', 'decision', 'communication', 'taboos', 'examples'];
  if (!validFiles.includes(targetFile)) throw new Error(`Invalid targetFile: ${targetFile}`);

  const rawParts = [];
  const allSourceIds = [];

  // ── 1. Fetch messages ────────────────────────────────────────────────────────
  if (chatId && startMs) {
    const msgs = await readMessages({ chatId, startMs, endMs, keyword, maxCount: 150 });

    // Resolve sender names for audit trail
    const senderIds = [...new Set(msgs.map(m => m.sender).filter(Boolean))];
    const names = await resolveUsers(senderIds);

    if (msgs.length === 0) {
      rawParts.push('（指定群聊在该时间范围内无匹配消息）');
    } else {
      rawParts.push(`## 群聊消息（${msgs.length} 条）\n\n`
        + msgs.map(m => {
          const label = m.sender === bossOpenId ? '【郑伟】' : `【成员_${(m.sender || 'unk').slice(-4)}】`;
          return `[${m.timestamp}] ${label} ${m.text}`;
        }).join('\n'));
    }

    for (const msg of msgs) {
      const sourceId = `msg_${msg.timestamp.replace(/[-:.TZ]/g, '').slice(0, 14)}_${(msg.sender || 'unk').slice(-6)}`;
      allSourceIds.push(sourceId);
      recordSourceAccess(auditContext, {
        sourceId,
        type: 'message',
        chatId,
        senderId: msg.sender,
        senderName: names[msg.sender] || null,
        createTime: msg.timestamp,
        isFromBoss: msg.sender === bossOpenId,
        contentHash: hashContent(msg.text),
        // Desensitised excerpt: trim to 50 chars, no raw PII
        summary: msg.text.slice(0, 50).replace(/\d{11}/g, '***').replace(/[一-龥]{2,4}\d+/g, '***'),
        isDistilled: true,
      });
    }
  }

  // ── 2. Fetch document ────────────────────────────────────────────────────────
  if (docToken) {
    const docContent = await readDoc(docToken);
    rawParts.push(`## 文档内容\n\n${docContent}`);
    const sourceId = `doc_${docToken.slice(-8)}`;
    allSourceIds.push(sourceId);
    recordSourceAccess(auditContext, {
      sourceId,
      type: 'document',
      contentHash: hashContent(docContent),
      summary: docContent.slice(0, 50),
      isDistilled: true,
    });
  }

  // ── 3. Fetch meeting minutes ─────────────────────────────────────────────────
  if (minutesToken) {
    const minutesContent = await readMinutes(minutesToken);
    rawParts.push(`## 会议纪要\n\n${minutesContent}`);
    const sourceId = `min_${minutesToken.slice(-8)}`;
    allSourceIds.push(sourceId);
    recordSourceAccess(auditContext, {
      sourceId,
      type: 'minutes',
      contentHash: hashContent(minutesContent),
      summary: minutesContent.slice(0, 50),
      isDistilled: true,
    });
  }

  if (extraContext) rawParts.push(`## 额外背景\n\n${extraContext}`);

  if (rawParts.length === 0) {
    throw new Error('No data source specified. Provide chatId+startMs, docToken, or minutesToken.');
  }

  // ── 4. Read existing soul file ───────────────────────────────────────────────
  const soulFilePath = path.join(SOUL_DIR, `${targetFile}.md`);
  const existingContent = fs.existsSync(soulFilePath) ? fs.readFileSync(soulFilePath, 'utf8') : '';

  // ── 5. LLM extraction (raw data is NOT persisted — only insights are saved) ──
  const systemPrompt = `你是一个帮助提炼老板风格和决策原则的助手。
你的任务是分析提供的飞书群聊历史，**只提炼标注为【郑伟】的发言**中与"${targetFile}"相关的具体洞察。
群里其他成员的发言（标注为【成员_xxxx】）仅用作理解上下文，不纳入提炼范围。

规则：
- 只分析【郑伟】标注的消息，不分析其他成员的消息
- 只提炼真实可观察到的内容，不编造
- 输出必须是具体的、可操作的描述，不能是空泛的总结
- 输出格式为纯 Markdown，可以补充到现有文件中
- 不要重复现有文件中已有的内容
- 不保留原始敏感信息，只保留抽象的风格/原则描述
- 如果【郑伟】的发言中没有与"${targetFile}"相关的信息，明确说"本次材料中未发现相关内容"`;

  const userMessage = `请从以下材料中提炼与"${targetFile}"相关的洞察：

${rawParts.join('\n\n---\n\n')}

---

现有 boss-soul/${targetFile}.md 内容（避免重复）：

${existingContent || '（文件为空）'}

请输出：
1. 提炼到的新洞察（Markdown 格式，直接可追加到现有文件）
2. 如果没有新内容，说明原因`;

  const distilledContent = await generate(systemPrompt, userMessage, { maxTokens: 1500 });

  // ── 6. Append to soul file (never replace; raw data already discarded above) ─
  const timestamp = new Date().toISOString();
  const appendBlock = `\n\n---\n\n<!-- 蒸馏更新 ${timestamp} | run_id: ${auditContext.runId} | 原因：${reason} -->\n\n${distilledContent}`;
  fs.writeFileSync(soulFilePath, existingContent + appendBlock);

  // ── 7. Record soul update in audit context ────────────────────────────────────
  recordSoulUpdate(auditContext, `boss-soul/${targetFile}.md`, allSourceIds);

  // ── 8. Changelog ─────────────────────────────────────────────────────────────
  appendChangelog({
    file: `boss-soul/${targetFile}.md`,
    reason,
    summary: distilledContent.slice(0, 100).replace(/\n/g, ' ') + '...',
    operator: auditContext.operator,
    runId: auditContext.runId,
  });

  return `✅ 蒸馏完成，已更新 boss-soul/${targetFile}.md\n\n原因：${reason}\n\n提炼内容预览：\n${distilledContent.slice(0, 400)}${distilledContent.length > 400 ? '\n...' : ''}`;
}

/**
 * Parse a distill command: /distill --file=decision --chat=xxx --days=90 --keyword=xxx --reason=xxx
 */
function parseDistillCommand(text) {
  const opts = { _command: text };

  const fileMatch = text.match(/--file[=\s]+(\w+)/);
  if (fileMatch) opts.targetFile = fileMatch[1];

  const chatMatch = text.match(/--chat[=\s]+(\S+)/);
  if (chatMatch) opts.chatId = chatMatch[1];

  const daysMatch = text.match(/--days[=\s]+(\d+)/);
  if (daysMatch) {
    const days = parseInt(daysMatch[1], 10);
    opts.startMs = Date.now() - days * 24 * 60 * 60 * 1000;
    opts.endMs = Date.now();
  }

  const keywordMatch = text.match(/--keyword[=\s]+"?([^"]+)"?/);
  if (keywordMatch) opts.keyword = keywordMatch[1].trim();

  const docMatch = text.match(/--doc[=\s]+(\S+)/);
  if (docMatch) opts.docToken = docMatch[1];

  const minutesMatch = text.match(/--minutes[=\s]+(\S+)/);
  if (minutesMatch) opts.minutesToken = minutesMatch[1];

  const reasonMatch = text.match(/--reason[=\s]+"?([^"]+)"?/);
  opts.reason = reasonMatch ? reasonMatch[1].trim() : '手动蒸馏触发';

  return opts;
}

module.exports = { distill, parseDistillCommand };
