#!/usr/bin/env node
/**
 * Eval: 通用模型 vs Soul + Skill
 * 对比两种条件下对同一份文档的审阅输出质量
 * 用法: node evals/run-review-eval.js
 */

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const { buildSystemPrompt, loadSkill } = require('../src/soul/loader');

const CASES_FILE = path.join(__dirname, 'review-cases.jsonl');
const OUT_FILE = path.join(__dirname, `results-${new Date().toISOString().slice(0,10)}.md`);

// ── LLM 调用（复用 llm/client.js 的调用方式）──────────────────────────
function callClaude(systemPrompt, userMessage) {
  const fullPrompt = systemPrompt
    ? `<system>\n${systemPrompt}\n</system>\n\n${userMessage}`
    : userMessage;

  return new Promise((resolve, reject) => {
    const proc = spawn('claude', ['-p', fullPrompt], {
      env: { ...process.env },
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    let out = '';
    let err = '';
    const timer = setTimeout(() => { proc.kill(); reject(new Error('timeout')); }, 90000);
    proc.stdout.on('data', d => { out += d; });
    proc.stderr.on('data', d => { err += d; });
    proc.on('close', code => {
      clearTimeout(timer);
      code !== 0 ? reject(new Error(err.slice(0, 200))) : resolve(out.trim());
    });
  });
}

// ── 两种条件 ────────────────────────────────────────────────────────────
async function runBaseline(input) {
  // Condition A: 无 system prompt，裸问
  return callClaude(null, `请帮我审阅以下内容，指出存在的问题：\n\n${input}`);
}

async function runWithSkill(input) {
  // Condition B: Soul + review_inline Skill，结构化输出
  const systemPrompt = buildSystemPrompt();
  const skill = loadSkill('review_inline');
  const combined = `${systemPrompt}\n\n---\n\n## 当前任务指令\n\n${skill}`;
  const userPrompt = `review_mode: inline_comment\nmax_comments: 5\n\n文档内容：\n${input}\n\n请严格按 inline_comment JSON 输出格式输出，不要输出其他内容。`;
  return callClaude(combined, userPrompt);
}

// ── 主流程 ──────────────────────────────────────────────────────────────
async function main() {
  const cases = fs.readFileSync(CASES_FILE, 'utf8')
    .split('\n').filter(Boolean).map(l => JSON.parse(l));

  const lines = [
    '# Eval 对比报告',
    `> 生成时间：${new Date().toLocaleString('zh-CN')}`,
    `> 用例数量：${cases.length}`,
    '',
    '---',
    '',
  ];

  for (let i = 0; i < cases.length; i++) {
    const { input, notes, expected_traits, bad_patterns } = cases[i];

    console.log(`\n[${i + 1}/${cases.length}] 正在跑 Case ${i + 1}...`);

    lines.push(`## Case ${i + 1}`);
    lines.push(`**输入：** ${input}`);
    lines.push(`**预期关注点：** ${expected_traits?.join('、')}`);
    lines.push(`**应规避：** ${bad_patterns?.join('、')}`);
    lines.push(`**备注：** ${notes}`);
    lines.push('');

    // Condition A
    console.log(`  → Condition A (基线)...`);
    let baselineOut;
    try {
      baselineOut = await runBaseline(input);
    } catch (e) {
      baselineOut = `ERROR: ${e.message}`;
    }

    lines.push('### Condition A — 通用模型（无 Soul / 无 Skill）');
    lines.push('```');
    lines.push(baselineOut);
    lines.push('```');
    lines.push('');

    // Condition B
    console.log(`  → Condition B (Soul + Skill)...`);
    let skillOut;
    try {
      skillOut = await runWithSkill(input);
    } catch (e) {
      skillOut = `ERROR: ${e.message}`;
    }

    lines.push('### Condition B — Soul + review_inline Skill');
    lines.push('```json');
    lines.push(skillOut);
    lines.push('```');
    lines.push('');
    lines.push('---');
    lines.push('');
  }

  fs.writeFileSync(OUT_FILE, lines.join('\n'), 'utf8');
  console.log(`\n✅ 完成，结果已写入：${OUT_FILE}`);
}

main().catch(e => { console.error(e); process.exit(1); });
