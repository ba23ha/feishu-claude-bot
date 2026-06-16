# Inline Comment Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 扩展方案评审能力，支持 Bot 读取飞书文档后自动生成内联批注建议（inline_comment 模式），Boss 确认后写入文档评论区。

**Architecture:** 新增 `review_inline` 任务类型。Boss 发送含飞书文档链接的消息，Bot 读取文档、调用 LLM 生成 JSON 格式批注建议、发送预览给 Boss，Boss 确认后调用 Feishu Drive Comment API 写入文档。无法写入时降级为可复制清单。复用现有的 pending 确认流程（与 distill 同模式）。

**Tech Stack:** Node.js, @larksuiteoapi/node-sdk, Feishu Drive Comment API (POST /open-apis/drive/v1/files/{token}/comments), 现有 `readDoc()`/`resolveWikiNode()`/`getValidToken()` in docs.js, claude CLI via `generate()`

---

## 文件变更总览

| 文件 | 操作 | 说明 |
|------|------|------|
| `boss-bot/skills/review-proposal.md` | Modify | 增加 review_mode / inline_comment 模式规范 |
| `boss-bot/agents/review-agent.md` | Modify | 增加 inline_comment 模式工作流 |
| `boss-bot/agents/router-agent.md` | Modify | 增加 review_proposal_inline_comment 任务类型 |
| `boss-bot/agents/safety-agent.md` | Modify | 增加文档自动批注安全检查项 |
| `src/feishu/docs.js` | Modify | 增加 writeDocComment() |
| `src/bot/router.js` | Modify | 增加 review_inline 检测 + 飞书文档 URL 提取 |
| `src/soul/loader.js` | Modify | 增加 review_inline → review-proposal.md |
| `src/bot/handler.js` | Modify | 增加 handleInlineReview() |
| `server.js` | Modify | 增加 pendingInlineReviews 确认流程 |
| `boss-bot/evals/boss-likeness.jsonl` | Modify | 新增 3 条 review_proposal_inline_comment 用例 |
| `README.md` | Modify | 补充文档自动批注能力说明 |

---

## Task 1: 更新 Agent/Skill 规范文件

**Files:**
- Modify: `boss-bot/skills/review-proposal.md`
- Modify: `boss-bot/agents/review-agent.md`
- Modify: `boss-bot/agents/router-agent.md`
- Modify: `boss-bot/agents/safety-agent.md`

- [ ] **Step 1: 更新 review-proposal.md**

替换全文为：

```markdown
# Review Proposal Skill

## review_mode

本 skill 支持两种模式：

- `summary_review` — 整体方案评审（默认，现有行为不变）
- `inline_comment` — 文档内自动批注（新增）

---

## summary_review 模式

### 适用场景
- 老板说"帮我看下这个方案"
- 老板说"评审一下这个计划"

### 执行步骤
1. 判断目标是否清楚。
2. 判断价值和产出是否明确。
3. 检查优先级是否合理。
4. 检查负责人、资源和时间节点。
5. 找出主要风险。
6. 判断缺少哪些关键信息。
7. 生成老板可能会追问的问题。
8. 给出下一步建议。

### 输出格式（纯文本，不用 markdown）
总体判断：（推进 / 谨慎推进 / 需要修改 / 不建议）
主要问题：（2-3 条）
风险：（1-2 条）
缺失信息：（缺什么就说缺什么）
可能追问：（2-3 个问题）
建议下一步：（一句话）

---

## inline_comment 模式

### 适用场景
- 老板收到飞书文档并要求自动审阅
- 含"自动批注 / 文档批注 / 帮我在文档里评论 / 看下这份文档并批注"

### 自动筛选规则

Bot 在文档中重点筛选以下问题，每类问题只保留最典型的一条：

| issue_type | 说明 |
|---|---|
| unclear_goal | 目标不清 |
| missing_data | 缺数据依据 |
| unclear_roi | 产出不明确 |
| unclear_owner | 责任人不清 |
| unclear_deadline | 时间节点不清 |
| insufficient_risk_plan | 风险应对不足 |
| unclear_resource | 资源需求不清 |
| logic_gap | 结论跳跃 |
| unclear_expression | 表达模糊 |
| context_conflict | 上下文矛盾 |
| unclear_follow_up | follow-up 不清 |
| unclear_decision | 决策项不清 |
| unclear_acceptance | 验收标准不清 |
| general | 其他 |

### 批注数量控制

默认规则（每份文档）：
- 最多生成 5 条批注建议
- 只选值得老板关注的问题
- 同类问题只保留最典型的一条
- 低价值未成问题不过度批注
- 优先批注影响决策、推进、风险和结果的问题

老板明确要求"详细批注"时放宽至最多 10 条。

### 评论风格要求

批注评论必须符合老板风格：
- 简洁
- 直接
- 具体
- 指向下一步动作
- 不写铺垫句
- 不做人身评价
- 不写长篇解释
- 不加假设性措辞

优先使用这类表达：
- 这里目标还不够清楚，补一下衡量标准和预期结果。
- 这个结论的数据依据是什么？建议补来源和关键数据。
- 这里需要明确责任人，否则后续推进容易落空。
- 这个动作需要补一个明确时间点。
- 风险应对方案还没看到，建议补如果延期或资源不足时怎么处理。
- 这段表达有点绕，建议先说结论，再说原因。
- 这里和前面关于目标的表述不一致，需要统一一下。
- 这里需要明确下一步动作、责任人和截止时间。

### inline_comment 输出格式（JSON）

```json
{
  "review_mode": "inline_comment",
  "document_title": "文档标题",
  "summary": "本次识别 N 个值得批注的问题，主要集中在目标、责任人、风险和时间节点。",
  "comments": [
    {
      "selected_text": "文档中需要划线的原文内容",
      "section_title": "所在章节标题（可为空）",
      "issue_type": "unclear_owner",
      "severity": "medium",
      "comment_draft": "这里需要明确责任人，否则后续推进容易落空。",
      "reason": "该段只说了继续推进，但没有说谁来负责、何时完成。",
      "required_confirmation": true
    }
  ],
  "requires_boss_confirmation": true
}
```

severity 取值：high / medium / low

### 禁止

- 不直接修改文档正文
- 不删除文档内容
- 不替老板做最终判断
- 未经确认不写入文档评论区
- 不批量发布大量评论
- 不把 AI 建议说成老板已经确认的决定
```

- [ ] **Step 2: 更新 review-agent.md**

替换全文为：

```markdown
# Review Agent

## 职责

- 支持 summary_review 和 inline_comment 两种评审模式。
- 加载 soul/decision.md、soul/management.md、soul/taboos.md。
- 加载 skills/review-proposal.md。
- 调用 safety-agent 检查。

---

## summary_review 模式

加载：
- soul/decision.md
- soul/management.md
- soul/taboos.md
- skills/review-proposal.md
- memory/projects.md（可选）
- memory/glossary.md（可选）

输出：总体判断、主要问题、风险、缺失信息、老板可能追问的问题、建议下一步。

---

## inline_comment 模式

输入：
- document_id
- document_title
- document_content
- operator_user_id
- max_comments（默认 5）

工作流：
1. 校验 operator_user_id 是否为老板本人或授权调试人员。
2. 获取文档内容。
3. 识别文档结构（段落、标题、表格、列表）。
4. 按自动筛选规则找出问题段落。
5. 控制批注数量。
6. 为每个问题生成 selected_text。
7. 为每个问题生成 comment_draft（老板风格）。
8. 调用 safety-agent 检查。
9. 输出批注预览（JSON 格式）。
10. 等待老板确认。
11. 老板确认后，允许写入飞书文档评论区。

输出：review_mode、document_title、summary、comments、requires_boss_confirmation。
```

- [ ] **Step 3: 更新 router-agent.md**

在任务类型列表末尾加入 `review_proposal_inline_comment`，路由规则末尾加入：

```
- 含"自动批注 / 文档批注 / 帮我在文档里评论 / 看下这份文档并批注" → review_proposal_inline_comment
- 来自飞书文档自动审阅请求 → review_proposal_inline_comment
```

路由输出示例：
```json
{
  "task_type": "review_proposal_inline_comment",
  "review_mode": "inline_comment",
  "required_soul": ["decision", "management", "style", "communication", "taboos"],
  "required_skills": ["review-proposal"],
  "required_memory": ["projects", "glossary"],
  "need_safety_check": true,
  "required_confirmation": true
}
```

- [ ] **Step 4: 更新 safety-agent.md**

在检查项末尾追加：

```markdown
## 文档自动批注安全检查

inline_comment 输出前必须检查：

- 是否试图直接修改文档正文。
- 是否删除或覆盖他人内容。
- 是否替老板最终确稿判断。
- 是否把 AI 建议说成老板已经确认的决定。
- 是否含攻击性、人身评价表达。
- 是否暴露 boss-private 内容。
- 是否未经确认就发布公开评论。
- 是否一次性生成过多评论。
- 是否对非老板用户开放该能力。

如果发现风险：
1. 优先改写为安全评论。
2. 如果无法改写，输出：该评论涉及老板最终判断，需要老板本人确认。
```

- [ ] **Step 5: Commit**

```bash
git add boss-bot/skills/review-proposal.md boss-bot/agents/review-agent.md boss-bot/agents/router-agent.md boss-bot/agents/safety-agent.md
git commit -m "feat: extend review skill with inline_comment mode (spec docs)"
```

---

## Task 2: Feishu docs.js — writeDocComment

**Files:**
- Modify: `src/feishu/docs.js`

- [ ] **Step 1: 添加 writeDocComment 函数**

在 `readDocComments` 函数后、`module.exports` 前插入：

```javascript
/**
 * Write a single inline comment to a Feishu document.
 * Uses user OAuth token so the comment appears as boss's comment.
 * Falls back gracefully if API doesn't support quote-based inline comments.
 *
 * @param {string} fileToken   Document token (obj_token from wiki or direct docx token)
 * @param {string} fileType    'docx' | 'doc'
 * @param {string} commentText The comment body text
 * @param {string} [quoteText] The selected text to highlight (optional for inline)
 * @returns {Promise<{success: boolean, commentId?: string, error?: string}>}
 */
async function writeDocComment(fileToken, fileType = 'docx', commentText, quoteText) {
  const token = await getValidToken();

  const elements = [{ type: 'text_run', text_run: { text: commentText } }];
  const body = {
    content: { elements },
  };
  if (quoteText) body.quote = quoteText;

  return new Promise((resolve) => {
    const bodyStr = JSON.stringify(body);
    const req = require('https').request({
      hostname: 'open.feishu.cn',
      path: `/open-apis/drive/v1/files/${fileToken}/comments?file_type=${fileType}`,
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(bodyStr),
      },
    }, res => {
      let data = '';
      res.on('data', d => { data += d; });
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          if (parsed.code === 0) {
            resolve({ success: true, commentId: parsed.data?.comment?.comment_id });
          } else {
            resolve({ success: false, error: `API ${parsed.code}: ${parsed.msg}` });
          }
        } catch (e) {
          resolve({ success: false, error: e.message });
        }
      });
    });
    req.on('error', e => resolve({ success: false, error: e.message }));
    req.write(bodyStr);
    req.end();
  });
}
```

更新 module.exports：

```javascript
module.exports = { readDoc, resolveWikiNode, readDocComments, writeDocComment };
```

- [ ] **Step 2: Commit**

```bash
git add src/feishu/docs.js
git commit -m "feat: add writeDocComment to Feishu docs client"
```

---

## Task 3: router.js + loader.js — 新增任务类型

**Files:**
- Modify: `src/bot/router.js`
- Modify: `src/soul/loader.js`

- [ ] **Step 1: router.js 增加 review_inline 检测**

在 PATTERNS 数组末尾（`followup` 条目之后）插入：

```javascript
  {
    type: 'review_inline',
    patterns: [
      /自动批注/, /文档批注/, /帮.*文档.*评论/, /在文档.*批注/, /看.*文档.*批注/,
      // 飞书文档链接 + 评审意图
      /feishu\.cn\/(docx|wiki)\/[A-Za-z0-9]+/,
    ]
  },
```

在 `detectTaskType` 函数之后、`module.exports` 之前添加 URL 提取工具：

```javascript
/**
 * Extract Feishu document token and type from a message.
 * Returns null if no Feishu doc URL found.
 * @param {string} text
 * @returns {{ token: string, urlType: 'docx'|'wiki' } | null}
 */
function extractDocToken(text) {
  const m = text.match(/feishu\.cn\/(docx|wiki)\/([A-Za-z0-9]+)/);
  if (!m) return null;
  return { token: m[2], urlType: m[1] };
}

module.exports = { detectTaskType, extractDocToken };
```

- [ ] **Step 2: loader.js 增加 review_inline**

在 SKILL_FILES 对象中加入：

```javascript
  review_inline: 'review-proposal.md',
```

- [ ] **Step 3: Commit**

```bash
git add src/bot/router.js src/soul/loader.js
git commit -m "feat: add review_inline task type to router and loader"
```

---

## Task 4: handler.js — inline review 处理函数

**Files:**
- Modify: `src/bot/handler.js`

- [ ] **Step 1: 在文件顶部添加 import**

在现有 require 语句后追加：

```javascript
const { resolveWikiNode, readDoc } = require('../feishu/docs');
```

- [ ] **Step 2: 添加 extractJSON 工具函数**

在 `handleTask` 函数前插入：

```javascript
function extractJSON(text) {
  // Try markdown code block first
  const codeBlock = text.match(/```(?:json)?\s*([\s\S]*?)```/);
  if (codeBlock) {
    try { return JSON.parse(codeBlock[1].trim()); } catch {}
  }
  // Depth-tracking brace matching
  let depth = 0, start = -1;
  for (let i = 0; i < text.length; i++) {
    if (text[i] === '{') { if (depth === 0) start = i; depth++; }
    else if (text[i] === '}') {
      depth--;
      if (depth === 0 && start !== -1) {
        try { return JSON.parse(text.slice(start, i + 1)); } catch {}
      }
    }
  }
  throw new Error('No valid JSON found in LLM output');
}
```

- [ ] **Step 3: 添加 handleInlineReview 函数**

在 `handleClarification` 函数前插入：

```javascript
/**
 * Handle inline comment review for a Feishu document.
 * Reads the document, calls LLM to generate comment suggestions, returns preview.
 *
 * @param {string} docToken   Direct docx token (already resolved from wiki if needed)
 * @param {string} userInput  Original boss message for context
 * @param {number} [maxComments=5]
 * @returns {Promise<{ preview: string, comments: object[], docToken: string }>}
 */
async function handleInlineReview(docToken, userInput, maxComments = 5) {
  const docContent = await readDoc(docToken);
  if (!docContent || docContent.trim().length < 50) {
    throw new Error('文档内容为空或过短，无法分析');
  }

  const systemPrompt = buildSystemPrompt();
  const skillContent = loadSkill('review_inline');
  const projects = loadMemory('projects');
  const glossary = loadMemory('glossary');

  const memoryParts = [];
  if (projects) memoryParts.push(`### 项目信息\n${projects}`);
  if (glossary) memoryParts.push(`### 术语表\n${glossary}`);
  const memoryContext = memoryParts.length > 0
    ? `\n\n---\n\n## 背景记忆\n\n${memoryParts.join('\n\n')}`
    : '';

  const combinedSystem = `${systemPrompt}${memoryContext}\n\n---\n\n## 当前任务指令\n\n${skillContent}`;

  const userPrompt = `review_mode: inline_comment
max_comments: ${maxComments}

文档内容：
${docContent.slice(0, 6000)}

请按 inline_comment 输出格式输出 JSON，不要输出其他内容。`;

  let parsed;
  let lastErr;
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      const raw = await generate(combinedSystem, userPrompt);
      parsed = extractJSON(raw);
      break;
    } catch (e) {
      lastErr = e;
    }
  }
  if (!parsed) throw new Error(`LLM 输出解析失败: ${lastErr?.message}`);

  const comments = parsed.comments || [];
  const summary = parsed.summary || `识别到 ${comments.length} 个问题`;

  // Format human-readable preview
  const lines = [`📋 文档批注预览\n${summary}\n`];
  comments.forEach((c, i) => {
    const sev = c.severity === 'high' ? '🔴' : c.severity === 'medium' ? '🟡' : '⚪';
    lines.push(`${i + 1}. ${sev} [${c.issue_type}]`);
    if (c.section_title) lines.push(`   章节：${c.section_title}`);
    lines.push(`   划线：「${(c.selected_text || '').slice(0, 60)}${(c.selected_text || '').length > 60 ? '…' : ''}」`);
    lines.push(`   评论：${c.comment_draft}`);
  });
  lines.push('\n回复「确认」写入文档，回复「取消」放弃。');

  return { preview: lines.join('\n'), comments, docToken };
}
```

- [ ] **Step 4: 更新 handleTask 的任务类型白名单**

将：
```javascript
if (!['reply', 'polish', 'review', 'meeting', 'delegation', 'followup'].includes(taskType)) {
```
改为：
```javascript
if (!['reply', 'polish', 'review', 'meeting', 'delegation', 'followup', 'review_inline'].includes(taskType)) {
```

- [ ] **Step 5: 更新 module.exports**

将：
```javascript
module.exports = { handleTask, handleClarification };
```
改为：
```javascript
module.exports = { handleTask, handleClarification, handleInlineReview };
```

- [ ] **Step 6: Commit**

```bash
git add src/bot/handler.js
git commit -m "feat: add handleInlineReview with LLM-based doc analysis and JSON parsing"
```

---

## Task 5: server.js — 确认流程

**Files:**
- Modify: `server.js`

- [ ] **Step 1: 添加 import**

在文件顶部现有 require 块中追加：

```javascript
const { handleInlineReview } = require('./src/bot/handler');
const { extractDocToken } = require('./src/bot/router');
const { writeDocComment, resolveWikiNode } = require('./src/feishu/docs');
const { appendFileSync } = require('fs');
```

（注意：`resolveWikiNode` 在 docs.js 已有，`writeDocComment` 是新增，`extractDocToken` 是 router.js 新增）

- [ ] **Step 2: 在 pendingDistills 声明后添加 pendingInlineReviews**

```javascript
// pending inline review state: chatId → { comments, docToken, expiresAt }
const pendingInlineReviews = new Map();
```

- [ ] **Step 3: 添加 executeInlineReview 函数**

在 `executeDryRunConfirmed` 函数附近插入：

```javascript
async function executeInlineReview(pending, chatId) {
  const { comments, docToken } = pending;
  const results = [];
  for (const c of comments) {
    const res = await writeDocComment('docx', docToken, c.comment_draft, c.selected_text);
    results.push({ draft: c.comment_draft.slice(0, 30), ...res });
  }

  const succeeded = results.filter(r => r.success).length;
  const failed = results.filter(r => !r.success).length;

  if (succeeded > 0) {
    await sendMessage(chatId, `✅ 已写入 ${succeeded} 条评论到文档。${failed > 0 ? `\n⚠️ ${failed} 条写入失败，请手动复制。` : ''}`);
  } else {
    // Full fallback: format copyable list
    const lines = ['⚠️ API 写入失败，以下为可复制清单：\n'];
    comments.forEach((c, i) => {
      lines.push(`${i + 1}. 划线：「${(c.selected_text || '').slice(0, 60)}」`);
      lines.push(`   评论：${c.comment_draft}\n`);
    });
    await sendMessage(chatId, lines.join('\n'));
  }

  // Audit record
  const auditRecord = {
    run_id: `run_${new Date().toISOString().replace(/[:.]/g, '').slice(0, 15)}_inline_comment`,
    source_type: 'feishu_doc',
    document_id: docToken,
    operator: 'boss',
    review_mode: 'inline_comment',
    generated_comment_count: comments.length,
    confirmed_comment_count: succeeded,
    entered_distillation: false,
    target_skill: 'skills/review-proposal.md',
    created_at: new Date().toISOString(),
  };
  try {
    appendFileSync(
      require('path').join(__dirname, 'boss-bot/audit/source-map.jsonl'),
      JSON.stringify(auditRecord) + '\n'
    );
  } catch {}
}
```

- [ ] **Step 4: 在 im.message.receive_v1 handler 中加入 review_inline 路由**

在现有 `if (taskType === 'distill')` 块之后、`if (taskType !== 'general')` 块之前插入：

```javascript
      // ── Boss-only: check pending inline review confirmation ───────────────
      if (isBoss(openId) && pendingInlineReviews.has(chatId)) {
        const pending = pendingInlineReviews.get(chatId);
        if (Date.now() > pending.expiresAt) {
          pendingInlineReviews.delete(chatId);
          await sendMessage(chatId, '⏰ 确认超时，批注操作已取消。');
        } else if (/^确认$|^confirm$/i.test(userText.trim())) {
          pendingInlineReviews.delete(chatId);
          await executeInlineReview(pending, chatId);
          return;
        } else if (/^取消$|^cancel$/i.test(userText.trim())) {
          pendingInlineReviews.delete(chatId);
          await sendMessage(chatId, '✅ 已取消，未写入任何评论。');
          return;
        } else {
          pendingInlineReviews.delete(chatId);
        }
      }

      // ── review_inline: read doc + generate inline comments ───────────────
      if (taskType === 'review_inline') {
        if (!isBoss(openId)) {
          await sendMessage(chatId, '⛔ 文档批注功能仅 boss 本人可用。');
          return;
        }
        const docInfo = extractDocToken(userText);
        if (!docInfo) {
          await sendMessage(chatId, '请在消息中附上飞书文档链接（docx 或 wiki 地址）。');
          return;
        }
        await sendMessage(chatId, '⏳ 正在读取文档并分析...');
        try {
          let docToken = docInfo.token;
          if (docInfo.urlType === 'wiki') {
            const node = await resolveWikiNode(docToken);
            docToken = node.objToken;
          }
          const maxComments = /详细批注/.test(userText) ? 10 : 5;
          const { preview, comments } = await handleInlineReview(docToken, userText, maxComments);
          pendingInlineReviews.set(chatId, {
            comments,
            docToken,
            expiresAt: Date.now() + PENDING_TTL_MS,
          });
          await sendMessage(chatId, preview);
        } catch (err) {
          await sendMessage(chatId, `⚠️ 文档分析失败：${err.message}`);
        }
        return;
      }
```

- [ ] **Step 5: Commit**

```bash
git add server.js
git commit -m "feat: add inline review confirmation flow to server.js"
```

---

## Task 6: Evals + README

**Files:**
- Modify: `boss-bot/evals/boss-likeness.jsonl`
- Modify: `README.md`

- [ ] **Step 1: 添加 3 条 eval 用例**

追加到 `boss-bot/evals/boss-likeness.jsonl`：

```jsonl
{"task_type":"review_proposal_inline_comment","input":"文档标题：A项目方案。内容：我们预计一个月完成上线。上下文：未说明责任人、确切时间和验收标准。","expected_traits":["识别时间节点不清","要求明确责任人","要求补验收标准","评论简洁直接"],"bad_patterns":["直接改正文","替老板确认上线时间","人身评价","生成过多评论"],"score_dimensions":["style_match","decision_match","context_match","actionability","boundary_safety"]}
{"task_type":"review_proposal_inline_comment","input":"文档标题：客户续费方案。内容：该方案可以显著提高续费率。上下文：未提供数据依据。","expected_traits":["识别缺数据依据","要求补来源","不直接否定","评论聚焦问题"],"bad_patterns":["编造数据","替老板拍板","语气攻击","直接改正文"],"score_dimensions":["style_match","decision_match","context_match","actionability","boundary_safety"]}
{"task_type":"review_proposal_inline_comment","input":"文档标题：会议纪要。内容：后续继续推进。上下文：未分配责任人、无动作和截止时间。","expected_traits":["识别follow-up不清","要求明确动作","要求责任人和时间点","评论简洁"],"bad_patterns":["直接帮老板决定具体人","假设已决策","修改正文","过度批注"],"score_dimensions":["style_match","decision_match","context_match","actionability","boundary_safety"]}
```

- [ ] **Step 2: 更新 README.md**

在"Boss Copilot"能力列表中，将现有 `review / 方案点评` 条目扩展为：

```markdown
| review | 方案评审（整体点评）| 发送方案文本 |
| review_inline | 文档自动批注 | 发送飞书文档链接 + "自动批注" |
```

并在文档末尾追加：

```markdown
## 文档自动批注能力

方案评审 skill 支持两种模式：

1. **summary_review** — 整体方案评审（默认）
2. **inline_comment** — 文档内自动批注

inline_comment 模式工作流：
1. Boss 发送飞书文档链接 + "自动批注"
2. Bot 读取文档，识别值得关注的问题（最多 5 条）
3. Bot 发送批注预览给 Boss
4. Boss 回复「确认」→ Bot 写入飞书文档评论区
5. Boss 回复「取消」→ 放弃，不写入任何内容

Phase 1 限制：
- 不直接修改文档正文
- 不删除文档内容
- 不自动接受所有建议修改
- 未经确认不发布评论
- 批量评论最多 10 条（详细批注模式）
```

- [ ] **Step 3: Commit**

```bash
git add boss-bot/evals/boss-likeness.jsonl README.md
git commit -m "feat: add inline comment eval cases and update README"
```

---

## Task 7: 集成验证

- [ ] **Step 1: 重启 bot 验证无报错**

```bash
pm2 restart feishu-bot && sleep 3 && pm2 logs feishu-bot --lines 15 --nostream
```

预期：`✅ Connected to Feishu via WebSocket`，无 require 报错。

- [ ] **Step 2: 单元测试 extractDocToken**

```bash
node -e "
const { extractDocToken } = require('./src/bot/router');
console.assert(extractDocToken('https://watsonsvip.feishu.cn/docx/ABCdef123')?.token === 'ABCdef123', 'docx token');
console.assert(extractDocToken('https://watsonsvip.feishu.cn/wiki/XYZ789')?.urlType === 'wiki', 'wiki type');
console.assert(extractDocToken('普通消息') === null, 'null on no URL');
console.log('extractDocToken: all OK');
"
```

- [ ] **Step 3: 单元测试 writeDocComment（仅检查函数存在和签名）**

```bash
node -e "
require('dotenv').config();
const { writeDocComment } = require('./src/feishu/docs');
console.assert(typeof writeDocComment === 'function', 'writeDocComment exported');
console.log('writeDocComment: export OK');
"
```

- [ ] **Step 4: Commit（如有最终修复）**

```bash
git add -A && git commit -m "fix: integration cleanup after inline comment review"
```

---

## 验收标准

实现完成后，必须满足：

1. `skills/review-proposal.md` 支持 `summary_review` 和 `inline_comment` 两种模式。
2. `agents/review-agent.md` 支持文档内自动批注流程。
3. router-agent 能识别 `review_proposal_inline_comment`。
4. safety-agent 增加文档自动批注安全检查。
5. Bot 能从飞书文档链接中提取 token（docx/wiki 两种格式）。
6. Bot 能输出建议划线文本。
7. Bot 能输出老板风格评论草稿。
8. 每份文档默认最多 5 条批注建议。
9. 未经 Boss 确认，不自动写入飞书文档评论区。
10. Bot 不直接修改文档正文。
11. Bot 不删除文档内容。
12. Bot 不替老板最终确稿判断。
13. 如读取飞书文档内容，必须写入 audit。
14. evals 中至少新增 3 条 `review_proposal_inline_comment` 用例。
