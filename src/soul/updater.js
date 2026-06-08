const fs = require('fs');
const path = require('path');
const { readMessages } = require('../feishu/messages');
const { readDoc } = require('../feishu/docs');
const { readMinutes } = require('../feishu/minutes');
const { generate } = require('../llm/client');
const { appendChangelog } = require('./changelog');

const SOUL_DIR = path.join(__dirname, '..', '..', 'boss-soul');

/**
 * Run a distillation task:
 * 1. Fetch specified Feishu data
 * 2. Ask LLM to extract relevant soul insights
 * 3. Update the target boss-soul file (APPEND, not replace)
 * 4. Log to changelog
 * 5. Return summary of what was added
 *
 * @param {object} opts
 * @param {string}   opts.targetFile    Which boss-soul file to update (e.g. 'decision')
 * @param {string}   opts.reason        Why we're distilling (logged in changelog)
 * @param {string}   [opts.chatId]      Feishu group ID to read messages from
 * @param {number}   [opts.startMs]     Start of time range (ms)
 * @param {number}   [opts.endMs]       End of time range (ms, defaults to now)
 * @param {string}   [opts.keyword]     Keyword filter for messages
 * @param {string}   [opts.docToken]    Doc token to read
 * @param {string}   [opts.minutesToken] Minutes token to read
 * @param {string}   [opts.extraContext] Additional context to pass to LLM
 * @returns {Promise<string>}  Summary of the update
 */
async function distill(opts) {
  const { targetFile, reason, chatId, startMs, endMs = Date.now(), keyword, docToken, minutesToken, extraContext } = opts;

  const validFiles = ['identity', 'style', 'decision', 'communication', 'taboos', 'examples'];
  if (!validFiles.includes(targetFile)) throw new Error(`Invalid targetFile: ${targetFile}`);

  // 1. Collect raw material
  const rawParts = [];

  if (chatId && startMs) {
    const msgs = await readMessages({ chatId, startMs, endMs, keyword, maxCount: 150 });
    if (msgs.length === 0) {
      rawParts.push('（指定群聊在该时间范围内无匹配消息）');
    } else {
      rawParts.push(`## 群聊消息（${msgs.length} 条）\n\n`
        + msgs.map(m => `[${m.timestamp}] ${m.text}`).join('\n'));
    }
  }

  if (docToken) {
    const docContent = await readDoc(docToken);
    rawParts.push(`## 文档内容\n\n${docContent}`);
  }

  if (minutesToken) {
    const minutesContent = await readMinutes(minutesToken);
    rawParts.push(`## 会议纪要\n\n${minutesContent}`);
  }

  if (extraContext) rawParts.push(`## 额外背景\n\n${extraContext}`);

  if (rawParts.length === 0) throw new Error('No data source specified. Provide chatId+startMs, docToken, or minutesToken.');

  // 2. Read existing soul file
  const soulFilePath = path.join(SOUL_DIR, `${targetFile}.md`);
  const existingContent = fs.existsSync(soulFilePath) ? fs.readFileSync(soulFilePath, 'utf8') : '';

  // 3. Ask LLM to extract insights (raw data is not persisted — only extracted insights are saved)
  const systemPrompt = `你是一个帮助提炼老板风格和决策原则的助手。
你的任务是分析提供的飞书历史数据，提炼出与"${targetFile}"相关的具体洞察。

规则：
- 只提炼真实可观察到的内容，不编造
- 输出必须是具体的、可操作的描述，不能是空泛的总结
- 输出格式为纯 Markdown，可以补充到现有文件中
- 不要重复现有文件中已有的内容
- 不保留原始敏感信息，只保留抽象的风格/原则描述
- 如果材料中没有与"${targetFile}"相关的信息，明确说"本次材料中未发现相关内容"`;

  const userMessage = `请从以下材料中提炼与"${targetFile}"相关的洞察：

${rawParts.join('\n\n---\n\n')}

---

现有 boss-soul/${targetFile}.md 内容（避免重复）：

${existingContent || '（文件为空）'}

请输出：
1. 提炼到的新洞察（Markdown 格式，直接可追加到现有文件）
2. 如果没有新内容，说明原因`;

  const distilledContent = await generate(systemPrompt, userMessage, { maxTokens: 1500 });

  // 4. Append to soul file (never replace — only add; raw data discarded)
  const timestamp = new Date().toISOString();
  const appendBlock = `\n\n---\n\n<!-- 蒸馏更新 ${timestamp} | 原因：${reason} -->\n\n${distilledContent}`;
  fs.writeFileSync(soulFilePath, existingContent + appendBlock);

  // 5. Update changelog
  appendChangelog({
    file: `boss-soul/${targetFile}.md`,
    reason,
    summary: distilledContent.slice(0, 100).replace(/\n/g, ' ') + '...',
    operator: 'distill-command',
  });

  return `✅ 蒸馏完成，已更新 boss-soul/${targetFile}.md\n\n原因：${reason}\n\n提炼内容预览：\n${distilledContent.slice(0, 400)}${distilledContent.length > 400 ? '\n...' : ''}`;
}

/**
 * Parse a distill command: /distill --file=decision --chat=xxx --days=90 --keyword=方案评审 --reason=xxx
 */
function parseDistillCommand(text) {
  const opts = {};

  const fileMatch = text.match(/--file[=\s]+(\w+)/);
  if (fileMatch) opts.targetFile = fileMatch[1];

  const chatMatch = text.match(/--chat[=\s]+(\S+)/);
  if (chatMatch) opts.chatId = chatMatch[1];

  const daysMatch = text.match(/--days[=\s]+(\d+)/);
  if (daysMatch) {
    const days = parseInt(daysMatch[1], 10);
    opts.startMs = Date.now() - days * 24 * 60 * 60 * 1000;
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
