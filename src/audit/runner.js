const fs = require('fs');
const path = require('path');

const AUDIT_DIR = path.join(__dirname, '..', '..', 'audit');

function generateRunId() {
  const ts = Date.now();
  const rand = Math.random().toString(36).slice(2, 8);
  return `dist_${ts}_${rand}`;
}

/**
 * Create an audit context that tracks all sources accessed and soul updates made.
 * @param {object} opts         Distill options (targetFile, reason, chatId, etc.)
 * @param {string} operator     Feishu open_id of whoever triggered the command
 * @param {string} [runId]      Pre-assigned run_id (e.g. from dry-run phase)
 */
function createAuditContext(opts, operator, runId = null) {
  fs.mkdirSync(AUDIT_DIR, { recursive: true });
  return {
    runId: runId || generateRunId(),
    operator: operator || 'unknown',
    triggeredAt: new Date().toISOString(),
    triggerCommand: opts._command || '',
    reason: opts.reason || '',
    opts,
    sources: [],
    soulUpdates: [],
  };
}

/**
 * Record a single data source access (message / document / minutes).
 * @param {object} context  AuditContext from createAuditContext
 * @param {object} source
 * @param {string} source.sourceId
 * @param {string} source.type         'message' | 'document' | 'minutes'
 * @param {string} [source.chatId]
 * @param {string} [source.senderId]
 * @param {string} [source.senderName]
 * @param {string} [source.createTime]
 * @param {boolean} [source.isFromBoss]
 * @param {string} [source.contentHash]
 * @param {string} [source.summary]    Desensitised excerpt (no raw content)
 * @param {boolean} [source.isDistilled]
 * @param {string} [source.excludedReason]
 */
function recordSourceAccess(context, source) {
  context.sources.push({
    sourceId: source.sourceId || `src_${Date.now()}`,
    type: source.type,
    chatId: source.chatId || null,
    senderId: source.senderId || null,
    senderName: source.senderName || null,
    createTime: source.createTime || null,
    isFromBoss: source.isFromBoss || false,
    contentHash: source.contentHash || null,
    summary: source.summary || '',
    isDistilled: source.isDistilled !== undefined ? source.isDistilled : true,
    excludedReason: source.excludedReason || null,
  });
}

/**
 * Record that a soul file was updated as a result of this distillation.
 * @param {object} context
 * @param {string} file       e.g. 'boss-soul/decision.md'
 * @param {string[]} sourceIds  source_ids that contributed to this update
 */
function recordSoulUpdate(context, file, sourceIds) {
  context.soulUpdates.push({
    file,
    runId: context.runId,
    sourceIds: sourceIds || [],
    reason: context.reason,
    timestamp: new Date().toISOString(),
  });
}

module.exports = { generateRunId, createAuditContext, recordSourceAccess, recordSoulUpdate, AUDIT_DIR };
