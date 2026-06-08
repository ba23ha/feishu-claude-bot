const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..', '..');
const SOUL_DIR = path.join(ROOT, 'boss-soul');
const PROMPTS_DIR = path.join(ROOT, 'prompts');

const SOUL_FILES = ['identity', 'style', 'decision', 'communication', 'taboos', 'examples'];
// 'distill' task type is handled separately in soul/updater.js and does not use loadPrompt()
const PROMPT_FILES = { reply: 'reply.md', polish: 'polish.md', review: 'review.md', meeting: 'meeting-summary.md' };

function loadSoul() {
  const soul = {};
  for (const key of SOUL_FILES) {
    const filePath = path.join(SOUL_DIR, `${key}.md`);
    soul[key] = fs.existsSync(filePath) ? fs.readFileSync(filePath, 'utf8') : '';
  }
  return soul;
}

function loadPrompt(taskType) {
  const filename = PROMPT_FILES[taskType];
  if (!filename) throw new Error(`Unknown task type: ${taskType}`);
  const filePath = path.join(PROMPTS_DIR, filename);
  if (!fs.existsSync(filePath)) throw new Error(`Prompt file not found: ${filePath}`);
  return fs.readFileSync(filePath, 'utf8');
}

function loadSystemPromptTemplate() {
  const filePath = path.join(PROMPTS_DIR, 'system.md');
  if (!fs.existsSync(filePath)) throw new Error('system.md not found');
  return fs.readFileSync(filePath, 'utf8');
}

function buildSystemPrompt() {
  const template = loadSystemPromptTemplate();
  const soul = loadSoul();
  const soulText = SOUL_FILES
    .filter(k => soul[k])
    .map(k => `### ${k}\n${soul[k]}`)
    .join('\n\n---\n\n');
  return template.replace('{{BOSS_SOUL}}', soulText);
}

module.exports = { loadSoul, loadPrompt, buildSystemPrompt };
