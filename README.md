# feishu-claude-bot

飞书 Bot，包含两套能力：

1. **通用对话 + Skill 生成** — 基于 Claude CLI，面向所有用户
2. **Boss Copilot** — 基于 Anthropic SDK，仅限 `BOSS_OPEN_ID` 用户，提供回复代写、表达润色、方案点评、会议纪要提炼四项能力

---

## 快速开始

### 1. 环境配置

```bash
cp .env.example .env
# 必填：
# FEISHU_APP_ID / FEISHU_APP_SECRET  — 飞书开放平台 App 凭证
# BOSS_OPEN_ID                        — 老板的 Feishu open_id（仅老板功能需要）
# ANTHROPIC_API_KEY                   — Claude API Key（Boss Copilot 需要）
# ANTHROPIC_MODEL                     — 默认 claude-opus-4-8
```

### 2. 安装依赖

```bash
npm install
```

### 3. 启动 Bot

```bash
npm start
# 或
node server.js
```

Bot 通过 WebSocket 长连接与飞书通信，无需公网 IP 或 Webhook 配置。

---

## Boss Copilot

### 本地 CLI 测试（不需要飞书）

```bash
node cli-boss.js reply "背景：同事催项目进度，我想说这周五给结果"
node cli-boss.js polish "大家看下这个能不能做"
node cli-boss.js review "方案：Q3上线推荐功能，投入3人2个月"
node cli-boss.js meeting "今天讨论了预算，决定由张三负责削减方案，周五提交"
node cli-boss.js auto "帮我润色一下这段话：xxx"   # 自动判断任务类型
```

### 任务类型（自动识别）

| 类型 | 触发词示例 |
|------|----------|
| reply | 帮我回复、代写回复、怎么回 |
| polish | 润色、改写、优化表达 |
| review | 点评方案、看汇报、评价计划 |
| meeting | 会议纪要、提炼会议、妙记 |
| distill | /distill、蒸馏 |
| general | 其他问答 |

### 蒸馏命令

在飞书中向 Bot 发送：

```
/distill --file=decision --chat=oc_xxx --days=90 --keyword=方案评审 --reason=提炼项目决策标准
```

| 参数 | 说明 |
|------|------|
| `--file` | 要更新的 soul 文件（identity/style/decision/communication/taboos/examples） |
| `--chat` | 飞书群 chat_id |
| `--days` | 往前读取天数 |
| `--keyword` | 消息关键词过滤 |
| `--doc` | 飞书文档 token |
| `--minutes` | 飞书妙记 token |
| `--reason` | 本次蒸馏原因（写入 changelog） |

蒸馏不保存原始消息，只将提炼出的风格/原则追加到 boss-soul 文件。

---

## Boss Soul 文件

位于 `boss-soul/`，定义老板的风格和判断原则：

| 文件 | 内容 |
|------|------|
| `identity.md` | 身份、角色、业务目标、管理风格 |
| `style.md` | 表达风格：语气、长度、措辞 |
| `decision.md` | 决策原则：优先级、风险偏好、ROI |
| `communication.md` | 面向不同对象的沟通方式 |
| `taboos.md` | 禁止事项 |
| `examples.md` | 精选脱敏案例 |
| `changelog.md` | 每次 Soul 变更记录 |

初始化：直接编辑上述文件，或通过蒸馏命令从飞书历史数据自动提炼。

---

## 运行评测

```bash
npm run eval
```

LLM-as-judge 对每条案例打分，通过率低于 60% 时退出码非零。报告保存在 `evals/report-<date>.json`。

---

## 运行测试

```bash
npm test
```

---

## 权限说明

- 只有 `BOSS_OPEN_ID` 对应的用户可以使用 Boss Copilot 功能
- 其他用户的消息走原有通用对话逻辑
- 蒸馏操作自动记录到 `boss-soul/changelog.md`
- Bot 不会替老板做最终审批、承诺或人事决定

---

## 飞书开放平台配置

1. 创建企业自建应用
2. 开启权限：
   - `im:message`（读写消息）
   - `im:message.receive_v1`（接收消息事件）
   - `contact:user.base:readonly`（读取用户信息，可选）
   - `drive:drive:readonly`（读文档，蒸馏需要）
   - `minutes:minute:readonly`（读妙记，蒸馏需要）
3. 开启「长连接接收事件」模式

---

## 项目结构

```
feishu-claude-bot/
├── boss-soul/          # 老板风格文件（核心，需初始化）
├── prompts/            # Boss Copilot 任务 prompt 模板
├── evals/              # 评测案例
├── src/
│   ├── feishu/         # 飞书 API 封装（消息/文档/妙记）
│   ├── bot/            # Boss 路由、权限、任务处理器
│   ├── soul/           # Soul 加载和蒸馏
│   ├── llm/            # Anthropic SDK 封装
│   └── eval/           # 评测运行器
├── tests/              # 单元测试
├── server.js           # WebSocket Bot 主入口
├── cli-boss.js         # Boss Copilot 本地测试入口
└── start.sh
```
