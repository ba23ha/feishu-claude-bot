const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..', '..');
const SOUL_DIR = path.join(ROOT, 'boss-bot', 'soul');
const SKILLS_DIR = path.join(ROOT, 'boss-bot', 'skills');
const MEMORY_DIR = path.join(ROOT, 'boss-bot', 'memory');
const PROMPTS_DIR = path.join(ROOT, 'prompts');

const SOUL_FILES = ['style', 'decision', 'management', 'communication', 'taboos'];
// 'distill' task type is handled separately in soul/updater.js and does not use loadSkill()
// 'polish' is merged into 'reply'
const SKILL_FILES = {
  reply: 'reply.md',
  polish: 'reply.md',
  review: 'review-proposal.md',
  review_inline: 'review-proposal.md',
  meeting: 'meeting-summary.md',
  delegation: 'task-delegation.md',
  followup: 'follow-up.md',
};

function loadSoul() {
  const soul = {};
  for (const key of SOUL_FILES) {
    const filePath = path.join(SOUL_DIR, `${key}.md`);
    soul[key] = fs.existsSync(filePath) ? fs.readFileSync(filePath, 'utf8') : '';
  }
  return soul;
}

function loadSkill(taskType) {
  const filename = SKILL_FILES[taskType];
  if (!filename) throw new Error(`Unknown task type: ${taskType}`);
  const filePath = path.join(SKILLS_DIR, filename);
  if (!fs.existsSync(filePath)) throw new Error(`Skill file not found: ${filePath}`);
  return fs.readFileSync(filePath, 'utf8');
}

function loadMemory(memoryFile) {
  const filePath = path.join(MEMORY_DIR, `${memoryFile}.md`);
  return fs.existsSync(filePath) ? fs.readFileSync(filePath, 'utf8') : '';
}

/** @deprecated use loadSkill instead */
function loadPrompt(taskType) {
  return loadSkill(taskType);
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

module.exports = { loadSoul, loadSkill, loadMemory, loadPrompt, buildSystemPrompt };
