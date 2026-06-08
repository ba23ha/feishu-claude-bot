// cli-boss.js — local command line test entry for Boss Copilot (no Feishu needed)
// Usage:
//   node cli-boss.js reply "背景：对方催进度，我想说延期"
//   node cli-boss.js polish "大家一起看下这个事情能不能做"
//   node cli-boss.js review "方案文本..."
//   node cli-boss.js meeting "会议纪要文本..."
//   node cli-boss.js general "问个问题"
//   node cli-boss.js auto "帮我润色一下这段话：xxx"

require('dotenv').config();
const { handleTask, handleClarification } = require('./src/bot/handler');
const { detectTaskType } = require('./src/bot/router');

const [, , taskArg, ...rest] = process.argv;
const VALID_TYPES = ['reply', 'polish', 'review', 'meeting', 'general'];

async function main() {
  let taskType = taskArg;
  let input = rest.join(' ');

  if (!taskType) {
    console.error('Usage: node cli-boss.js <reply|polish|review|meeting|general|auto> "<input>"');
    process.exit(1);
  }

  if (taskType === 'auto') {
    taskType = detectTaskType(input);
    console.log(`[auto-detected task type: ${taskType}]`);
  }

  if (!VALID_TYPES.includes(taskType)) {
    console.error(`Unknown task type: ${taskType}. Valid: ${VALID_TYPES.join(', ')}, auto`);
    process.exit(1);
  }

  if (!input.trim()) {
    console.error('Error: input cannot be empty');
    process.exit(1);
  }

  console.log(`\n=== Boss Copilot CLI ===`);
  console.log(`Task: ${taskType}`);
  console.log(`Input: ${input}\n`);
  console.log('Generating...\n');

  try {
    const result = await handleTask(taskType, input);
    console.log('--- Response ---\n');
    console.log(result);
    console.log('\n---');
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

main();
