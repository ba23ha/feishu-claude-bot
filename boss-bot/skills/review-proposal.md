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
