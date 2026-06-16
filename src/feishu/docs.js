const https = require('https');
const { getFeishuClient } = require('./client');
const { getValidToken } = require('./oauth');

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
 * Resolve a wiki page token to the underlying document token + type.
 * @param {string} wikiToken
 * @returns {Promise<{objToken: string, objType: string}>}
 */
async function resolveWikiNode(wikiToken) {
  const token = await getValidToken();
  const res = await httpsGet(
    `/open-apis/wiki/v2/spaces/get_node?token=${wikiToken}&obj_type=wiki`,
    token
  );
  if (res.code !== 0) throw new Error(`Wiki node API error ${res.code}: ${res.msg}`);
  const node = res.data?.node;
  if (!node) throw new Error('Wiki node not found');
  return { objToken: node.obj_token, objType: node.obj_type };
}

/**
 * Read comments on a Feishu document, optionally filtered by author open_id.
 * Returns array of { authorId, content, createdAt }.
 * @param {string} fileToken   Document token (obj_token from wiki)
 * @param {string} fileType    'docx' | 'doc'
 * @param {string} [authorId]  Filter to specific author open_id
 */
async function readDocComments(fileToken, fileType = 'docx', authorId = null) {
  const token = await getValidToken();
  const results = [];
  let pageToken;

  do {
    let qs = `file_type=${fileType}&page_size=50`;
    if (pageToken) qs += `&page_token=${encodeURIComponent(pageToken)}`;
    const res = await httpsGet(
      `/open-apis/drive/v1/files/${fileToken}/comments?${qs}`,
      token
    );
    if (res.code !== 0) throw new Error(`Comments API error ${res.code}: ${res.msg}`);

    for (const comment of res.data?.items || []) {
      for (const reply of comment.reply_list?.replies || []) {
        const replyUid = typeof reply.user_id === 'string' ? reply.user_id : (reply.user_id?.open_id || reply.user_id?.user_id || '');
        if (authorId && replyUid !== authorId) continue;
        const text = (reply.content?.elements || [])
          .map(e => e.text_run?.text || '')
          .join('')
          .trim();
        if (text) {
          results.push({
            authorId: reply.user_id?.open_id,
            content: text,
            createdAt: new Date(reply.create_time * 1000).toISOString(),
          });
        }
      }
    }
    pageToken = res.data?.has_more ? res.data?.page_token : null;
  } while (pageToken);

  return results;
}

/**
 * Read the content of a Feishu doc by token.
 * Uses user OAuth token (requires docx:document:readonly scope).
 * @param {string} docToken
 * @returns {Promise<string>}
 */
async function readDoc(docToken) {
  if (!docToken) throw new Error('docToken is required');
  const token = await getValidToken();

  // Try docx raw_content with user token
  const res = await httpsGet(
    `/open-apis/docx/v1/documents/${docToken}/raw_content`,
    token
  );
  if (res.code === 0) return res.data?.content || '';

  throw new Error(`Could not read doc: ${docToken} (code ${res.code}: ${res.msg})`);
}

/**
 * Write a single inline comment to a Feishu document using the boss's OAuth token.
 * Falls back gracefully if the API doesn't support quote-based inline comments.
 *
 * @param {string} fileToken   Document token
 * @param {string} fileType    'docx' | 'doc'
 * @param {string} commentText The comment body text
 * @param {string} [quoteText] The selected text to highlight (inline anchor)
 * @returns {Promise<{success: boolean, commentId?: string, error?: string}>}
 */
async function writeDocComment(fileToken, fileType = 'docx', commentText, quoteText) {
  const token = await getValidToken();

  const body = {
    content: {
      elements: [{ type: 'text_run', text_run: { text: commentText } }],
    },
  };
  if (quoteText) body.quote = quoteText;

  const bodyStr = JSON.stringify(body);

  return new Promise((resolve) => {
    const req = https.request({
      hostname: 'open.feishu.cn',
      path: `/open-apis/drive/v1/files/${fileToken}/comments?file_type=${fileType}`,
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(bodyStr),
      },
    }, res => {
      const chunks = [];
      res.on('data', d => chunks.push(d));
      res.on('end', () => {
        try {
          const parsed = JSON.parse(Buffer.concat(chunks).toString('utf8'));
          if (parsed.code === 0) {
            resolve({ success: true, commentId: parsed.data?.comment?.comment_id });
          } else {
            resolve({ success: false, error: `API ${parsed.code}: ${parsed.msg}` });
          }
        } catch (e) {
          resolve({ success: false, error: e.message });
        }
      });
    });
    req.on('error', e => resolve({ success: false, error: e.message }));
    req.write(bodyStr);
    req.end();
  });
}

module.exports = { readDoc, resolveWikiNode, readDocComments, writeDocComment };
