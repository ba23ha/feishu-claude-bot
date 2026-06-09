const { buildSystemPrompt, loadSkill, loadMemory } = require('../soul/loader');
const { generate } = require('../llm/client');

/**
 * Handle a task request from the boss.
 * @param {'reply'|'polish'|'review'|'meeting'|'general'} taskType
 * @param {string} userInput  Raw message from boss
 * @returns {Promise<string>}  The response to send back
 */
async function handleTask(taskType, userInput) {
  const systemPrompt = buildSystemPrompt();

  if (taskType === 'general') {
    return generate(systemPrompt, userInput);
  }

  // Note: 'distill' is handled in server.js before calling handleTask — never reaches here
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

module.exports = { handleTask, handleClarification };
