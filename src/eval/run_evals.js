// Runs eval cases and scores responses against expected_traits and bad_patterns.
require('dotenv').config();
const fs = require('fs');
const path = require('path');
const { handleTask } = require('../bot/handler');
const { generate } = require('../llm/client');

const EVALS_DIR = path.join(__dirname, '..', '..', 'evals');

const TASK_TYPE_MAP = {
  'reply-cases.jsonl': 'reply',
  'review-cases.jsonl': 'review',
  'meeting-cases.jsonl': 'meeting',
};

async function scoreResponse(input, response, expectedTraits, badPatterns) {
  const judgePrompt = `你是一个评测助手。请判断以下 AI 回复是否满足要求。

## 用户输入
${input}

## AI 回复
${response}

## 期望特征（每条满足得1分）
${expectedTraits.map((t, i) => `${i + 1}. ${t}`).join('\n')}

## 不良模式（每条出现扣1分）
${badPatterns.map((p, i) => `${i + 1}. ${p}`).join('\n')}

请按以下 JSON 格式输出（不要加任何其他文字）：
{
  "met_traits": ["实际满足的特征列表"],
  "violated_patterns": ["实际出现的不良模式列表"],
  "score": <0到1之间的小数>,
  "comment": "一句话总结"
}`;

  const result = await generate('你是一个严格的 AI 输出评测助手，只输出 JSON。', judgePrompt, { maxTokens: 500 });
  try {
    const match = result.match(/\{[\s\S]+\}/);
    if (!match) return { met_traits: [], violated_patterns: [], score: 0, comment: '评分输出格式错误' };
    return JSON.parse(match[0]);
  } catch {
    return { met_traits: [], violated_patterns: [], score: 0, comment: '评分解析失败' };
  }
}

async function runEvalFile(filename) {
  const taskType = TASK_TYPE_MAP[filename];
  if (!taskType) { console.warn(`Unknown eval file: ${filename}`); return []; }

  const filePath = path.join(EVALS_DIR, filename);
  if (!fs.existsSync(filePath)) { console.warn(`Eval file not found: ${filePath}`); return []; }

  const lines = fs.readFileSync(filePath, 'utf8').split('\n').filter(Boolean);
  const results = [];

  console.log(`\n=== Running ${filename} (${lines.length} cases) ===\n`);

  for (let i = 0; i < lines.length; i++) {
    let caseData;
    try { caseData = JSON.parse(lines[i]); } catch { continue; }

    const { input, expected_traits, bad_patterns, notes } = caseData;
    console.log(`[${i + 1}/${lines.length}] ${notes || input.slice(0, 40)}...`);

    let response;
    try {
      response = await handleTask(taskType, input);
    } catch (err) {
      response = `ERROR: ${err.message}`;
    }

    const score = await scoreResponse(input, response, expected_traits || [], bad_patterns || []);
    const passed = score.score >= 0.6;

    results.push({ input, notes, response, score, passed });
    console.log(`  ${passed ? '✅' : '❌'} Score: ${score.score.toFixed(2)} — ${score.comment}`);
  }

  return results;
}

async function main() {
  const files = Object.keys(TASK_TYPE_MAP);
  const allResults = {};
  let totalPassed = 0;
  let totalCases = 0;

  for (const file of files) {
    const results = await runEvalFile(file);
    allResults[file] = results;
    totalPassed += results.filter(r => r.passed).length;
    totalCases += results.length;
  }

  console.log('\n=== Eval Summary ===');
  for (const [file, results] of Object.entries(allResults)) {
    const passed = results.filter(r => r.passed).length;
    console.log(`  ${file}: ${passed}/${results.length} passed`);
  }
  console.log(`\nTotal: ${totalPassed}/${totalCases} passed (${totalCases > 0 ? Math.round(totalPassed / totalCases * 100) : 0}%)`);

  // Save report
  const reportPath = path.join(EVALS_DIR, `report-${new Date().toISOString().split('T')[0]}.json`);
  fs.writeFileSync(reportPath, JSON.stringify(allResults, null, 2));
  console.log(`\nReport saved: ${reportPath}`);

  if (totalCases > 0 && totalPassed / totalCases < 0.6) {
    console.error('\n❌ Eval pass rate below 60% — review boss-soul and prompts');
    process.exit(1);
  }
}

main().catch(err => { console.error(err); process.exit(1); });
