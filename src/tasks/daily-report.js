const { listAllChats, readMessages } = require('../feishu/messages');
const { listMinutes, readMinutes } = require('../feishu/minutes');
const { buildSystemPrompt, loadSkill } = require('../soul/loader');
const { generate } = require('../llm/client');

// ── 群分级配置 ────────────────────────────────────────────────────────────

const LEVEL_1_GROUPS = new Set([
  '33 direct team',
  'AI-Agent Team',
  'WTCCN HO Data Lab & Product',
  'WTCCN HO Data Lab & Product_Product',
  '未来云店-项目组',
  'Ivy Han(韩媛媛), Gavin Zheng(郑伟), Gavin Liu(刘利伟)',
  'Shanshan Li(李珊珊), Gavin Zheng(郑伟), Coral Ho(何宇珊)',
]);

const LEVEL_2_GROUPS = new Set([
  'GPTPro客户沟通群',
  '屈臣氏 & 飞书  知识运营专项',
  'PD × 飞书',
  '屈臣氏飞书专属运维中心',
  '门店数字化能力蓝图',
  '门店服务应用内部工作群（门店提效助手 & 巡店助手）',
  '智能问答内部工作群',
  '屈臣氏｜飞书Aily落地场景沟通',
  '门店生态图',
  'chatstore需求沟通',
  '门店AI-Agent-IT 800子项目沟通',
  'DC × 飞书沟通群',
  'IA × 飞书沟通群',
  '屈臣氏 AI 需求讨论|  MooX AI',
  'AI效率先锋大赛--内部群',
  '知识运营管理项目 业务群',
  '未来云店项目内部小群',
  '未来云店救命群😂',
  'ChatStore未来云店（+供应商）',
  '未来云店&商品信息问题沟通群',
  '未来云店合同咨询',
  '未来云店Sourcing',
  'Supply & Product LLM-Agent 落地沟通群',
  'DEV & Product LLM-Agent 场景沟通群',
  'Finance & CST LLM-Agent 场景沟通群',
  'Trading & CST LLM-Agent 场景沟通群',
  'DC & CST LLM-Agent 场景沟通群',
  'NOD & CST LLM-Agent 场景沟通',
  'BFM & CST LLM-Agent场景沟通',
  'QA & Product LLM-Agent 场景沟通群',
  'O+O & CST LLM Agent沟通群',
  'People & CST',
  'People & Product 智能问答沟通群',
  'IA & CST 沟通群',
  'VOC Agent 沟通群',
  'VOC项目沟通群（业务 & 产品）',
  'voc数据同步',
  'CB1.0项目跟进搬砖群',
  'CB需求沟通',
  '门店提效助手  & 供应链需求',
  '门店agent--WDC数据支持',
  '巡店助手沟通小群 （业务+产品）',
  '智能访店助手SVA- IT&产品',
  'SVA智能访店用户UAT沟通',
  '[项目组]智能访店助手SVA一期UAT测试群',
  '屈臣氏-语音工牌需求',
  '飞书-语音工牌能力探索',
  '屈臣氏 X 语音工牌需求',
  'Legal AI提效需求',
  '财务部AI项目组',
  'Gen AI Library',
  'Gen AI L2项目沟通群',
  '查数mcp能力沟通',
  'ChatBI - 探索小组',
  '智能体小分队',
  '10个Agent场景',
  '门店产品系列设计规范',
  '云店活动风控Review和AI赋能',
  '健康智能问答沟通群',
  'Health智能问答沟通群',
  'Development AI陪练',
  'I-Memo项目群',
  'I-Memo 1.0 项目沟通群',
  'BFM Reporting & Analysis AI 项目实施沟通',
  'LLM - 财务数据提取+预测+分析 POC 沟通',
  '门店问答',
  'IA 黄金会议总结skill讨论',
  '门店提效助手-mcp需求沟通',
  '飞书智能中心沟通',
]);

// 完全跳过的群（Bot 自身服务台 / Demo 群 / 无效群）
const EXCLUDED_GROUPS = new Set([
  'Gavin Zheng\'s Feishu Assistant',
  'Gavin\'s IT Help Desk (Demo)',
  'Gavin Zheng\'s Gavin - 服务台能力测试',
  'Gavin Zheng\'s People智答服务台',
  'Gavin Zheng\'s 财务智答服务台',
  '[Closed] 11977 Gavin Zheng\'s 财务智答服务台',
  'test',
]);

function inferGroupLevel(name) {
  if (/服务台|[Dd]emo|[Tt]est|\[Closed\]|已关闭|机器人|[Bb]ot/.test(name)) return 0;

  // 广播/教育性大群，即使含 AI 等词也归三级
  if (/全员|训练营|大群|培训|公告|学员/.test(name)) return 3;

  // 人名组合小群：格式类似 "张三(Zhang San), 李四(Li Si)" 且人数 ≤ 3
  const commaCount = (name.match(/[,，]/g) || []).length;
  if (commaCount <= 2 && /\(|\（/.test(name) && name.length < 80) return 1;

  if (/项目|需求|沟通|合作|专项|工作群|推进|[Aa]gent|AI|LLM|[Pp]roduct|[Dd]ev|[Dd]ata/.test(name)) return 2;

  return 3;
}

function getGroupLevel(name) {
  if (EXCLUDED_GROUPS.has(name)) return 0;
  if (LEVEL_1_GROUPS.has(name)) return 1;
  if (LEVEL_2_GROUPS.has(name)) return 2;
  return inferGroupLevel(name);
}

// ── 数据采集 ──────────────────────────────────────────────────────────────

async function collectMessages(startMs, endMs) {
  const chats = await listAllChats();
  console.log(`[daily-report] found ${chats.length} chats, pulling messages...`);

  const active = [];
  for (const chat of chats) {
    const level = getGroupLevel(chat.name);
    if (level === 0) continue;

    try {
      const messages = await readMessages({ chatId: chat.chatId, startMs, endMs, maxCount: 100 });
      if (messages.length > 0) {
        active.push({ chatName: chat.name, level, messages });
      }
    } catch (e) {
      console.warn(`[daily-report] skip chat ${chat.chatId} (${chat.name}): ${e.message}`);
    }
  }

  active.sort((a, b) => a.level - b.level);
  console.log(`[daily-report] active chats: L1=${active.filter(c=>c.level===1).length} L2=${active.filter(c=>c.level===2).length} L3=${active.filter(c=>c.level===3).length}`);
  return active;
}

async function collectMeetingMinutes(startMs, endMs) {
  try {
    const list = await listMinutes(startMs, endMs);
    if (list.length === 0) return [];

    const result = [];
    for (const m of list) {
      try {
        const content = await readMinutes(m.minutesToken);
        if (content) result.push({ topic: m.topic, startTime: m.startTime, content: content.slice(0, 3000) });
      } catch (e) {
        console.warn(`[daily-report] skip minutes ${m.minutesToken} (${m.topic}): ${e.message}`);
      }
    }
    console.log(`[daily-report] collected ${result.length} meeting minutes`);
    return result;
  } catch (e) {
    console.warn(`[daily-report] collectMinutes failed: ${e.message}`);
    return [];
  }
}

// ── Prompt 构建 ───────────────────────────────────────────────────────────

const LEVEL_LABEL = { 1: '一级群', 2: '二级群', 3: '三级群' };

function buildPrompt(chatGroups, minutes, date) {
  const lines = [`今天是 ${date}，请根据以下群聊内容和会议纪要生成日报。\n`];

  for (const { chatName, level, messages } of chatGroups) {
    lines.push(`【${LEVEL_LABEL[level]}】${chatName}`);
    for (const m of messages) {
      lines.push(`${m.timestamp.slice(11, 16)} ${m.text}`);
    }
    lines.push('');
  }

  if (minutes.length > 0) {
    lines.push('【今日妙记】');
    for (const m of minutes) {
      lines.push(`\n### ${m.topic}（${m.startTime.slice(11, 16)}）`);
      lines.push(m.content);
      lines.push('');
    }
  }

  return lines.join('\n');
}

// ── 主流程 ────────────────────────────────────────────────────────────────

async function runDailyReport(sendFn, { startMs, endMs } = {}) {
  const now = new Date();
  const midnight = new Date(now);
  midnight.setHours(0, 0, 0, 0);
  const start = startMs ?? midnight.getTime();
  const end = endMs ?? now.getTime();

  const date = now.toLocaleDateString('zh-CN', { month: 'long', day: 'numeric', weekday: 'short' });
  console.log(`[daily-report] starting for ${date}`);

  const [chatGroups, minutes] = await Promise.all([
    collectMessages(start, end),
    collectMeetingMinutes(start, end),
  ]);

  if (chatGroups.length === 0 && minutes.length === 0) {
    await sendFn(`📊 日报 · ${date}\n\n今日各群无实质性更新。`);
    return;
  }

  const systemPrompt = buildSystemPrompt();
  const skillContent = loadSkill('daily_report');
  const userPrompt = buildPrompt(chatGroups, minutes, date);

  const report = await generate(
    `${systemPrompt}\n\n---\n\n## 当前任务指令\n\n${skillContent}`,
    userPrompt
  );

  await sendFn(report);
  console.log(`[daily-report] sent (${report.length} chars)`);
}

// ── 调度器 ────────────────────────────────────────────────────────────────

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
