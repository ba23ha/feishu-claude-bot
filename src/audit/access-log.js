const fs = require('fs');
const path = require('path');
const { REPORTS_DIR } = require('./runner');

/**
 * Write machine-readable access log (JSONL) for the audit context.
 * Each line is one source record.
 * @param {object} context  AuditContext
 * @returns {string}  Path to the written file
 */
function writeAccessLog(context) {
  const date = new Date().toISOString().split('T')[0];
  const filename = `${date}-${context.runId}-access.jsonl`;
  const filePath = path.join(REPORTS_DIR, filename);

  const header = JSON.stringify({
    _type: 'audit_header',
    runId: context.runId,
    operator: context.operator,
    triggeredAt: context.triggeredAt,
    reason: context.reason,
    opts: context.opts,
  });

  const sourceLines = context.sources.map(s => JSON.stringify(s));
  const updateLines = context.soulUpdates.map(u => JSON.stringify({ _type: 'soul_update', ...u }));

  fs.writeFileSync(filePath, [header, ...sourceLines, ...updateLines].join('\n') + '\n');
  return filePath;
}

module.exports = { writeAccessLog };
