const { detectTaskType } = require('../src/bot/router');

describe('detectTaskType', () => {
  test('detects reply task', () => {
    expect(detectTaskType('帮我回复这条消息')).toBe('reply');
    expect(detectTaskType('代写一个飞书回复')).toBe('reply');
    expect(detectTaskType('帮我写一下回复')).toBe('reply');
  });

  test('detects polish as reply task (polish merged into reply)', () => {
    expect(detectTaskType('帮我润色一下')).toBe('reply');
    expect(detectTaskType('优化一下这段话')).toBe('reply');
    expect(detectTaskType('帮我改写这段文字')).toBe('reply');
  });

  test('detects delegation task', () => {
    expect(detectTaskType('帮我安排一下这件事')).toBe('delegation');
    expect(detectTaskType('委派给张三')).toBe('delegation');
  });

  test('detects followup task', () => {
    expect(detectTaskType('帮我催一下负责人')).toBe('followup');
    expect(detectTaskType('追一下进度')).toBe('followup');
  });

  test('detects review task', () => {
    expect(detectTaskType('帮我点评这个方案')).toBe('review');
    expect(detectTaskType('看一下这个汇报')).toBe('review');
    expect(detectTaskType('评价一下这个计划')).toBe('review');
  });

  test('detects meeting task', () => {
    expect(detectTaskType('提炼一下会议纪要')).toBe('meeting');
    expect(detectTaskType('总结这次会议')).toBe('meeting');
    expect(detectTaskType('帮我看下妙记')).toBe('meeting');
  });

  test('detects distill task', () => {
    expect(detectTaskType('/distill 读取A群消息')).toBe('distill');
    expect(detectTaskType('蒸馏老板的风格')).toBe('distill');
  });

  test('returns general for ambiguous input', () => {
    expect(detectTaskType('你好')).toBe('general');
    expect(detectTaskType('现在几点了')).toBe('general');
  });
});
