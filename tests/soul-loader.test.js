const { loadSoul, loadSkill, loadPrompt, buildSystemPrompt } = require('../src/soul/loader');

describe('soul loader', () => {
  test('loadSoul returns object with all soul file keys', () => {
    const soul = loadSoul();
    expect(soul).toHaveProperty('style');
    expect(soul).toHaveProperty('decision');
    expect(soul).toHaveProperty('management');
    expect(soul).toHaveProperty('communication');
    expect(soul).toHaveProperty('taboos');
    expect(typeof soul.management).toBe('string');
    expect(soul.management.length).toBeGreaterThan(0);
  });

  test('loadSkill returns string content for valid task type', () => {
    const skill = loadSkill('review_inline');
    expect(typeof skill).toBe('string');
    expect(skill.length).toBeGreaterThan(0);
  });

  test('loadSkill throws for unknown task type', () => {
    expect(() => loadSkill('unknown')).toThrow();
  });

  test('loadPrompt (deprecated alias) still works', () => {
    const prompt = loadPrompt('review_inline');
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
