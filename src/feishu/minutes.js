const { getFeishuClient } = require('./client');

/**
 * Get a list of recent meeting minutes accessible to the app.
 * @param {number} [limit=20]
 * @returns {Promise<Array<{minutesToken: string, topic: string, startTime: string}>>}
 */
async function listMinutes(limit = 20) {
  const client = getFeishuClient();
  const res = await client.minutes.minute.list({
    params: { page_size: limit },
  });
  if (res.code !== 0) throw new Error(`Feishu API error ${res.code}: ${res.msg}`);
  return (res.data?.minutes || []).map(m => ({
    minutesToken: m.token,
    topic: m.topic || '未命名会议',
    startTime: new Date(parseInt(m.start_time, 10) * 1000).toISOString(),
  }));
}

/**
 * Get the transcript/summary of a meeting by minutes token.
 * @param {string} minutesToken
 * @returns {Promise<string>}
 */
async function readMinutes(minutesToken) {
  if (!minutesToken) throw new Error('minutesToken is required');
  const client = getFeishuClient();

  const res = await client.minutes.minute.get({
    path: { minute_token: minutesToken },
  });
  if (res.code !== 0) throw new Error(`Feishu API error ${res.code}: ${res.msg}`);

  const minute = res.data?.minute;
  if (!minute) throw new Error('No minute data returned');

  const lines = [];
  if (minute.topic) lines.push(`# 会议主题：${minute.topic}`);
  if (minute.start_time) lines.push(`开始时间：${new Date(parseInt(minute.start_time, 10) * 1000).toISOString()}`);

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
