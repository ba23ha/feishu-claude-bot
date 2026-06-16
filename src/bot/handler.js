const { buildSystemPrompt, loadSkill, loadMemory } = require('../soul/loader');
const { generate } = require('../llm/client');
const { resolveWikiNode, readDoc } = require('../feishu/docs');

/**
 * Extract the first valid JSON object from LLM output.
 * Tries markdown code block first, then depth-tracking brace scan.
 */
function extractJSON(text) {
  const codeBlock = text.match(/```(?:json)?\s*([\s\S]*?)```/);
  if (codeBlock) {
    try { return JSON.parse(codeBlock[1].trim()); } catch {}
  }
  let depth = 0, start = -1;
  for (let i = 0; i < text.length; i++) {
    if (text[i] === '{') { if (depth === 0) start = i; depth++; }
    else if (text[i] === '}') {
      depth--;
      if (depth === 0 && start !== -1) {
        try { return JSON.parse(text.slice(start, i + 1)); } catch {}
      }
    }
  }
  throw new Error('No valid JSON found in LLM output');
}

/**
 * Handle a task request from the boss.
 * @param {'reply'|'polish'|'review'|'review_inline'|'meeting'|'delegation'|'followup'|'general'} taskType
 * @param {string} userInput  Raw message from boss
 * @returns {Promise<string>}  The response to send back
 */
async function handleTask(taskType, userInput, opts = {}) {
  const systemPrompt = buildSystemPrompt(opts.roleContext);

  if (taskType === 'general') {
    return generate(systemPrompt, userInput);
  }

  // Note: 'distill' and 'review_inline' are handled in server.js — never reach here
  if (!['reply', 'polish', 'review', 'meeting', 'delegation', 'followup'].includes(taskType)) {
    throw new Error(`Unknown task type: ${taskType}`);
  }

  const skillContent = loadSkill(taskType);

  // Inject relevant memory for context-heavy tasks
  let memoryContext = '';
  if (['reply', 'review', 'delegation', 'followup'].includes(taskType)) {
    const projects = loadMemory('projects');
    const people = loadMemory('people-map');
    const glossary = loadMemory('glossary');
    const parts = [];
    if (projects) parts.push(`### 项目信息\n${projects}`);
    if (people) parts.push(`### 人员信息\n${people}`);
    if (glossary) parts.push(`### 术语表\n${glossary}`);
    if (parts.length > 0) memoryContext = `\n\n---\n\n## 背景记忆\n\n${parts.join('\n\n')}`;
  }

  const combinedSystem = `${systemPrompt}${memoryContext}\n\n---\n\n## 当前任务指令\n\n${skillContent}`;
  return generate(combinedSystem, userInput);
}

/**
 * Read a Feishu doc and generate inline comment suggestions.
 * Handles wiki→docx token resolution internally.
 *
 * @param {string} token    Raw token from URL (docx token or wiki token)
 * @param {string} urlType  'docx' | 'wiki'
 * @param {string} userInput Original boss message (for context)
 * @param {number} [maxComments=5]
 * @returns {Promise<{ preview: string, comments: object[], docToken: string }>}
 */
async function handleInlineReview(token, urlType, userInput, maxComments = 5, opts = {}) {
  let docToken = token;
  if (urlType === 'wiki') {
    const node = await resolveWikiNode(token);
    docToken = node.objToken;
  }

  const docContent = await readDoc(docToken);
  if (!docContent || docContent.trim().length < 50) {
    throw new Error('文档内容为空或过短，无法分析');
  }

  const systemPrompt = buildSystemPrompt(opts.roleContext);
  const skillContent = loadSkill('review_inline');
  const projects = loadMemory('projects');
  const glossary = loadMemory('glossary');

  const memoryParts = [];
  if (projects) memoryParts.push(`### 项目信息\n${projects}`);
  if (glossary) memoryParts.push(`### 术语表\n${glossary}`);
  const memoryContext = memoryParts.length > 0
    ? `\n\n---\n\n## 背景记忆\n\n${memoryParts.join('\n\n')}`
    : '';

  const combinedSystem = `${systemPrompt}${memoryContext}\n\n---\n\n## 当前任务指令\n\n${skillContent}`;

  const userPrompt = `review_mode: inline_comment
max_comments: ${maxComments}

文档内容：
${docContent.slice(0, 6000)}

请严格按 inline_comment JSON 输出格式输出，不要输出其他内容。`;

  let parsed;
  let lastErr;
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      const raw = await generate(combinedSystem, userPrompt);
      parsed = extractJSON(raw);
      break;
    } catch (e) {
      lastErr = e;
    }
  }
  if (!parsed) throw new Error(`LLM 输出解析失败: ${lastErr?.message}`);

  const comments = parsed.comments || [];
  const summary = parsed.summary || `识别到 ${comments.length} 个问题`;

  const lines = [`📋 文档批注预览\n${summary}\n`];
  comments.forEach((c, i) => {
    const sev = c.severity === 'high' ? '🔴' : c.severity === 'medium' ? '🟡' : '⚪';
    lines.push(`${i + 1}. ${sev} [${c.issue_type}]`);
    if (c.section_title) lines.push(`   章节：${c.section_title}`);
    const snippet = (c.selected_text || '').slice(0, 60);
    lines.push(`   划线：「${snippet}${snippet.length === 60 ? '…' : ''}」`);
    lines.push(`   评论：${c.comment_draft}`);
  });
  lines.push('\n回复「确认」写入文档，回复「取消」放弃。');

  return { preview: lines.join('\n'), comments, docToken };
}

/**
 * Handle ambiguous input — ask boss to clarify.
 * @returns {string}
 */
function handleClarification() {
  return `需要确认一下你的需求，请选择：

1️⃣ 代写回复 — 帮你生成一条飞书消息
2️⃣ 润色表达 — 优化你已写好的草稿
3️⃣ 方案点评 — 对一份方案/汇报给出意见
4️⃣ 会议纪要 — 提炼会议要点和 follow-up

请直接发送数字，或者补充更多背景信息。`;
}

module.exports = { handleTask, handleInlineReview, handleClarification };
