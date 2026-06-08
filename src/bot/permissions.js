/**
 * Check if the given Feishu open_id belongs to the boss.
 */
function isBoss(openId) {
  const bossId = process.env.BOSS_OPEN_ID;
  if (!bossId || !openId) return false;
  return openId === bossId;
}

/**
 * Assert that the sender is the boss. Throws if not.
 */
function assertBoss(openId) {
  if (!isBoss(openId)) {
    console.warn(`[permissions] Unauthorized access attempt from: ${openId}`);
    throw new Error('unauthorized: boss-only feature');
  }
}

module.exports = { isBoss, assertBoss };
