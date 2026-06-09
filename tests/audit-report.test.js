const fs = require('fs');
const path = require('path');
const { generateReport } = require('../src/audit/report');
const { createAuditContext, recordSourceAccess, recordSoulUpdate, REPORTS_DIR } = require('../src/audit/runner');
const AUDIT_DIR = REPORTS_DIR;

function makeContext(runId = 'dist_test_rpt_001') {
  const ctx = createAuditContext(
    { targetFile: 'decision', reason: '提炼决策标准', chatId: 'oc_test', startMs: 1000000, endMs: 2000000 },
    'ou_boss123',
    runId
  );
  recordSourceAccess(ctx, {
    sourceId: 'msg_001', type: 'message', senderId: 'ou_boss123',
    senderName: '老板', isFromBoss: true,
    contentHash: 'sha256:aabbccdd', summary: '这个方案可以推进', isDistilled: true,
  });
  recordSourceAccess(ctx, {
    sourceId: 'msg_002', type: 'message', senderId: 'ou_user456',
    senderName: '李四', isFromBoss: false,
    contentHash: 'sha256:eeff0011', summary: '我觉得风险有点大', isDistilled: true,
  });
  recordSourceAccess(ctx, {
    sourceId: 'msg_003', type: 'message', senderId: 'ou_user456',
    senderName: '李四', isFromBoss: false,
    contentHash: 'sha256:22334455', summary: '另一条消息', isDistilled: false,
    excludedReason: '关键词过滤',
  });
  recordSoulUpdate(ctx, 'boss-soul/decision.md', ['msg_001', 'msg_002']);
  return ctx;
}

describe('generateReport', () => {
  let reportPath;
  let date;

  beforeEach(() => {
    date = new Date().toISOString().split('T')[0];
  });

  afterEach(() => {
    // Clean up generated files
    const runId = 'dist_test_rpt_001';
    const rp = path.join(AUDIT_DIR, `${date}-${runId}-report.md`);
    const ap = path.join(AUDIT_DIR, `${date}-${runId}-access.jsonl`);
    if (fs.existsSync(rp)) fs.unlinkSync(rp);
    if (fs.existsSync(ap)) fs.unlinkSync(ap);
  });

  test('creates report.md file', () => {
    const ctx = makeContext();
    reportPath = generateReport(ctx);
    expect(fs.existsSync(reportPath)).toBe(true);
  });

  test('report contains run_id', () => {
    const ctx = makeContext();
    reportPath = generateReport(ctx);
    expect(fs.readFileSync(reportPath, 'utf8')).toContain('dist_test_rpt_001');
  });

  test('report contains per-user stats', () => {
    const ctx = makeContext();
    reportPath = generateReport(ctx);
    const content = fs.readFileSync(reportPath, 'utf8');
    expect(content).toContain('老板');
    expect(content).toContain('李四');
  });

  test('report contains soul update mapping with source_ids', () => {
    const ctx = makeContext();
    reportPath = generateReport(ctx);
    const content = fs.readFileSync(reportPath, 'utf8');
    expect(content).toContain('boss-soul/decision.md');
    expect(content).toContain('msg_001');
  });

  test('report distinguishes distilled vs excluded sources', () => {
    const ctx = makeContext();
    reportPath = generateReport(ctx);
    const content = fs.readFileSync(reportPath, 'utf8');
    expect(content).toContain('进入蒸馏');
    expect(content).toContain('未进入蒸馏');
    expect(content).toContain('关键词过滤');
  });

  test('also creates access.jsonl file', () => {
    const ctx = makeContext();
    reportPath = generateReport(ctx);
    const accessPath = path.join(AUDIT_DIR, `${date}-dist_test_rpt_001-access.jsonl`);
    expect(fs.existsSync(accessPath)).toBe(true);
    const lines = fs.readFileSync(accessPath, 'utf8').split('\n').filter(Boolean);
    expect(lines.length).toBeGreaterThan(0);
    // Each line should be valid JSON
    for (const line of lines) {
      expect(() => JSON.parse(line)).not.toThrow();
    }
  });
});
