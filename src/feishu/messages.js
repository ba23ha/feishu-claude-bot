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

  let token;
  if (hasValidAuth()) {
    token = await getValidToken();
    console.log('[messages] using boss user token');
  } else {
    throw new Error('No valid user token. Run: node cli-boss.js auth-url');
  }

  const collected = [];
  let pageToken;

  while (collected.length < maxCount) {
    let qs = `container_id_type=chat&container_id=${chatId}&page_size=50&sort_type=ByCreateTimeDesc`;
    if (pageToken) qs += `&page_token=${encodeURIComponent(pageToken)}`;

    const res = await httpsGet(`/open-apis/im/v1/messages?${qs}`, token);
    if (res.code !== 0) throw new Error(`Feishu API error ${res.code}: ${res.msg}`);

    const items = res.data?.items || [];
    if (items.length === 0) break;

    let reachedOlder = false;
    for (const item of items) {
      const ts = parseInt(item.create_time, 10);
      if (ts < startMs) { reachedOlder = true; break; }
      if (ts > endMs) continue;

      let text = '';
      try {
        const body = JSON.parse(item.body?.content || '{}');
        text = body.text || '';
      } catch { continue; }

      if (!text) continue;
      if (keyword && !text.includes(keyword)) continue;

      collected.push({
        sender: item.sender?.id || 'unknown',
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

/**
 * List all chats the authorized user (boss) is in.
 * @returns {Promise<Array<{chatId: string, name: string, type: string}>>}
 */
async function listAllChats() {
  const token = await getValidToken();
  const results = [];
  let pageToken;
  do {
    const qs = `page_size=50${pageToken ? `&page_token=${encodeURIComponent(pageToken)}` : ''}`;
    const res = await httpsGet(`/open-apis/im/v1/chats?${qs}`, token);
    if (res.code !== 0) throw new Error(`List chats error ${res.code}: ${res.msg}`);
    for (const c of res.data?.items || []) {
      results.push({ chatId: c.chat_id, name: c.name || c.chat_id, type: c.chat_type });
    }
    pageToken = res.data?.has_more ? res.data?.page_token : null;
  } while (pageToken);
  return results;
}

/**
 * Send a private message to a user by open_id using the app client.
 * Requires the client to be passed in to avoid circular dependency.
 */
async function sendPrivateMessage(client, openId, text) {
  const res = await client.im.message.create({
    data: { receive_id: openId, msg_type: 'text', content: JSON.stringify({ text }) },
    params: { receive_id_type: 'open_id' },
  });
  if (res.code !== 0) throw new Error(`sendPrivateMessage error ${res.code}: ${res.msg}`);
  return res;
}

module.exports = { readMessages, listAllChats, sendPrivateMessage };
