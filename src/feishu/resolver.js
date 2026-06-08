require('dotenv').config();
const { getFeishuClient } = require('./client');

// In-process cache: openId → name (cleared on restart, no persistence)
const _cache = new Map();

/**
 * Resolve a single Feishu open_id to a display name.
 * Returns a fallback string if the API is unavailable or user is unknown.
 * @param {string} openId
 * @returns {Promise<string>}
 */
async function resolveUser(openId) {
  if (!openId || openId === 'unknown') return 'unknown_user';
  if (_cache.has(openId)) return _cache.get(openId);

  try {
    const client = getFeishuClient();
    const res = await client.contact.user.get({
      path: { user_id: openId },
      params: { user_id_type: 'open_id' },
    });
    if (res.code === 0 && res.data?.user?.name) {
      _cache.set(openId, res.data.user.name);
      return res.data.user.name;
    }
  } catch {}

  const fallback = `unknown_user_${openId.slice(-6)}`;
  _cache.set(openId, fallback);
  return fallback;
}

/**
 * Resolve multiple open_ids in parallel.
 * @param {string[]} openIds
 * @returns {Promise<Object.<string, string>>}  openId → name map
 */
async function resolveUsers(openIds) {
  const unique = [...new Set((openIds || []).filter(Boolean))];
  const result = {};
  await Promise.all(unique.map(async id => {
    result[id] = await resolveUser(id);
  }));
  return result;
}

module.exports = { resolveUser, resolveUsers };
