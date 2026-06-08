const fs = require('fs');
const path = require('path');

const CHANGELOG_PATH = path.join(__dirname, '..', '..', 'boss-soul', 'changelog.md');

/**
 * Append an entry to changelog.md.
 * @param {object} entry
 * @param {string} entry.file      Which boss-soul file was updated
 * @param {string} entry.reason    Why it was updated
 * @param {string} entry.summary   What changed (brief)
 * @param {string} [entry.operator] Who triggered the update (defaults to 'system')
 */
function appendChangelog({ file, reason, summary, operator = 'system' }) {
  const date = new Date().toISOString().split('T')[0];
  const row = `| ${date} | 更新 | ${file} | ${reason} | ${operator} |`;

  let content = fs.existsSync(CHANGELOG_PATH)
    ? fs.readFileSync(CHANGELOG_PATH, 'utf8')
    : '# Skill 变更记录\n\n| 日期 | 操作 | 影响文件 | 原因 | 操作人 |\n|------|------|----------|------|--------|\n';

  content = content.trimEnd() + '\n' + row + '\n';
  fs.writeFileSync(CHANGELOG_PATH, content);

  console.log(`[changelog] ${date} | ${file} | ${reason}`);
}

module.exports = { appendChangelog };
