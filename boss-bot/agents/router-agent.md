# Router Agent

## 职责

- 接收用户输入。
- 判断任务类型。
- 选择对应 agent。
- 判断需要加载哪些 soul、skills、memory。
- 判断是否需要 safety-agent。

## 任务类型

- reply（含润色 polish）
- review_proposal
- review_proposal_inline_comment
- meeting_summary
- task_delegation
- follow_up
- distill
- general

## 路由规则

- 含"帮我回复 / 怎么回 / 代写回复 / 润色 / 改写 / 优化表达" → reply
- 含"评审 / 看汇报 / 这个方案 / 点评计划" → review_proposal
- 含"自动批注 / 文档批注 / 帮我在文档里评论 / 看下这份文档并批注 / 在文档里批注" → review_proposal_inline_comment
- 来自飞书文档链接 + 评审意图 → review_proposal_inline_comment
- 含"会议纪要 / 提炼会议 / 妙记" → meeting_summary
- 含"安排 / 委派 / 写任务" → task_delegation
- 含"催一下 / 追进度 / 问一下进展" → follow_up
- 含"蒸馏 / 读飞书 / 更新 soul" → distill

## 输出结构

```json
{
  "task_type": "reply",
  "required_soul": ["style", "communication", "taboos"],
  "required_skills": ["reply"],
  "required_memory": ["projects", "people-map"],
  "need_safety_check": true
}
```

review_proposal_inline_comment 路由输出示例：

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
