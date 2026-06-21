const https = require('https');
const { getValidToken, hasValidAuth } = require('./oauth');

function httpsGet(path, token) {
  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'open.feishu.cn',
      path,
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` },
    }, res => {
      const chunks = [];
      res.on('data', d => chunks.push(d));
      res.on('end', () => {
        try { resolve(JSON.parse(Buffer.concat(chunks).toString('utf8'))); }
        catch (e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

async function getUserToken() {
  if (!hasValidAuth()) throw new Error('No valid user token. Run: node cli-boss.js auth-url');
  return getValidToken();
}

/**
 * List meeting minutes within a time range using the boss user token.
 * @param {number} startMs  Start timestamp in ms
 * @param {number} endMs    End timestamp in ms
 * @returns {Promise<Array<{minutesToken, topic, startTime}>>}
 */
async function listMinutes(startMs, endMs) {
  const token = await getUserToken();
  const res = await httpsGet('/open-apis/minutes/v1/minutes?page_size=50', token);
  if (res.code !== 0) throw new Error(`Feishu minutes API error ${res.code}: ${res.msg}`);

  return (res.data?.minutes || [])
    .filter(m => {
      const ts = parseInt(m.start_time, 10) * 1000;
      return ts >= startMs && ts <= endMs;
    })
    .map(m => ({
      minutesToken: m.token,
      topic: m.topic || '未命名会议',
      startTime: new Date(parseInt(m.start_time, 10) * 1000).toISOString(),
    }));
}

/**
 * Get the transcript of a meeting minute using the boss user token.
 * @param {string} minutesToken
 * @returns {Promise<string>}
 */
async function readMinutes(minutesToken) {
  if (!minutesToken) throw new Error('minutesToken is required');
  const token = await getUserToken();
  const res = await httpsGet(`/open-apis/minutes/v1/minutes/${minutesToken}`, token);
  if (res.code !== 0) throw new Error(`Feishu minutes API error ${res.code}: ${res.msg}`);

  const minute = res.data?.minute;
  if (!minute) throw new Error('No minute data returned');

  const lines = [];
  if (minute.topic) lines.push(`# 会议主题：${minute.topic}`);
  if (minute.start_time) {
    const dt = new Date(parseInt(minute.start_time, 10) * 1000);
    lines.push(`开始时间：${dt.toLocaleString('zh-CN')}`);
  }

  if (Array.isArray(minute.transcript?.paragraphs)) {
    lines.push('\n## 会议记录\n');
    for (const para of minute.transcript.paragraphs) {
      const speaker = para.speaker?.user?.name || '';
      const text = (para.words || []).map(w => w.text).join('');
      if (text.trim()) lines.push(speaker ? `**${speaker}**：${text}` : text);
    }
  }

  return lines.join('\n');
}

module.exports = { listMinutes, readMinutes };
