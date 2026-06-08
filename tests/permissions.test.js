const { isBoss, assertBoss } = require('../src/bot/permissions');

describe('permissions', () => {
  const originalEnv = process.env.BOSS_OPEN_ID;

  beforeEach(() => { process.env.BOSS_OPEN_ID = 'ou_boss123'; });
  afterEach(() => { process.env.BOSS_OPEN_ID = originalEnv; });

  test('isBoss returns true for boss open_id', () => {
    expect(isBoss('ou_boss123')).toBe(true);
  });

  test('isBoss returns false for other users', () => {
    expect(isBoss('ou_other456')).toBe(false);
    expect(isBoss('')).toBe(false);
    expect(isBoss(null)).toBe(false);
  });

  test('assertBoss does not throw for boss', () => {
    expect(() => assertBoss('ou_boss123')).not.toThrow();
  });

  test('assertBoss throws for non-boss', () => {
    expect(() => assertBoss('ou_stranger')).toThrow('unauthorized');
  });

  test('isBoss returns false when BOSS_OPEN_ID not configured', () => {
    delete process.env.BOSS_OPEN_ID;
    expect(isBoss('ou_anyone')).toBe(false);
  });
});
