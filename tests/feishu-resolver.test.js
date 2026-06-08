// resolver.js catches all Feishu API errors and returns fallback names,
// so these tests run without real credentials.
const { resolveUser, resolveUsers } = require('../src/feishu/resolver');

describe('resolveUser', () => {
  test('returns unknown_user for null/empty input', async () => {
    expect(await resolveUser(null)).toBe('unknown_user');
    expect(await resolveUser('')).toBe('unknown_user');
    expect(await resolveUser('unknown')).toBe('unknown_user');
  });

  test('returns fallback string when API unavailable', async () => {
    // No real Feishu credentials in test env — falls back gracefully
    const name = await resolveUser('ou_test123456');
    expect(typeof name).toBe('string');
    expect(name.length).toBeGreaterThan(0);
  });

  test('caches results — same id returns same value', async () => {
    const first = await resolveUser('ou_cache_test99');
    const second = await resolveUser('ou_cache_test99');
    expect(first).toBe(second);
  });
});

describe('resolveUsers', () => {
  test('returns map for all input ids', async () => {
    const result = await resolveUsers(['ou_aaa111', 'ou_bbb222']);
    expect(result).toHaveProperty('ou_aaa111');
    expect(result).toHaveProperty('ou_bbb222');
  });

  test('deduplicates ids', async () => {
    const result = await resolveUsers(['ou_dup', 'ou_dup', 'ou_dup']);
    expect(Object.keys(result)).toHaveLength(1);
  });

  test('handles empty array', async () => {
    const result = await resolveUsers([]);
    expect(result).toEqual({});
  });
});
