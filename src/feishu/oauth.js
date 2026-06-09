require('dotenv').config();
const fs = require('fs');
const path = require('path');
const https = require('https');

const TOKEN_FILE = path.join(__dirname, '..', '..', 'data', 'boss-token.json');

// ── Token persistence ─────────────────────────────────────────────────────────

function loadTokens() {
  try { return JSON.parse(fs.readFileSync(TOKEN_FILE, 'utf8')); }
  catch { return null; }
}

function saveTokens(tokens) {
  fs.mkdirSync(path.dirname(TOKEN_FILE), { recursive: true });
  fs.writeFileSync(TOKEN_FILE, JSON.stringify(tokens, null, 2));
  console.log(`[oauth] tokens saved to ${TOKEN_FILE}`);
}

function isExpired(tokens) {
  if (!tokens?.expiresAt) return true;
  return Date.now() >= tokens.expiresAt - 60_000; // 1 min buffer
}

// ── HTTP helper ───────────────────────────────────────────────────────────────

function httpsPost(urlPath, body, headers = {}) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const req = https.request({
      hostname: 'open.feishu.cn',
      path: urlPath,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': Buffer.byteLength(data),
        ...headers,
      },
    }, res => {
      let buf = '';
      res.on('data', d => buf += d);
      res.on('end', () => {
        try { resolve(JSON.parse(buf)); }
        catch { reject(new Error('Invalid JSON from Feishu')); }
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

// ── App access token (needed to exchange user code) ───────────────────────────

async function getAppAccessToken() {
  const res = await httpsPost('/open-apis/auth/v3/app_access_token/internal', {
    app_id: process.env.FEISHU_APP_ID,
    app_secret: process.env.FEISHU_APP_SECRET,
  });
  if (res.code !== 0) throw new Error(`App token error (${res.code}): ${res.msg}`);
  return res.app_access_token;
}

// ── Auth URL ──────────────────────────────────────────────────────────────────

function getAuthUrl() {
  const appId = process.env.FEISHU_APP_ID;
  const redirectUri = encodeURIComponent(
    process.env.FEISHU_REDIRECT_URI || 'http://localhost:3000/oauth/callback'
  );
  // Scopes: list chats + read messages + resolve user names
  const scope = encodeURIComponent([
    'im:chat:readonly',
    'im:message:readonly',
    'contact:contact.base:readonly',
  ].join(' '));
  return `https://open.feishu.cn/open-apis/authen/v1/authorize`
    + `?app_id=${appId}&redirect_uri=${redirectUri}&scope=${scope}&state=boss-distill`;
}

// ── Code → Token exchange ─────────────────────────────────────────────────────

async function exchangeCode(code) {
  const appToken = await getAppAccessToken();
  const res = await httpsPost(
    '/open-apis/authen/v1/oidc/access_token',
    { grant_type: 'authorization_code', code },
    { Authorization: `Bearer ${appToken}` }
  );
  if (res.code !== 0) throw new Error(`OAuth exchange error (${res.code}): ${res.msg}`);

  const tokens = {
    accessToken: res.data.access_token,
    refreshToken: res.data.refresh_token,
    tokenType: res.data.token_type,
    expiresAt: Date.now() + (res.data.expires_in || 7200) * 1000,
    refreshExpiresAt: Date.now() + (res.data.refresh_expires_in || 2592000) * 1000,
    authorizedAt: new Date().toISOString(),
  };
  saveTokens(tokens);
  return tokens;
}

// ── Refresh ───────────────────────────────────────────────────────────────────

async function refreshAccessToken() {
  const tokens = loadTokens();
  if (!tokens?.refreshToken) throw new Error('No refresh token — need to re-authorize');
  if (tokens.refreshExpiresAt && Date.now() >= tokens.refreshExpiresAt) {
    throw new Error('Refresh token expired — need to re-authorize');
  }

  const appToken = await getAppAccessToken();
  const res = await httpsPost(
    '/open-apis/authen/v1/oidc/refresh_access_token',
    { grant_type: 'refresh_token', refresh_token: tokens.refreshToken },
    { Authorization: `Bearer ${appToken}` }
  );
  if (res.code !== 0) throw new Error(`Refresh error (${res.code}): ${res.msg}`);

  const updated = {
    ...tokens,
    accessToken: res.data.access_token,
    refreshToken: res.data.refresh_token || tokens.refreshToken,
    expiresAt: Date.now() + (res.data.expires_in || 7200) * 1000,
    refreshedAt: new Date().toISOString(),
  };
  saveTokens(updated);
  return updated;
}

// ── Get valid access token (auto-refresh) ─────────────────────────────────────

async function getValidToken() {
  let tokens = loadTokens();
  if (!tokens) throw new Error('未授权 — 请先运行: node cli-boss.js auth-url');
  if (isExpired(tokens)) {
    console.log('[oauth] access token expired, refreshing...');
    tokens = await refreshAccessToken();
  }
  return tokens.accessToken;
}

function hasValidAuth() {
  const tokens = loadTokens();
  return !!(tokens?.refreshToken);
}

module.exports = { getAuthUrl, exchangeCode, getValidToken, hasValidAuth };
