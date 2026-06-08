const { generateRunId, createAuditContext, recordSourceAccess, recordSoulUpdate } = require('../src/audit/runner');

describe('audit runner', () => {
  test('generateRunId returns unique string with expected format', () => {
    const id1 = generateRunId();
    const id2 = generateRunId();
    expect(id1).toMatch(/^dist_\d+_[a-z0-9]+$/);
    expect(id1).not.toBe(id2);
  });

  test('createAuditContext has all required fields', () => {
    const ctx = createAuditContext({ targetFile: 'decision', reason: '提炼决策' }, 'ou_boss123');
    expect(ctx.runId).toMatch(/^dist_/);
    expect(ctx.operator).toBe('ou_boss123');
    expect(ctx.triggeredAt).toBeTruthy();
    expect(ctx.reason).toBe('提炼决策');
    expect(Array.isArray(ctx.sources)).toBe(true);
    expect(Array.isArray(ctx.soulUpdates)).toBe(true);
    expect(ctx.sources).toHaveLength(0);
    expect(ctx.soulUpdates).toHaveLength(0);
  });

  test('createAuditContext accepts pre-assigned runId', () => {
    const ctx = createAuditContext({}, 'ou_boss', 'dist_test_fixed');
    expect(ctx.runId).toBe('dist_test_fixed');
  });

  test('recordSourceAccess appends to context.sources', () => {
    const ctx = createAuditContext({ targetFile: 'style' }, 'ou_boss');
    recordSourceAccess(ctx, {
      sourceId: 'msg_001', type: 'message', senderId: 'ou_boss',
      senderName: '老板', summary: '这是摘要', isDistilled: true,
    });
    expect(ctx.sources).toHaveLength(1);
    expect(ctx.sources[0].sourceId).toBe('msg_001');
    expect(ctx.sources[0].type).toBe('message');
    expect(ctx.sources[0].senderName).toBe('老板');
    expect(ctx.sources[0].isDistilled).toBe(true);
  });

  test('recordSourceAccess fills defaults for missing fields', () => {
    const ctx = createAuditContext({}, 'ou_boss');
    recordSourceAccess(ctx, { type: 'document' });
    expect(ctx.sources[0].sourceId).toMatch(/^src_/);
    expect(ctx.sources[0].isDistilled).toBe(true);
    expect(ctx.sources[0].excludedReason).toBeNull();
  });

  test('recordSoulUpdate appends to context.soulUpdates with runId', () => {
    const ctx = createAuditContext({ targetFile: 'decision', reason: '复盘' }, 'ou_boss');
    recordSoulUpdate(ctx, 'boss-soul/decision.md', ['msg_001', 'msg_002']);
    expect(ctx.soulUpdates).toHaveLength(1);
    expect(ctx.soulUpdates[0].file).toBe('boss-soul/decision.md');
    expect(ctx.soulUpdates[0].runId).toBe(ctx.runId);
    expect(ctx.soulUpdates[0].sourceIds).toEqual(['msg_001', 'msg_002']);
    expect(ctx.soulUpdates[0].reason).toBe('复盘');
  });
});
