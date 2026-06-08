const { getFeishuClient } = require('./client');

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

module.exports = { readDoc };
