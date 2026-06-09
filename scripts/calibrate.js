#!/usr/bin/env node
/**
 * Calibrate boss-bot soul files using historical Feishu messages.
 * Validates: hypothesis → supported / contradicted / deprecated.
 *
 * Usage:
 *   node scripts/calibrate.js --batch=1           # dry-run, confirm, execute
 *   node scripts/calibrate.js --batch=1 --dry-run # dry-run only, no write
 *   node scripts/calibrate.js --batch=all         # all soul batches (1-4) sequentially
 */
require('dotenv').config();
const readline = require('readline');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { readMessages } = require('../src/feishu/messages');
const { generate } = require('../src/llm/client');

const ROOT = path.join(__dirname, '..');
const SOUL_DIR = path.join(ROOT, 'boss-bot', 'soul');
const AUDIT_DIR = path.join(ROOT, 'boss-bot', 'audit');
const REPORTS_DIR = path.join(AUDIT_DIR, 'reports');
const SOURCE_MAP_PATH = path.join(AUDIT_DIR, 'source-map.jsonl');
const BOSS_ID = process.env.BOSS_OPEN_ID;

// ── Groups ───────────────────────────────────────────────────────────────────
// P0: 郑伟主要管理群，发言密度高
const GROUPS_P0 = [
  { id: 'oc_3e96240b7f3708f746cd5a05e05b839c', name: 'AI Agent Team' },
  { id: 'oc_035bedfd39d2c2f5aa941da3d95af8d6', name: '33 direct team' },
  { id: 'oc_800222a883411ba37cc96d3c629f5b73', name: 'DataLab & Product' },
];
// P1: 项目推进群，偶有发言
const GROUPS_P1 = [
  { id: 'oc_85e15d4d13c4f8e18bfc058af0fce1a3', name: 'CB1.0项目跟进搬砖群' },
  { id: 'oc_7de7e9b33dfcb06c3d7097a9ec81894e', name: '门店服务应用内部工作群' },
  { id: 'oc_0c3d0a34ef1e8527a1fde8c15cb1a04e', name: 'CB1.0 商品陈列属性需求沟通' },
  { id: 'oc_f7d79bda2c02c3b7799325ac9fa04ead', name: 'ChatStore未来云店（+供应商）' },
  { id: 'oc_e36a9993ef6b10df9d425a692f712fd8', name: 'WTCCN HO Data Lab & Product_Product' },
  { id: 'oc_0e90958e82b4d0cc00a566e3ab538b25', name: '屈臣氏飞书Aily落地场景沟通' },
];
const GROUPS = [...GROUPS_P0, ...GROUPS_P1];

// ── Batch configs ────────────────────────────────────────────────────────────
const BATCHES = {
  1: {
    name: 'style',
    description: '表达风格校验',
    targetFiles: ['style'],
    days: 90,
    maxPerGroup: 100,      // messages per group from Feishu (P0 groups need more)
    maxBossMessages: 80,   // cap sent to LLM
    // Prefer short messages for style analysis (natural expression)
    messageFilter: msg => msg.text.length <= 250,
    llmFocus: '回复风格、句式结构、回复长度、是否分点、是否用反问、是否用口头禅、语气轻重',
  },
  2: {
    name: 'decision',
    description: '决策方式校验',
    targetFiles: ['decision'],
    days: 90,
    maxPerGroup: 40,
    maxBossMessages: 80,
    messageFilter: msg => msg.text.length >= 10, // decisions tend to be substantive
    llmFocus: '方案审批、优先级判断、否定理由、追问方式、要求补充信息的场景、什么情况推进/暂停/否定',
  },
  3: {
    name: 'management',
    description: '管理方式校验',
    targetFiles: ['management'],
    days: 90,
    maxPerGroup: 40,
    maxBossMessages: 80,
    messageFilter: msg => msg.text.length >= 10,
    llmFocus: '任务派发、追进度、处理延误、要求汇报格式、要求结果而非过程、明确时间节点和责任人',
  },
  4: {
    name: 'communication',
    description: '沟通对象差异校验',
    targetFiles: ['communication'],
    days: 90,
    maxPerGroup: 40,
    maxBossMessages: 80,
    messageFilter: () => true,
    llmFocus: '对下属/管理层/客户/合作方的语气差异、正式程度、是否强调边界、是否强调推进、是否更委婉/直接',
  },
};

// ── Helpers ──────────────────────────────────────────────────────────────────
function hash(text) {
  return 'sha256:' + crypto.createHash('sha256').update(text || '').digest('hex').slice(0, 12);
}

function sanitize(text) {
  return text.slice(0, 60).replace(/\d{11}/g, '***').replace(/[一-龥]{2,4}\d+/g, '***');
}

function makeRunId(batchNum) {
  const d = new Date().toISOString().replace(/[-:T]/g, '').slice(0, 14);
  return `run_${d}_batch${batchNum}`;
}

function extractJSON(text) {
  // Try markdown code block first
  const codeBlock = text.match(/```(?:json)?\s*(\{[\s\S]*?\})\s*```/);
  if (codeBlock) {
    try { return JSON.parse(codeBlock[1]); } catch {}
  }
  // Find outermost { } by depth
  let depth = 0, start = -1, end = -1;
  for (let i = 0; i < text.length; i++) {
    if (text[i] === '{') { if (depth === 0) start = i; depth++; }
    else if (text[i] === '}') { depth--; if (depth === 0) { end = i; break; } }
  }
  if (start === -1 || end === -1) throw new Error(`No JSON in LLM output:\n${text.slice(0, 300)}`);
  const raw = text.slice(start, end + 1);
  try {
    return JSON.parse(raw);
  } catch {
    // Repair: replace unescaped double quotes inside string values
    const repaired = raw.replace(/("(?:hypothesis_text|note|text)"\s*:\s*")([\s\S]*?)("(?:\s*[,}\]]))/g,
      (_, key, val, tail) => key + val.replace(/(?<!\\)"/g, '\\"') + tail
    );
    try {
      return JSON.parse(repaired);
    } catch (e2) {
      throw new Error(`JSON parse failed: ${e2.message}\nRaw: ${raw.slice(0, 400)}`);
    }
  }
}

// ── Prompt confirm ───────────────────────────────────────────────────────────
function confirm(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => {
    rl.question(question, answer => {
      rl.close();
      resolve(answer.trim().toLowerCase() === 'y');
    });
  });
}

// ── Read hypotheses from soul file ───────────────────────────────────────────
function readHypotheses(filePath) {
  if (!fs.existsSync(filePath)) return [];
  const lines = fs.readFileSync(filePath, 'utf8').split('\n');
  const items = [];
  for (let i = 0; i < lines.length - 2; i++) {
    if (lines[i].startsWith('- ') &&
        lines[i + 1]?.match(/^  - status: /) &&
        lines[i + 2]?.match(/^  - evidence: /)) {
      items.push({
        text: lines[i].slice(2).trim(),
        status: lines[i + 1].replace('  - status: ', '').trim(),
        evidence: lines[i + 2].replace('  - evidence: ', '').trim(),
        lineIdx: i,
      });
    }
  }
  return items;
}

// ── Fetch boss messages from all groups ──────────────────────────────────────
async function fetchBossMessages(batch) {
  if (!BOSS_ID) throw new Error('BOSS_OPEN_ID not set in .env');
  const startMs = Date.now() - batch.days * 86400000;
  const endMs = Date.now();
  const allBoss = [];

  for (const group of GROUPS) {
    process.stdout.write(`  读取 ${group.name} ... `);
    try {
      const msgs = await readMessages({ chatId: group.id, startMs, endMs, maxCount: batch.maxPerGroup });
      const boss = msgs.filter(m => m.sender === BOSS_ID && batch.messageFilter(m));
      process.stdout.write(`${boss.length} 条郑伟消息\n`);
      for (const m of boss) {
        allBoss.push({ groupId: group.id, groupName: group.name, ...m });
      }
    } catch (err) {
      process.stdout.write(`跳过 (${err.message.slice(0, 50)})\n`);
    }
    await new Promise(r => setTimeout(r, 600));
  }

  // Sort by time desc, cap at maxBossMessages
  allBoss.sort((a, b) => b.timestamp.localeCompare(a.timestamp));
  return allBoss.slice(0, batch.maxBossMessages);
}

// ── LLM calibration ──────────────────────────────────────────────────────────
async function callLLM(batch, hypotheses, messages, runId) {
  const hypothesisList = hypotheses
    .filter(h => h.status === 'hypothesis')
    .map((h, i) => `[H${i + 1}] ${h.text}`)
    .join('\n');

  const messageList = messages
    .map((m, i) => {
      const sid = `${runId}/source_${String(i + 1).padStart(3, '0')}`;
      return `[${sid}] [${m.timestamp.slice(0, 10)}] [${m.groupName}] ${m.text}`;
    })
    .join('\n');

  const system = `你是一个行为分析助手，专门从飞书消息中提取郑伟的稳定行为模式。
规则：
- 只分析郑伟的消息（已预先过滤，以下消息均为郑伟发言）
- 基于实际观察，不推断，不假设
- supported：需要至少 2 条不同时间/场景的证据
- contradicted：明确与假设相反的证据
- insufficient：证据太少或不确定，保持 hypothesis
- 新增条目必须是稳定可复用的规律，不是一次性情境
- 严禁保存原始消息正文，evidence 只写 source_id
- 输出必须是合法 JSON，不要任何前言或解释
- 所有字符串字段内严禁使用双引号（"），改用「」或单引号`;

  const user = `## 待校验假设（${batch.description}）

聚焦维度：${batch.llmFocus}

${hypothesisList}

---

## 郑伟历史消息（source_id 格式：run_id/source_NNN）

${messageList}

---

## 输出格式（严格 JSON，不要其他内容）

{
  "calibrations": [
    {
      "hypothesis_text": "（完整复制原文，一字不差）",
      "new_status": "supported|contradicted|insufficient",
      "evidence_ids": ["${runId}/source_001"],
      "note": "简要说明，1句话"
    }
  ],
  "new_items": [
    {
      "text": "新发现的稳定规律，作为新假设条目",
      "status": "supported",
      "evidence_ids": ["${runId}/source_003"],
      "note": "说明为什么是稳定规律"
    }
  ]
}`;

  const raw = await generate(system, user, { timeoutMs: 180000 });
  return extractJSON(raw);
}

// ── Apply calibrations to soul file ──────────────────────────────────────────
function applyToFile(filePath, calibrations, newItems, runId) {
  let content = fs.readFileSync(filePath, 'utf8');
  let updated = 0, added = 0;

  for (const cal of calibrations) {
    if (cal.new_status === 'insufficient') continue;
    const evidenceStr = cal.evidence_ids.join(', ');
    const noteStr = cal.note ? `\n  - note: ${cal.note}` : '';

    // Match: "- {text}\n  - status: hypothesis\n  - evidence: {old}"
    const escapedText = cal.hypothesis_text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const re = new RegExp(
      `(^- ${escapedText}\n  - status: )hypothesis(\n  - evidence: )[^\n]+`,
      'm'
    );

    if (re.test(content)) {
      content = content.replace(re, `$1${cal.new_status}$2${evidenceStr}${noteStr}`);
      updated++;
    } else {
      console.log(`  ⚠️  未找到匹配假设: ${cal.hypothesis_text.slice(0, 40)}`);
    }
  }

  if (newItems && newItems.length > 0) {
    const toAppend = newItems.map(item => {
      const evidenceStr = item.evidence_ids.join(', ');
      const noteStr = item.note ? `\n  - note: ${item.note}` : '';
      return `- ${item.text}\n  - status: ${item.status}\n  - evidence: ${evidenceStr}${noteStr}`;
    }).join('\n\n');

    content += `\n\n---\n\n<!-- 新增条目 | run_id: ${runId} -->\n\n${toAppend}`;
    added = newItems.length;
  }

  fs.writeFileSync(filePath, content);
  return { updated, added };
}

// ── Audit: source-map.jsonl ───────────────────────────────────────────────────
function writeSourceMap(messages, calibrations, batch, runId) {
  fs.mkdirSync(AUDIT_DIR, { recursive: true });
  const now = new Date().toISOString();

  // Build set of source_ids that actually entered distillation (cited in calibrations)
  const cited = new Set();
  for (const cal of calibrations) {
    for (const sid of (cal.evidence_ids || [])) cited.add(sid);
  }

  const lines = messages.map((m, i) => {
    const sourceId = `${runId}/source_${String(i + 1).padStart(3, '0')}`;
    return JSON.stringify({
      run_id: runId,
      source_id: sourceId,
      source_type: 'feishu_message',
      source_name: m.groupName,
      involved_users: ['郑伟'],
      entered_distillation: cited.has(sourceId),
      target_file: batch.targetFiles.map(f => `soul/${f}.md`).join(', '),
      sanitized_summary: sanitize(m.text),
      content_hash: hash(m.text),
      operator: 'calibrate-script',
      created_at: now,
    });
  });

  fs.appendFileSync(SOURCE_MAP_PATH, lines.join('\n') + '\n');
}

// ── Audit: report.md ─────────────────────────────────────────────────────────
function writeReport(batch, runId, messages, calibrationResult, stats) {
  fs.mkdirSync(REPORTS_DIR, { recursive: true });
  const date = new Date().toISOString().split('T')[0];
  const reportPath = path.join(REPORTS_DIR, `${date}-${runId}-report.md`);

  const calCount = calibrationResult.calibrations?.length || 0;
  const supportedCount = calibrationResult.calibrations?.filter(c => c.new_status === 'supported').length || 0;
  const contradictedCount = calibrationResult.calibrations?.filter(c => c.new_status === 'contradicted').length || 0;
  const insufficientCount = calibrationResult.calibrations?.filter(c => c.new_status === 'insufficient').length || 0;
  const newCount = calibrationResult.new_items?.length || 0;

  const calDetail = (calibrationResult.calibrations || []).map(c =>
    `- [${c.new_status}] ${c.hypothesis_text.slice(0, 60)}\n  - 证据: ${c.evidence_ids?.join(', ')}\n  - ${c.note || ''}`
  ).join('\n');

  const content = `# 历史消息校验审计报告

## 基本信息

- run_id: ${runId}
- 批次: Batch ${Object.entries(BATCHES).find(([, b]) => b.name === batch.name)?.[0]} — ${batch.description}
- 操作时间: ${new Date().toISOString()}
- 操作者: calibrate-script

## 读取范围

- 群数量: ${GROUPS.length}
- 时间范围: 近 ${batch.days} 天
- 每群最大消息数: ${batch.maxPerGroup}

## 读取结果汇总

- 郑伟消息总数（进入 LLM）: ${messages.length}
- 目标文件: ${batch.targetFiles.map(f => `soul/${f}.md`).join(', ')}

## 校验结果

- 校验假设总数: ${calCount}
- supported（已支持）: ${supportedCount}
- contradicted（已推翻）: ${contradictedCount}
- insufficient（证据不足）: ${insufficientCount}
- 新增条目: ${newCount}

## 文件更新

- 更新假设状态: ${stats.updated} 条
- 新增条目: ${stats.added} 条

## 假设详情

${calDetail}

## 安全处理

- 原始消息正文已丢弃，未持久化
- 仅保存: source_id、sanitized_summary、content_hash
- 证据可通过 source-map.jsonl 追溯

## 待补充

- 证据不足的假设需继续累积数据
`;

  fs.writeFileSync(reportPath, content);
  return reportPath;
}

// ── Dry-run ───────────────────────────────────────────────────────────────────
function showDryRun(batchNum) {
  const batch = BATCHES[batchNum];
  console.log(`\n📋 Dry-run — Batch ${batchNum}: ${batch.description}`);
  console.log('─'.repeat(60));
  console.log(`目标文件: ${batch.targetFiles.map(f => `soul/${f}.md`).join(', ')}`);
  console.log(`时间范围: 近 ${batch.days} 天`);
  console.log(`每群最大消息: ${batch.maxPerGroup} 条 → 仅保留郑伟发言`);
  console.log(`LLM 输入上限: ${batch.maxBossMessages} 条郑伟消息`);
  console.log(`聚焦维度: ${batch.llmFocus}`);
  console.log(`\n读取群列表 (${GROUPS.length} 个):`);
  GROUPS.forEach(g => console.log(`  · ${g.name}`));

  const hypotheses = [];
  for (const f of batch.targetFiles) {
    const fp = path.join(SOUL_DIR, `${f}.md`);
    const h = readHypotheses(fp).filter(x => x.status === 'hypothesis');
    hypotheses.push(...h);
    console.log(`\n${f}.md — ${h.length} 个待校验假设:`);
    h.forEach(x => console.log(`  · ${x.text.slice(0, 60)}`));
  }

  console.log(`\n⚠️  风险提示:`);
  console.log(`  · 会读取 ${GROUPS.length} 个群的消息（包含所有成员）`);
  console.log(`  · 仅分析郑伟发言，其他成员消息用作上下文后丢弃`);
  console.log(`  · 原始消息正文不持久化`);
  console.log('─'.repeat(60));
}

// ── Run one batch ─────────────────────────────────────────────────────────────
async function runBatch(batchNum, dryRunOnly) {
  const batch = BATCHES[batchNum];
  if (!batch) throw new Error(`未知批次: ${batchNum}`);

  showDryRun(batchNum);

  if (dryRunOnly) {
    console.log('\n[dry-run 模式，不执行实际操作]\n');
    return;
  }

  const proceed = await confirm('\n确认执行? (y/n): ');
  if (!proceed) { console.log('已取消。\n'); return; }

  const runId = makeRunId(batchNum);
  console.log(`\n🆔 run_id: ${runId}`);
  console.log('\n📥 读取飞书消息...');

  const messages = await fetchBossMessages(batch);
  if (messages.length === 0) {
    console.log('❌ 未读取到郑伟消息，退出。\n');
    return;
  }
  console.log(`✅ 共 ${messages.length} 条郑伟消息进入分析`);

  // Load hypotheses for all target files
  const hypothesesByFile = {};
  for (const f of batch.targetFiles) {
    const fp = path.join(SOUL_DIR, `${f}.md`);
    hypothesesByFile[f] = readHypotheses(fp);
  }
  const allHypotheses = Object.values(hypothesesByFile).flat();
  const pendingCount = allHypotheses.filter(h => h.status === 'hypothesis').length;
  console.log(`\n🔍 发起 LLM 校验 (${pendingCount} 个 hypothesis)...`);

  const result = await callLLM(batch, allHypotheses, messages, runId);
  console.log(`✅ LLM 返回: ${result.calibrations?.length || 0} 条校验, ${result.new_items?.length || 0} 条新增`);

  // Apply to files
  let totalStats = { updated: 0, added: 0 };
  for (const f of batch.targetFiles) {
    const fp = path.join(SOUL_DIR, `${f}.md`);
    // Filter calibrations relevant to this file's hypotheses
    const fileHyps = new Set(hypothesesByFile[f].map(h => h.text));
    const fileCals = (result.calibrations || []).filter(c => fileHyps.has(c.hypothesis_text));
    const fileNew = result.new_items || [];
    const stats = applyToFile(fp, fileCals, fileNew.length > 0 && f === batch.targetFiles[0] ? fileNew : [], runId);
    console.log(`  soul/${f}.md: 更新 ${stats.updated} 条, 新增 ${stats.added} 条`);
    totalStats.updated += stats.updated;
    totalStats.added += stats.added;
  }

  // Audit
  writeSourceMap(messages, result.calibrations || [], batch, runId);
  const reportPath = writeReport(batch, runId, messages, result, totalStats);
  console.log(`\n📊 Audit 报告: ${path.relative(ROOT, reportPath)}`);
  console.log(`📊 Source map: boss-bot/audit/source-map.jsonl`);
  console.log('\n✅ Batch', batchNum, '完成\n');
}

// ── Main ──────────────────────────────────────────────────────────────────────
async function main() {
  const args = process.argv.slice(2);
  const batchArg = args.find(a => a.startsWith('--batch='))?.split('=')[1];
  const dryRunOnly = args.includes('--dry-run');

  if (!batchArg) {
    console.error('用法: node scripts/calibrate.js --batch=1|2|3|4|all [--dry-run]');
    process.exit(1);
  }

  if (batchArg === 'all') {
    for (const num of [1, 2, 3, 4]) {
      await runBatch(num, dryRunOnly);
    }
  } else {
    const num = parseInt(batchArg, 10);
    if (!BATCHES[num]) {
      console.error(`批次 ${num} 不存在。可用: 1 2 3 4`);
      process.exit(1);
    }
    await runBatch(num, dryRunOnly);
  }
}

main().catch(err => { console.error('❌', err.message); process.exit(1); });
