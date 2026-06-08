const { buildSystemPrompt, loadPrompt } = require('../soul/loader');
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
  if (!['reply', 'polish', 'review', 'meeting'].includes(taskType)) {
    throw new Error(`Unknown task type: ${taskType}`);
  }

  const taskPrompt = loadPrompt(taskType);
  const combinedSystem = `${systemPrompt}\n\n---\n\n## 当前任务指令\n\n${taskPrompt}`;
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
