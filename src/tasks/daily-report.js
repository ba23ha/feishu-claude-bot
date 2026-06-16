const { listAllChats, readMessages } = require('../feishu/messages');
const { readDoc } = require('../feishu/docs');
const { buildSystemPrompt, loadSkill } = require('../soul/loader');
const { generate } = require('../llm/client');

/**
 * Collect today's messages from all of boss's active chats.
 * Returns array of { chatName, messages[] }.
 */
async function collectTodayMessages() {
  const now = new Date();
  const midnight = new Date(now);
  midnight.setHours(0, 0, 0, 0);
  const startMs = midnight.getTime();
  const endMs = now.getTime();

  const chats = await listAllChats();
  console.log(`[daily-report] found ${chats.length} chats, pulling today's messages...`);

  const active = [];
  for (const chat of chats) {
    try {
      const messages = await readMessages({ chatId: chat.chatId, startMs, endMs, maxCount: 100 });
      if (messages.length > 0) {
        active.push({ chatName: chat.name, messages });
      }
    } catch (e) {
      console.warn(`[daily-report] skip chat ${chat.chatId}: ${e.message}`);
    }
  }
  return active;
}

/**
 * Optionally read supplementary docs from DAILY_REPORT_DOCS env.
 */
async function collectDocs() {
  const tokens = (process.env.DAILY_REPORT_DOCS || '').split(',').map(s => s.trim()).filter(Boolean);
  const docs = [];
  for (const token of tokens) {
    try {
      const content = await readDoc(token);
      if (content) docs.push({ token, content: content.slice(0, 2000) });
    } catch (e) {
      console.warn(`[daily-report] skip doc ${token}: ${e.message}`);
    }
  }
  return docs;
}

/**
 * Build the user prompt from collected data.
 */
function buildPrompt(chatGroups, docs, date) {
  const lines = [`今天是 ${date}，请根据以下群聊内容生成日报。\n`];

  for (const { chatName, messages } of chatGroups) {
    lines.push(`【${chatName}】`);
    for (const m of messages) {
      lines.push(`${m.timestamp.slice(11, 16)} ${m.text}`);
    }
    lines.push('');
  }

  if (docs.length > 0) {
    lines.push('【补充文档】');
    for (const d of docs) {
      lines.push(d.content);
      lines.push('');
    }
  }

  return lines.join('\n');
}

/**
 * Run the full daily report pipeline.
 * @param {Function} sendFn  async (text) => void — sends to boss
 */
async function runDailyReport(sendFn) {
  const date = new Date().toLocaleDateString('zh-CN', { month: 'long', day: 'numeric', weekday: 'short' });
  console.log(`[daily-report] starting for ${date}`);

  const [chatGroups, docs] = await Promise.all([collectTodayMessages(), collectDocs()]);

  if (chatGroups.length === 0 && docs.length === 0) {
    await sendFn(`今日工作更新（${date}）\n\n暂无群聊更新。`);
    return;
  }

  const systemPrompt = buildSystemPrompt();
  const skillContent = loadSkill('daily_report');
  const userPrompt = buildPrompt(chatGroups, docs, date);

  const report = await generate(
    `${systemPrompt}\n\n---\n\n## 当前任务指令\n\n${skillContent}`,
    userPrompt
  );

  await sendFn(report);
  console.log(`[daily-report] sent (${report.length} chars)`);
}

/**
 * Schedule daily report at 18:30 local time.
 * @param {Function} sendFn  async (text) => void
 */
function scheduleDailyReport(sendFn) {
  function msUntilNext1830() {
    const now = new Date();
    const target = new Date(now);
    target.setHours(18, 30, 0, 0);
    if (target <= now) target.setDate(target.getDate() + 1);
    return target - now;
  }

  function scheduleNext() {
    const delay = msUntilNext1830();
    const nextRun = new Date(Date.now() + delay);
    console.log(`[daily-report] next run at ${nextRun.toLocaleString('zh-CN')} (in ${Math.round(delay / 60000)} min)`);

    setTimeout(async () => {
      try {
        await runDailyReport(sendFn);
      } catch (e) {
        console.error('[daily-report] run failed:', e.message);
      }
      scheduleNext();
    }, delay);
  }

  scheduleNext();
}

module.exports = { runDailyReport, scheduleDailyReport };
