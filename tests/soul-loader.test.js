const { loadSoul, loadPrompt, buildSystemPrompt } = require('../src/soul/loader');

describe('soul loader', () => {
  test('loadSoul returns object with all soul file keys', () => {
    const soul = loadSoul();
    expect(soul).toHaveProperty('identity');
    expect(soul).toHaveProperty('style');
    expect(soul).toHaveProperty('decision');
    expect(soul).toHaveProperty('communication');
    expect(soul).toHaveProperty('taboos');
    expect(soul).toHaveProperty('examples');
    expect(typeof soul.identity).toBe('string');
    expect(soul.identity.length).toBeGreaterThan(0);
  });

  test('loadPrompt returns string content for valid task type', () => {
    const prompt = loadPrompt('reply');
    expect(typeof prompt).toBe('string');
    expect(prompt.length).toBeGreaterThan(0);
  });

  test('loadPrompt throws for unknown task type', () => {
    expect(() => loadPrompt('unknown')).toThrow();
  });

  test('buildSystemPrompt injects boss-soul into system prompt', () => {
    const result = buildSystemPrompt();
    expect(result).not.toContain('{{BOSS_SOUL}}');
    expect(result.length).toBeGreaterThan(100);
  });
});
