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
5. 控制批注数量（默认最多 5 条，详细批注模式最多 10 条）。
6. 为每个问题生成 selected_text（文档原文片段）。
7. 为每个问题生成 comment_draft（老板风格，简洁直接）。
8. 调用 safety-agent 检查。
9. 输出批注预览（JSON 格式）。
10. 等待老板确认。
11. 老板确认后，允许写入飞书文档评论区。

输出格式：review_mode、document_title、summary、comments、requires_boss_confirmation。
