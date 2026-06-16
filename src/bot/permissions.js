function isBoss(openId) {
  const bossId = process.env.BOSS_OPEN_ID;
  if (!bossId || !openId) return false;
  return openId === bossId;
}

function isEmployee(openId) {
  if (!openId) return false;
  return (process.env.EMPLOYEE_OPEN_IDS || '')
    .split(',').map(s => s.trim()).filter(Boolean)
    .includes(openId);
}

// Boss or whitelisted employee
function isMember(openId) {
  return isBoss(openId) || isEmployee(openId);
}

function assertBoss(openId) {
  if (!isBoss(openId)) {
    console.warn(`[permissions] Unauthorized access attempt from: ${openId}`);
    throw new Error('unauthorized: boss-only feature');
  }
}

module.exports = { isBoss, isEmployee, isMember, assertBoss };
