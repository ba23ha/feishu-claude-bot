# feishu-claude-bot

飞书 Bot，包含两套能力：

1. **通用对话 + Skill 生成** — 基于 Claude CLI，面向所有用户
2. **Boss Copilot** — 仅限授权用户，提供回复代写、表达润色、方案点评、会议纪要提炼、数据蒸馏五项能力

---

## 用户角色

| 角色 | 说明 | 可用功能 |
|------|------|---------|
| **Boss（郑伟）** | `BOSS_OPEN_ID` 对应账号 | 全部功能，含蒸馏 |
| **其他用户** | 任何人私聊 Bot | reply / polish / review / meeting / 通用对话 |
| **开发者** | 通过 Claude Code CLI 迭代功能 | 不经由飞书 Bot 交互 |

---

## 快速开始

### 1. 环境配置

```bash
cp .env.example .env
# 必填：
# FEISHU_APP_ID / FEISHU_APP_SECRET  — 飞书开放平台 App 凭证
# BOSS_OPEN_ID                        — 郑伟的 Feishu open_id
```

LLM 通过本机 `claude` CLI（Claude Code）调用，无需 Anthropic API Key。

### 2. 安装依赖

```bash
npm install
```

### 3. 启动 Bot

```bash
npm start
```

Bot 通过 WebSocket 长连接与飞书通信，无需公网 IP 或 Webhook 配置。

---

## Boss Copilot

### 任务类型

| 类型 | 触发词示例 | 可用用户 |
|------|----------|----|
| reply | 帮我回复、代写回复、怎么回 | 所有用户 |
| polish | 润色、改写、优化表达 | 所有用户 |
| review | 点评方案、看汇报、评价计划 | 所有用户 |
| review_inline | 飞书文档链接 + 自动批注 | 仅 Boss |
| meeting | 会议纪要、提炼会议、妙记 | 所有用户 |
| followup | 催一下、追进度、问进展 | 所有用户 |
| delegation | 帮我安排、委派任务 | 所有用户 |
| general | 其他问答 | 所有用户 |

### 文档自动批注（review_inline，仅 Boss）

Bot 读取飞书文档，自动识别值得关注的问题，生成老板风格批注建议。

**使用方式：**
在飞书向 Bot 发送文档链接，附加"自动批注"：
```
https://xxx.feishu.cn/docx/TOKEN 自动批注
```

**工作流：**
1. Bot 读取文档 → LLM 分析 → 发送批注预览（最多 5 条）
2. 回复「确认」→ Bot 写入飞书文档评论区
3. 回复「取消」→ 放弃，不写入任何内容

**限制（Phase 1）：**
- 不直接修改文档正文
- 不自动接受所有建议
- 未确认不发布评论
- 单次最多 5 条（详细批注模式最多 10 条）

### 蒸馏（仅 Boss）

蒸馏从飞书历史数据提炼郑伟的风格原则，追加到 `boss-soul/` 文件，全程有审计日志。

**飞书中发送：**
```
/distill --file=style --chat=oc_xxx --days=90 --reason=提炼沟通风格
```

**CLI 执行（开发者代操作）：**
```bash
node cli-boss.js distill --file=style --chat=oc_xxx --days=90 --reason=提炼沟通风格
```

| 参数 | 说明 |
|------|------|
| `--file` | 要更新的 soul 文件（identity/style/decision/communication/taboos/examples） |
| `--chat` | 飞书群 chat_id |
| `--days` | 往前读取天数 |
| `--keyword` | 消息关键词过滤（可选） |
| `--doc` | 飞书文档 token（可选） |
| `--minutes` | 飞书妙记 token（可选） |
| `--reason` | 本次蒸馏原因（写入 changelog） |
| `--yes` | 跳过终端确认（CLI 专用） |

---

## Boss 授权（OAuth）

蒸馏功能需要以郑伟身份读取消息，无需将 Bot 拉入群聊。

```bash
# 1. 生成授权链接，发给郑伟
node cli-boss.js auth-url

# 2. 郑伟浏览器授权后，将跳转 URL 中的 code 值发回
# 3. 完成授权（一次性操作，refresh token 自动续期 30 天）
node cli-boss.js auth-callback <code>

# 查看郑伟所在的所有群聊
node cli-boss.js list-chats
```

---

## CLI 本地测试

```bash
# 任务测试（无需飞书）
node cli-boss.js reply   "背景：同事催进度，我想说这周五给结果"
node cli-boss.js polish  "大家看下这个能不能做"
node cli-boss.js review  "方案：Q3上线推荐功能，投入3人2个月"
node cli-boss.js meeting "今天讨论了预算，决定由张三负责削减方案，周五提交"
node cli-boss.js auto    "帮我润色一下这段话：xxx"

# 连接验证
npm run verify
npm run verify -- --chat=oc_xxx --days=7   # 加上群消息测试
```

---

## Boss Soul 文件

位于 `boss-soul/`，定义郑伟的风格和判断原则：

| 文件 | 内容 |
|------|------|
| `identity.md` | 身份、角色、业务目标、管理风格 |
| `style.md` | 表达风格：语气、长度、措辞 |
| `decision.md` | 决策原则：优先级、风险偏好、ROI |
| `communication.md` | 面向不同对象的沟通方式 |
| `taboos.md` | 禁止事项 |
| `examples.md` | 精选脱敏案例 |
| `changelog.md` | 每次 Soul 变更记录（含 run_id，可追溯审计报告） |

---

## 飞书开放平台配置

**权限管理**中开通：
- `im:message:readonly` — 读取群消息（Bot 需在群内，或用 OAuth 用户 token）
- `contact:contact.base:readonly` — 解析用户姓名
- `docx:document:readonly` — 读取飞书文档（蒸馏文档时需要）
- `minutes:read` — 读取妙记（蒸馏会议记录时需要）

**事件与回调**：订阅 `im.message.receive_v1`，使用「长连接」模式。

---

## 运行测试

```bash
npm test       # 单元测试（44 个）
npm run eval   # LLM-as-judge 评测，报告保存至 evals/report-<date>.json
```

---

## 项目结构

```
feishu-claude-bot/
├── server.js              # WebSocket Bot 主入口
├── cli-boss.js            # Boss Copilot CLI（本地测试 + 蒸馏 + 授权）
├── boss-soul/             # 郑伟风格文件（蒸馏目标，需初始化）
├── prompts/               # Boss Copilot 任务 prompt 模板
├── scripts/
│   └── verify-feishu.js   # Feishu + LLM 连接验证
├── src/
│   ├── feishu/            # Feishu API 封装（消息/文档/妙记/OAuth）
│   ├── bot/               # 路由、权限、任务处理器
│   ├── soul/              # Soul 加载、蒸馏、changelog
│   ├── audit/             # 审计：dry-run、access-log、report
│   ├── llm/               # LLM 调用（claude CLI 子进程）
│   └── eval/              # 评测运行器
├── tests/                 # Jest 单元测试
├── evals/                 # 评测案例（jsonl）
├── audit/                 # 审计报告（gitignore，运行时生成）
└── data/                  # 运行时数据（gitignore）
```
