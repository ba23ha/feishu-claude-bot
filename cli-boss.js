// cli-boss.js — local CLI for Boss Copilot (no Feishu interaction needed)
//
// Task commands:
//   node cli-boss.js reply   "背景：对方催进度，我想说延期"
//   node cli-boss.js polish  "大家一起看下这个事情能不能做"
//   node cli-boss.js review  "方案文本..."
//   node cli-boss.js meeting "会议纪要文本..."
//   node cli-boss.js auto    "帮我润色一下这段话：xxx"
//
// Distill commands (reads Feishu data → appends to boss-soul):
//   node cli-boss.js distill --file=style --chat=oc_xxx --days=90 --reason=提炼沟通风格
//   node cli-boss.js distill --file=decision --doc=xxxtoken --reason=提炼决策原则
//   node cli-boss.js distill --file=style --chat=oc_xxx --days=30 --yes   (skip confirm)
//
// List accessible chats (to find group IDs):
//   node cli-boss.js list-chats

require('dotenv').config();
const readline = require('readline');
const { handleTask } = require('./src/bot/handler');
const { detectTaskType } = require('./src/bot/router');
const { distill, parseDistillCommand } = require('./src/soul/updater');
const { dryRun, formatDryRunMessage } = require('./src/audit/dry-run');
const { createAuditContext } = require('./src/audit/runner');
const { generateReport } = require('./src/audit/report');

const args = process.argv.slice(2);
const taskArg = args[0];

function parseFlags(argv) {
  const flags = { _: [] };
  for (const a of argv) {
    if (a.startsWith('--')) {
      const [k, v] = a.slice(2).split('=');
      flags[k] = v === undefined ? true : v;
    } else {
      flags._.push(a);
    }
  }
  return flags;
}

function confirm(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => {
    rl.question(question, ans => { rl.close(); resolve(ans.trim()); });
  });
}

async function runDistill(argv) {
  const flags = parseFlags(argv);
  const rawCommand = 'distill ' + argv.join(' ');
  const opts = parseDistillCommand(rawCommand);

  if (!opts.targetFile) {
    console.error('\n❌ 必须指定 --file，例如：');
    console.error('   node cli-boss.js distill --file=style --chat=oc_xxx --days=90 --reason=提炼沟通风格\n');
    console.error('可选 --file 值：identity | style | decision | communication | taboos | examples');
    process.exit(1);
  }

  if (!opts.chatId && !opts.docToken && !opts.minutesToken) {
    console.error('\n❌ 必须指定数据来源：--chat=oc_xxx 或 --doc=token 或 --minutes=token\n');
    process.exit(1);
  }

  console.log('\n=== 蒸馏干跑预览 ===\n');
  console.log('正在扫描数据范围（不读取内容）...\n');

  let preview;
  try {
    preview = await dryRun(opts);
  } catch (err) {
    console.error('❌ 干跑失败：', err.message);
    process.exit(1);
  }

  // Print dry-run result to terminal
  const previewText = formatDryRunMessage(preview);
  console.log(previewText.replace(/回复「确认」执行，或「取消」中止。（5 分钟内有效）/, ''));

  if (flags.yes || flags.y) {
    console.log('（--yes 跳过确认）\n');
  } else {
    const ans = await confirm('确认读取以上数据并更新 soul 文件？(y/N) ');
    if (!/^y(es)?$/i.test(ans)) {
      console.log('\n已取消，未读取任何数据。\n');
      process.exit(0);
    }
  }

  console.log('\n⏳ 开始读取并蒸馏...\n');

  try {
    const operator = process.env.SKILL_DATA_SOURCE_NAME || 'cli-operator';
    const auditContext = createAuditContext(opts, operator, preview.runId);
    const summary = await distill(opts, auditContext);
    const reportPath = generateReport(auditContext);

    console.log('\n' + summary);
    console.log(`\n📋 审计报告：${reportPath}\n`);
  } catch (err) {
    console.error('\n❌ 蒸馏失败：', err.message);
    process.exit(1);
  }
}

async function showAuthUrl() {
  const { getAuthUrl, hasValidAuth } = require('./src/feishu/oauth');
  if (hasValidAuth()) {
    console.log('\n✅ 郑伟已授权，user token 有效。\n');
    console.log('如需重新授权，删除 data/boss-token.json 后再运行此命令。\n');
    return;
  }
  const url = getAuthUrl();
  console.log('\n=== 郑伟飞书授权 ===\n');
  console.log('步骤：');
  console.log('  1. 将以下链接发给郑伟，让他在浏览器中打开');
  console.log('  2. 他登录飞书账号并点击「授权」');
  console.log('  3. 浏览器会跳转到 localhost（可能显示无法访问，这是正常的）');
  console.log('  4. 复制浏览器地址栏中 ?code= 后面的值');
  console.log('  5. 运行：node cli-boss.js auth-callback <code>\n');
  console.log('授权链接：');
  console.log(url);
  console.log();
}

async function handleAuthCallback(code) {
  if (!code) {
    console.error('用法：node cli-boss.js auth-callback <code>');
    process.exit(1);
  }
  const { exchangeCode } = require('./src/feishu/oauth');
  console.log('\n⏳ 正在交换授权码...\n');
  try {
    await exchangeCode(code);
    console.log('✅ 授权成功！user token 已保存到 data/boss-token.json');
    console.log('\n现在可以读取郑伟所在的所有群聊消息了。\n');
    console.log('运行以下命令查看可访问的群聊：');
    console.log('  node cli-boss.js list-chats\n');
  } catch (err) {
    console.error('❌ 授权失败：', err.message);
    process.exit(1);
  }
}

async function listChats() {
  const https = require('https');
  const { getValidToken, hasValidAuth } = require('./src/feishu/oauth');

  if (!hasValidAuth()) {
    console.log('⚠️  未授权，运行 auth-url 完成授权后可查看郑伟所有群。\n');
    return;
  }

  const token = await getValidToken();
  console.log('\n=== 郑伟所在的所有群聊 ===\n');

  const fetchPage = (pageToken) => new Promise((resolve, reject) => {
    const qs = `page_size=50${pageToken ? `&page_token=${pageToken}` : ''}`;
    const req = https.request({
      hostname: 'open.feishu.cn',
      path: `/open-apis/im/v1/chats?${qs}`,
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` },
    }, res => {
      let data = '';
      res.on('data', d => { data += d; });
      res.on('end', () => resolve(JSON.parse(data)));
    });
    req.on('error', reject);
    req.end();
  });

  try {
    let pageToken;
    let total = 0;
    do {
      const res = await fetchPage(pageToken);
      if (res.code !== 0) { console.error(`API error ${res.code}: ${res.msg}`); return; }
      const chats = res.data?.items || [];
      chats.forEach(c => console.log(`  ${c.chat_id}  ${c.name || '（无名群）'}`));
      total += chats.length;
      pageToken = res.data?.page_token;
    } while (pageToken);
    console.log(`\n共 ${total} 个群聊\n`);
  } catch (err) {
    console.error('获取群列表失败：', err.message);
  }
}

async function main() {
  if (!taskArg) {
    console.log('用法：');
    console.log('  node cli-boss.js <reply|polish|review|meeting|auto> "<输入>"');
    console.log('  node cli-boss.js distill --file=style --chat=oc_xxx --days=90 --reason=xxx');
    console.log('  node cli-boss.js auth-url              生成郑伟授权链接');
    console.log('  node cli-boss.js auth-callback <code>  完成授权');
    console.log('  node cli-boss.js list-chats            查看可访问群聊');
    process.exit(1);
  }

  if (taskArg === 'distill') { await runDistill(args.slice(1)); return; }
  if (taskArg === 'list-chats') { await listChats(); return; }
  if (taskArg === 'auth-url') { await showAuthUrl(); return; }
  if (taskArg === 'auth-callback') { await handleAuthCallback(args[1]); return; }

  const VALID_TYPES = ['reply', 'polish', 'review', 'meeting', 'general', 'auto'];
  if (!VALID_TYPES.includes(taskArg)) {
    console.error(`未知命令：${taskArg}`);
    process.exit(1);
  }

  const input = args.slice(1).join(' ');
  if (!input.trim()) { console.error('Error: 输入不能为空'); process.exit(1); }

  const taskType = taskArg === 'auto' ? detectTaskType(input) : taskArg;
  if (taskArg === 'auto') console.log(`[自动识别任务类型：${taskType}]`);

  console.log(`\n=== Boss Copilot CLI ===`);
  console.log(`任务：${taskType}`);
  console.log(`输入：${input}\n`);
  console.log('生成中...\n');

  try {
    const result = await handleTask(taskType, input);
    console.log('--- 回复 ---\n');
    console.log(result);
    console.log('\n---');
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

main();
