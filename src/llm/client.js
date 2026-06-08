require('dotenv').config();
const Anthropic = require('@anthropic-ai/sdk');

let _client = null;

function getClient() {
  if (!_client) {
    if (!process.env.ANTHROPIC_API_KEY) throw new Error('ANTHROPIC_API_KEY not set');
    _client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
  }
  return _client;
}

const DEFAULT_MODEL = process.env.ANTHROPIC_MODEL || 'claude-opus-4-8';
const MAX_TOKENS = 2048;

async function generate(systemPrompt, userMessage, opts = {}) {
  const client = getClient();
  const response = await client.messages.create({
    model: opts.model || DEFAULT_MODEL,
    max_tokens: opts.maxTokens || MAX_TOKENS,
    system: systemPrompt,
    messages: [{ role: 'user', content: userMessage }],
  });
  return response.content[0].text;
}

module.exports = { generate };
