const { getFeishuClient } = require('./client');

/**
 * Read messages from a chat within a time range, optionally filtered by keyword.
 * @param {object} opts
 * @param {string} opts.chatId      Group/chat ID
 * @param {number} opts.startMs     Start timestamp in ms (inclusive)
 * @param {number} opts.endMs       End timestamp in ms (inclusive)
 * @param {string} [opts.keyword]   Optional keyword filter
 * @param {number} [opts.maxCount]  Max messages to fetch (default 200)
 * @returns {Promise<Array<{sender: string, timestamp: string, text: string}>>}
 */
async function readMessages({ chatId, startMs, endMs, keyword, maxCount = 200 }) {
  if (!chatId) throw new Error('chatId is required');
  if (!startMs || !endMs) throw new Error('startMs and endMs are required');

  const client = getFeishuClient();
  const collected = [];
  let pageToken;

  while (collected.length < maxCount) {
    const params = {
      container_id_type: 'chat',
      container_id: chatId,
      page_size: 50,
      sort_type: 'ByCreateTimeDesc',
    };
    if (pageToken) params.page_token = pageToken;

    const res = await client.im.message.list({ params });
    if (res.code !== 0) throw new Error(`Feishu API error ${res.code}: ${res.msg}`);

    const items = res.data?.items || [];
    if (items.length === 0) break;

    let reachedOlder = false;
    for (const item of items) {
      const ts = parseInt(item.create_time, 10);
      if (ts < startMs) { reachedOlder = true; break; } // messages older than range — stop pagination
      if (ts > endMs) continue;

      let text = '';
      try {
        const body = JSON.parse(item.body?.content || '{}');
        text = body.text || '';
      } catch { continue; }

      if (!text) continue;
      if (keyword && !text.includes(keyword)) continue;

      collected.push({
        sender: item.sender?.id?.open_id || 'unknown',
        timestamp: new Date(ts).toISOString(),
        text: text.replace(/@\S+/g, '').trim(),
      });

      if (collected.length >= maxCount) break;
    }

    if (reachedOlder) break;
    pageToken = res.data?.page_token;
    if (!pageToken) break;
  }

  return collected.reverse();
}

module.exports = { readMessages };
