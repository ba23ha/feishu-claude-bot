const { formatDryRunMessage } = require('../src/audit/dry-run');

describe('formatDryRunMessage', () => {
  const baseResult = {
    runId: 'dist_1717800000000_abc123',
    opts: { targetFile: 'decision', reason: '提炼决策', chatId: 'oc_xxx' },
    chatPreview: {
      chatId: 'oc_xxx',
      estimatedMessages: 50,
      senderCounts: { ou_boss123: 30, ou_user456: 20 },
      senderNames: { ou_boss123: '张三', ou_user456: '李四' },
      timeRange: { from: '2026-06-01T00:00:00.000Z', to: '2026-06-08T00:00:00.000Z' },
      keyword: null,
    },
    docPreview: null,
    minutesPreview: null,
    riskFlags: ['包含非老板用户数据（20 条消息）'],
  };

  test('contains run_id', () => {
    expect(formatDryRunMessage(baseResult)).toContain('dist_1717800000000_abc123');
  });

  test('contains target file', () => {
    expect(formatDryRunMessage(baseResult)).toContain('boss-soul/decision.md');
  });

  test('contains resolved user names', () => {
    const msg = formatDryRunMessage(baseResult);
    expect(msg).toContain('张三');
    expect(msg).toContain('李四');
  });

  test('contains confirm/cancel instructions', () => {
    const msg = formatDryRunMessage(baseResult);
    expect(msg).toContain('确认');
    expect(msg).toContain('取消');
  });

  test('contains risk flag when present', () => {
    expect(formatDryRunMessage(baseResult)).toContain('风险提示');
    expect(formatDryRunMessage(baseResult)).toContain('非老板用户数据');
  });

  test('no risk section when riskFlags is empty', () => {
    const result = { ...baseResult, riskFlags: [] };
    expect(formatDryRunMessage(result)).not.toContain('风险提示');
  });

  test('shows minutes preview when present', () => {
    const result = {
      ...baseResult,
      chatPreview: null,
      minutesPreview: { minutesToken: 'min_xxx', topic: '周一站会', startTime: '2026-06-08T09:00:00.000Z' },
      riskFlags: [],
    };
    const msg = formatDryRunMessage(result);
    expect(msg).toContain('周一站会');
    expect(msg).toContain('2026-06-08');
  });

  test('shows doc preview when present', () => {
    const result = { ...baseResult, chatPreview: null, docPreview: { docToken: 'doxcnABC123' }, riskFlags: [] };
    expect(formatDryRunMessage(result)).toContain('doxcnABC123');
  });
});
