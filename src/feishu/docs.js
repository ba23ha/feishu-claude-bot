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
      let data = '';
      res.on('data', d => { data += d; });
      res.on('end', () => { try { resolve(JSON.parse(data)); } catch (e) { reject(e); } });
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
    pageToken = res.data?.page_token;
  } while (pageToken);

  return results;
}

/**
 * Read the content of a Feishu doc by token.
 * Returns the text content (blocks flattened to string).
 * @param {string} docToken
 * @returns {Promise<string>}
 */
async function readDoc(docToken) {
  if (!docToken) throw new Error('docToken is required');
  const client = getFeishuClient();

  // Try docx API first (newer format)
  try {
    const res = await client.docx.document.rawContent({
      path: { document_id: docToken },
    });
    if (res.code === 0) return res.data?.content || '';
  } catch {}

  // Fallback: try doc API (older format)
  try {
    const res = await client.doc.v2.rawContent({
      path: { docToken },
      params: { lang: 0 },
    });
    if (res.code === 0) return res.data?.content || '';
  } catch {}

  throw new Error(`Could not read doc: ${docToken}`);
}

module.exports = { readDoc, resolveWikiNode, readDocComments };
