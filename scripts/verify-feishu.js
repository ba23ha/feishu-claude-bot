#!/usr/bin/env node
/**
 * Verify Feishu + Anthropic API connectivity.
 *
 * Usage:
 *   node scripts/verify-feishu.js
 *   node scripts/verify-feishu.js --chat=oc_xxx --days=7
 *   node scripts/verify-feishu.js --doc=xxxtoken
 *   node scripts/verify-feishu.js --minutes
 */
require('dotenv').config();

const args = Object.fromEntries(
  process.argv.slice(2)
    .filter(a => a.startsWith('--'))
    .map(a => {
      const [k, v] = a.slice(2).split('=');
      return [k, v === undefined ? true : v];
    })
);

let passed = 0;
let failed = 0;

function ok(label, detail = '') {
  passed++;
  console.log(`  ✅ ${label}${detail ? '  ' + detail : ''}`);
}

function fail(label, err) {
  failed++;
  console.log(`  ❌ ${label}`);
  console.log(`     ${err?.message || err}`);
}

async function checkEnv() {
  console.log('\n── 1. 环境变量 ──────────────────────────────');
  const required = [
    ['FEISHU_APP_ID', /^cli_/],
    ['FEISHU_APP_SECRET', /.{8}/],
    ['BOSS_OPEN_ID', /^ou_/],
  ];
  for (const [key, pattern] of required) {
    const val = process.env[key];
    if (!val) fail(key, new Error('未设置'));
    else if (!pattern.test(val)) fail(key, new Error(`格式异常: ${val.slice(0, 8)}...`));
    else ok(key, `(${val.slice(0, 8)}...)`);
  }
  const optional = ['PORT'];
  for (const key of optional) {
    const val = process.env[key];
    console.log(`  ℹ️  ${key} = ${val || '(未设置，使用默认值)'}`);
  }
}

async function checkFeishuAuth() {
  console.log('\n── 2. Feishu 应用认证 ────────────────────────');
  try {
    const { getFeishuClient } = require('../src/feishu/client');
    const client = getFeishuClient();

    // Call bot info as a lightweight auth check
    let apiCode = 0;
    try {
      const res = await client.im.message.list({
        params: { container_id_type: 'chat', container_id: 'placeholder', page_size: 1 },
      });
      apiCode = res.code;
    } catch (sdkErr) {
      // SDK throws on HTTP 4xx; extract the API code from the error payload
      const payload = Array.isArray(sdkErr) ? sdkErr[1] : sdkErr?.response?.data;
      apiCode = payload?.code ?? -1;
    }
    // Auth-failure codes (invalid app_id / app_secret)
    const authFailCodes = new Set([99991668, 99991663, 99991664, 10012, 10013]);
    if (authFailCodes.has(apiCode)) {
      fail('Feishu 认证', new Error(`Token 无效 (${apiCode})`));
    } else {
      // 230001 = invalid param, 230002 = chat not found — both mean auth passed
      ok('Feishu 认证', `应用 ${process.env.FEISHU_APP_ID} (code=${apiCode})`);
    }
    return client;
  } catch (err) {
    fail('Feishu 认证', err);
    return null;
  }
}

async function checkUserResolver() {
  console.log('\n── 3. 用户名解析 ─────────────────────────────');
  const targetId = process.env.BOSS_OPEN_ID || process.env.SKILL_DATA_SOURCE_OPENID;
  if (!targetId) { fail('用户解析', new Error('BOSS_OPEN_ID 未设置')); return; }
  try {
    const { resolveUser } = require('../src/feishu/resolver');
    const name = await resolveUser(targetId);
    if (name.startsWith('unknown_user')) {
      fail('用户解析', new Error(`无法解析 ${targetId} → ${name}（可能缺少 contact:contact.base:readonly 权限）`));
    } else {
      ok('用户解析', `${targetId.slice(-6)} → "${name}"`);
    }
  } catch (err) {
    fail('用户解析', err);
  }
}

async function checkMessages() {
  if (!args.chat) return;
  console.log('\n── 4. 群消息读取 ─────────────────────────────');
  try {
    const { readMessages } = require('../src/feishu/messages');
    const days = parseInt(args.days || '7', 10);
    const endMs = Date.now();
    const startMs = endMs - days * 24 * 60 * 60 * 1000;
    const msgs = await readMessages({ chatId: args.chat, startMs, endMs, maxCount: 5 });
    ok(`群消息 (${args.chat.slice(-6)})`, `过去 ${days} 天，取样 ${msgs.length} 条`);
    if (msgs.length > 0) {
      console.log(`     最新一条 [${msgs[msgs.length - 1].timestamp.slice(0, 10)}]: ${msgs[msgs.length - 1].text.slice(0, 60)}...`);
    }
  } catch (err) {
    fail('群消息读取', err);
  }
}

async function checkDoc() {
  if (!args.doc) return;
  console.log('\n── 5. 文档读取 ───────────────────────────────');
  try {
    const { readDoc } = require('../src/feishu/docs');
    const content = await readDoc(args.doc);
    ok(`文档 (${args.doc.slice(-8)})`, `${content.length} 字符`);
    console.log(`     预览: ${content.slice(0, 80).replace(/\n/g, ' ')}...`);
  } catch (err) {
    fail('文档读取', err);
  }
}

async function checkMinutes() {
  if (!args.minutes) return;
  console.log('\n── 6. 妙记列表 ───────────────────────────────');
  try {
    const { listMinutes } = require('../src/feishu/minutes');
    const list = await listMinutes(5);
    ok(`妙记列表`, `${list.length} 条`);
    list.forEach(m => console.log(`     • ${m.startTime.slice(0, 10)} ${m.topic}`));
  } catch (err) {
    fail('妙记列表', err);
  }
}

async function checkClaude() {
  console.log('\n── 7. Claude CLI (LLM) ───────────────────────');
  try {
    const { generate } = require('../src/llm/client');
    const result = await generate('你是测试助手，只回复一个词。', '回复：OK', { timeoutMs: 30000 });
    ok('Claude CLI', `响应: "${result.slice(0, 60)}"`);
  } catch (err) {
    fail('Claude CLI', err);
  }
}

async function main() {
  console.log('🔍 Feishu + Anthropic 连接验证');
  console.log('================================');

  await checkEnv();
  await checkFeishuAuth();
  await checkUserResolver();
  await checkMessages();
  await checkDoc();
  await checkMinutes();
  await checkClaude();

  console.log('\n================================');
  console.log(`结果: ${passed} 通过 / ${failed} 失败`);

  if (failed > 0) {
    console.log('\n常见修复：');
    console.log('  • 缺少环境变量    → 编辑 .env 填入真实值');
    console.log('  • 用户解析失败    → 在飞书开发平台启用 contact:user.base:readonly 权限');
    console.log('  • 消息读取 403   → 将机器人拉入目标群聊，并启用 im:message:readonly');
    console.log('  • 妙记 403       → 在飞书开发平台启用 minutes:read 权限');
    process.exit(1);
  }
}

main().catch(err => { console.error(err); process.exit(1); });
