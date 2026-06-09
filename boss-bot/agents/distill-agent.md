# Distill Agent

## 两种工作模式

### 模式 A：实时蒸馏（Bot 触发）

Bot 收到"蒸馏"指令时触发，调用 `src/soul/updater.js`：

- 读取指定群/文档/会议纪要
- LLM 提取洞察，追加到 soul 文件
- 适用场景：特定事件后的即时记录（会议、决策、方案）

### 模式 B：历史校验（脚本触发）

`node scripts/calibrate.js --batch=N` 触发：

- 批量读取历史消息，只分析郑伟发言
- LLM 校验 hypothesis → supported / contradicted / insufficient
- 新发现的稳定规律作为新条目追加
- 适用场景：初始化阶段、定期数据校准

## 分流规则（两种模式共用）

- 表达风格 → soul/style.md
- 决策方式 → soul/decision.md
- 管理方式 → soul/management.md
- 沟通方式 → soul/communication.md
- 禁忌边界 → soul/taboos.md
- 项目事实 → memory/projects.md
- 人员职责 → memory/people-map.md
- 术语 → memory/glossary.md
- 执行步骤 → skills/*.md

## 每次蒸馏必须输出

- 读取范围
- 涉及 source_id
- 更新文件
- 更新内容摘要
- 证据状态变更（hypothesis → supported/contradicted/insufficient）
- audit 记录位置

## 约束

- 不做无限制读取
- 每次执行前必须 dry-run
- 用户确认后才能正式读取
- 原始消息正文不持久化，只保存 source_id、hash、sanitized_summary
- 没有 evidence 不得将 hypothesis 改为 supported
