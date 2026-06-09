const fs = require('fs');
const path = require('path');

const CHANGELOG_PATH = path.join(__dirname, '..', '..', 'boss-bot', 'soul', 'changelog.md');

const DEFAULT_HEADER = '# Skill 变更记录\n\n| 日期 | 操作 | 影响文件 | 原因 | run_id | 操作人 |\n|------|------|----------|------|--------|--------|\n';

/**
 * Append an entry to changelog.md.
 * @param {object} entry
 * @param {string} entry.file       Which boss-soul file was updated
 * @param {string} entry.reason     Why it was updated
 * @param {string} entry.summary    What changed (brief, used for display only)
 * @param {string} [entry.operator] Who triggered the update
 * @param {string} [entry.runId]    Audit run_id for traceability
 */
function appendChangelog({ file, reason, summary, operator = 'system', runId = '—' }) {
  const date = new Date().toISOString().split('T')[0];
  const row = `| ${date} | 更新 | ${file} | ${reason} | \`${runId}\` | ${operator} |`;

  let content = fs.existsSync(CHANGELOG_PATH)
    ? fs.readFileSync(CHANGELOG_PATH, 'utf8')
    : DEFAULT_HEADER;

  content = content.trimEnd() + '\n' + row + '\n';
  fs.writeFileSync(CHANGELOG_PATH, content);

  console.log(`[changelog] ${date} | ${file} | run_id: ${runId} | ${reason}`);
}

module.exports = { appendChangelog };
