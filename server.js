require('dotenv').config();
const { Client, EventDispatcher, WSClient, LoggerLevel } = require('@larksuiteoapi/node-sdk');
const { execFile } = require('child_process');
const fs = require('fs');
const path = require('path');

// ─── Skill 数据源配置（严格执行，所有 skill 基于此用户数据生成）────────────────
const SKILL_DATA_SOURCE = {
  openId: process.env.SKILL_DATA_SOURCE_OPENID,
  name:   process.env.SKILL_DATA_SOURCE_NAME || '指定用户',
};
if (!SKILL_DATA_SOURCE.openId) {
  console.error('❌ SKILL_DATA_SOURCE_OPENID 未配置，skill 功能不可用');
}

// ─── Paths ────────────────────────────────────────────────────────────────────
const DATA_DIR    = path.join(__dirname, 'data');
const HISTORY_DIR = path.join(DATA_DIR, 'history');
const USERS_DIR   = path.join(DATA_DIR, 'users');
const DOCS_DIR    = path.join(DATA_DIR, 'docs');
const EXPORT_DIR  = path.join(DATA_DIR, 'skills-export');
const SKILLS_DIR  = path.join(process.env.HOME, '.claude', 'skills');

[HISTORY_DIR, USERS_DIR, DOCS_DIR, EXPORT_DIR].forEach(d => fs.mkdirSync(d, { recursive: true }));

// ─── Feishu Client ────────────────────────────────────────────────────────────
const client = new Client({
  appId: process.env.FEISHU_APP_ID,
  appSecret: process.env.FEISHU_APP_SECRET,
  loggerLevel: LoggerLevel.error,
});

// ─── Chat History ─────────────────────────────────────────────────────────────
function loadHistory(openId) {
  try { return JSON.parse(fs.readFileSync(path.join(HISTORY_DIR, `${openId}.json`), 'utf8')); }
  catch { return []; }
}

function appendHistory(openId, role, content) {
  const history = loadHistory(openId);
  history.push({ role, content, timestamp: new Date().toISOString() });
  const trimmed = history.slice(-500);
  fs.writeFileSync(path.join(HISTORY_DIR, `${openId}.json`), JSON.stringify(trimmed, null, 2));
  return trimmed;
}

// ─── User Profile ─────────────────────────────────────────────────────────────
async function fetchUserProfile(openId) {
  const cacheFile = path.join(USERS_DIR, `${openId}.json`);
  try {
    const cached = JSON.parse(fs.readFileSync(cacheFile, 'utf8'));
    if (Date.now() - new Date(cached._cachedAt).getTime() < 3_600_000) return cached;
  } catch {}

  try {
    const res = await client.contact.user.get({
      path: { user_id: openId },
      params: { user_id_type: 'open_id' },
    });
    if (res.code === 0) {
      const profile = { ...res.data.user, _cachedAt: new Date().toISOString() };
      fs.writeFileSync(cacheFile, JSON.stringify(profile, null, 2));
      return profile;
    }
    console.warn('fetchUserProfile API error:', res.code, res.msg);
  } catch (e) {
    console.warn('fetchUserProfile error:', e.message);
  }
  return { open_id: openId, name: '未知用户', _cachedAt: new Date().toISOString() };
}

// ─── Feishu Docs ──────────────────────────────────────────────────────────────
async function fetchUserDocs(openId) {
  const cacheFile = path.join(DOCS_DIR, `${openId}.json`);
  try {
    const cached = JSON.parse(fs.readFileSync(cacheFile, 'utf8'));
    if (Date.now() - new Date(cached._cachedAt).getTime() < 3_600_000) return cached.docs;
  } catch {}

  const collected = [];
  try {
    // List recent docs accessible to the app
    const res = await client.drive.file.list({ params: { page_size: 50 } });
    if (res.code === 0 && res.data?.files) {
      collected.push(...res.data.files.map(f => ({
        name: f.name, type: f.type, token: f.token,
        created_time: f.created_time, modified_time: f.modified_time,
        owner_id: f.owner_id,
      })));
    }
  } catch (e) { console.warn('fetchDocs (drive) error:', e.message); }

  try {
    // Try Wiki spaces
    const res = await client.wiki.space.list({ params: { page_size: 20 } });
    if (res.code === 0 && res.data?.items) {
      for (const space of res.data.items) {
        collected.push({ name: space.name, type: 'wiki_space', token: space.space_id });
      }
    }
  } catch (e) { console.warn('fetchDocs (wiki) error:', e.message); }

  const result = { docs: collected, _cachedAt: new Date().toISOString() };
  fs.writeFileSync(cacheFile, JSON.stringify(result, null, 2));
  return collected;
}

// ─── Skill Generator ──────────────────────────────────────────────────────────
function runClaude(prompt, callback) {
  execFile(
    '/Users/lth/.npm-global/bin/claude',
    ['--dangerously-skip-permissions', '-p', prompt, '--output-format', 'text'],
    { timeout: 180_000, maxBuffer: 1024 * 1024 * 10 },
    callback
  );
}

async function collectUserData(openId) {
  const [profile, docs] = await Promise.all([
    fetchUserProfile(openId),
    fetchUserDocs(openId),
  ]);
  const history = loadHistory(openId);
  return { profile, docs, history };
}

async function generateSkill(openId, skillName, extraContext) {
  const { profile, docs, history } = await collectUserData(openId);

  const profileSummary = JSON.stringify({
    name: profile.name,
    en_name: profile.en_name,
    department: profile.department,
    job_title: profile.job_title,
    email: profile.email,
    mobile: profile.mobile,
    city: profile.city,
    description: profile.description,
    custom_attrs: profile.custom_attrs,
  }, null, 2);

  const historySummary = history.length > 0
    ? history.slice(-100).map(h => `[${h.role}] ${h.content}`).join('\n')
    : '暂无历史记录';

  const docsSummary = docs.length > 0
    ? docs.map(d => `- [${d.type}] ${d.name}`).join('\n')
    : '无可访问文档（可能需要 drive:drive:readonly 权限）';

  const prompt = `你是 Claude Code skill 生成专家。

请基于以下飞书用户的真实数据，生成一个专属 skill 文件（SKILL.md 格式），skill 名称为「${skillName}」。

## 用户基本信息
${profileSummary}

## 用户与 bot 历史对话（最近100条）
${historySummary}

## 用户的飞书文档/Wiki 列表
${docsSummary}

## 额外补充信息
${extraContext || '无'}

## 输出格式要求
严格按以下 SKILL.md 格式输出，不要包含任何额外说明：

---
name: ${skillName}
description: "（一句话描述：这个 skill 针对该用户的核心使用场景）"
---

# （Skill 标题）

（基于用户真实数据生成的 skill 内容：
- 用户的角色和职责背景
- 用户的常用任务和行为模式（从历史对话中提炼）
- 推荐的协作方式和注意事项
- 具体的提示词/行为指令，让 AI 更好地服务该用户
）`;

  return new Promise((resolve, reject) => {
    runClaude(prompt, (err, stdout) => {
      if (err) return reject(err);
      resolve(stdout.trim());
    });
  });
}

async function saveSkill(skillName, content, openId) {
  // Save to Claude Code skills dir
  const claudeSkillDir = path.join(SKILLS_DIR, skillName);
  fs.mkdirSync(claudeSkillDir, { recursive: true });
  const claudeSkillFile = path.join(claudeSkillDir, 'SKILL.md');
  fs.writeFileSync(claudeSkillFile, content);

  // Also export as JSON for other bots to consume
  const exportFile = path.join(EXPORT_DIR, `${skillName}.json`);
  fs.writeFileSync(exportFile, JSON.stringify({
    name: skillName,
    owner_open_id: openId,
    created_at: new Date().toISOString(),
    content,
  }, null, 2));

  return { claudeSkillFile, exportFile };
}

// ─── Command Handlers ─────────────────────────────────────────────────────────
async function handleCreateSkill(senderOpenId, chatId, args) {
  // 强制原则：所有 skill 数据源锁定为 SKILL_DATA_SOURCE，忽略 --user 参数及发送者身份
  if (!SKILL_DATA_SOURCE.openId) {
    await sendMessage(chatId, '❌ 未配置 SKILL_DATA_SOURCE_OPENID，无法生成 skill。');
    return;
  }
  const openId = SKILL_DATA_SOURCE.openId;  // 始终使用郑伟的数据
  const cleanArgs = args.replace(/--user\s+\S+/, '').trim();
  const parts = cleanArgs.split(/\s+/);
  const skillName = parts[0];
  const extraContext = parts.slice(1).join(' ');

  if (!skillName) {
    await sendMessage(chatId,
      '用法：\n' +
      '  /create-skill <名称> [描述]                    → 为自己创建\n' +
      '  /create-skill <名称> --user <openId> [描述]   → 为指定用户创建\n\n' +
      '例：/create-skill 产品助手 --user ou_xxxxxx 专注需求分析'
    );
    return;
  }

  await sendMessage(chatId, `⏳ 正在采集 ${SKILL_DATA_SOURCE.name} 的飞书数据（个人信息、对话历史、文档列表）...`);

  try {
    const content = await generateSkill(openId, skillName, extraContext);
    const { claudeSkillFile, exportFile } = await saveSkill(skillName, content, openId);

    const preview = content.length > 600 ? content.slice(0, 600) + '\n...' : content;
    await sendMessage(chatId,
      `✅ Skill「${skillName}」已生成！\n` +
      `📌 数据来源：${SKILL_DATA_SOURCE.name}（${SKILL_DATA_SOURCE.openId}）\n\n` +
      `📁 Claude Code 路径：${claudeSkillFile}\n` +
      `📦 其他 bot 读取：${exportFile}\n\n` +
      `─── 预览 ───\n${preview}`
    );
    console.log(`[skill created] ${skillName} by ${openId}`);
  } catch (err) {
    await sendMessage(chatId, `❌ 生成 skill 失败：${err.message}`);
    console.error('[skill error]', err);
  }
}

function wrapWithThinking(userText) {
  return `请先在 <thinking> 标签内展示你的思考过程（分析问题、拆解步骤、权衡方案），然后给出最终答案。

格式要求：
<thinking>
（思考过程）
</thinking>
（最终回答，不含任何标签）

用户的问题/任务：
${userText}`;
}

function parseThinkingOutput(raw) {
  const thinkMatch = raw.match(/<thinking>([\s\S]*?)<\/thinking>/i);
  if (!thinkMatch) return { thinking: null, answer: raw.trim() };
  const thinking = thinkMatch[1].trim();
  const answer = raw.slice(raw.indexOf('</thinking>') + '</thinking>'.length).trim();
  return { thinking, answer };
}

async function handleRegularMessage(openId, chatId, userText) {
  appendHistory(openId, 'user', userText);
  await sendMessage(chatId, '⏳ 正在思考，请稍候...');

  const prompt = wrapWithThinking(userText);

  runClaude(prompt, async (err, stdout) => {
    if (err) {
      const msg = err.killed ? '⚠️ 执行超时（>3分钟）' : `⚠️ 出错: ${err.message}`;
      await sendMessage(chatId, msg);
      return;
    }

    const raw = (stdout || '').trim() || '（无输出）';
    const { thinking, answer } = parseThinkingOutput(raw);

    // 发思考过程
    if (thinking) {
      const thinkingMsg = `🧠 思考过程：\n\n${thinking.length > 1800 ? thinking.slice(0, 1800) + '\n…（已截断）' : thinking}`;
      await sendMessage(chatId, thinkingMsg);
    }

    // 发最终回答
    const reply = answer.length > 3800 ? answer.slice(0, 3800) + '\n…（已截断）' : answer;
    await sendMessage(chatId, `💬 回答：\n\n${reply}`);

    appendHistory(openId, 'assistant', answer);
    console.log(`[${new Date().toISOString()}] Done (thinking: ${!!thinking})`);
  });
}

// ─── Send Message ─────────────────────────────────────────────────────────────
async function sendMessage(chatId, text) {
  try {
    await client.im.message.create({
      data: { receive_id: chatId, msg_type: 'text', content: JSON.stringify({ text }) },
      params: { receive_id_type: 'chat_id' },
    });
  } catch (err) { console.error('Send failed:', err.message); }
}

// ─── Event Dispatcher ─────────────────────────────────────────────────────────
const processedMsgIds = new Set();

const dispatcher = new EventDispatcher({}).register({
  'im.message.receive_v1': async (data) => {
    const msg = data.message;
    if (!msg || msg.message_type !== 'text') return;

    if (processedMsgIds.has(msg.message_id)) return;
    processedMsgIds.add(msg.message_id);
    if (processedMsgIds.size > 1000) processedMsgIds.delete(processedMsgIds.values().next().value);

    let userText;
    try { userText = JSON.parse(msg.content).text.replace(/^@\S+\s*/, '').trim(); }
    catch { return; }
    if (!userText) return;

    const senderOpenId = data.sender?.sender_id?.open_id;
    const chatId = msg.chat_id;

    // 提取 @提及 的用户列表，key 如 @_user_1 → open_id
    const mentions = {};
    if (Array.isArray(msg.mentions)) {
      for (const m of msg.mentions) {
        if (m.key && m.id?.open_id) {
          mentions[m.key] = { open_id: m.id.open_id, name: m.name };
          console.log(`[mention] ${m.name}: ${m.id.open_id}`);
        }
      }
    }

    // 存储提及用户信息，方便后续 skill 生成使用
    if (Object.keys(mentions).length > 0) {
      const mentionFile = path.join(DATA_DIR, 'last_mentions.json');
      fs.writeFileSync(mentionFile, JSON.stringify({ mentions, updatedAt: new Date().toISOString() }, null, 2));
    }

    const openId = senderOpenId;
    console.log(`[${new Date().toISOString()}] ${openId}: ${userText}`);

    if (userText.startsWith('/create-skill')) {
      await handleCreateSkill(openId, chatId, userText.slice('/create-skill'.length).trim());
    } else {
      await handleRegularMessage(openId, chatId, userText);
    }
  },
});

// ─── Start ────────────────────────────────────────────────────────────────────
const wsClient = new WSClient({
  appId: process.env.FEISHU_APP_ID,
  appSecret: process.env.FEISHU_APP_SECRET,
  loggerLevel: LoggerLevel.error,
});

console.log('🚀 Starting Feishu-Claude bridge...');
wsClient.start({ eventDispatcher: dispatcher });
console.log('✅ Connected to Feishu via WebSocket');
