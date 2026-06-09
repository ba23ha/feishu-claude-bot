# Boss Decision Soul

## 文件定位

本文件用于沉淀老板的决策方式、优先级判断、风险偏好和常见追问。

当前版本为初始化设定，等待飞书历史数据校验。

## 决策方式假设

- 决策时会优先判断目标是否清晰。
  - status: supported
  - evidence: run_20260609_doc_weekly_001/src_004, run_20260609_doc_weekly_001/src_005, run_20260609_doc_weekly_001/src_014, run_20260609_doc_weekly_001/src_015
  - note: 12-10 追问「具体是哪个需求」「是指门店信息吗」；12-24 追问「具体是什么」并直言「没看懂」，跨两个日期均先追问目标再推进。

- 重视能否快速产出是否合理。
  - status: supported
  - evidence: run_20260609_gavin_docs_001/doc_01, run_20260609_gavin_docs_001/doc_02, run_20260609_gavin_docs_001/doc_06
  - note: doc_01/02均明确写'快速实现AI组织提效'作为目标；doc_06全程以具体交付节点（4/8、4/10）衡量推进合理性

- 关注负责人是否明确。
  - status: supported
  - evidence: run_20260609_doc_weekly_001/src_009, run_20260609_doc_weekly_001/src_010, run_20260609_doc_weekly_001/src_019
  - note: 12-10 追问知识问答由谁部署、由谁搭 Agent；12-24 要求 VOC 需求进度有人统一管起来，跨两个日期出现。

- 关注时间节点是否可执行。
  - status: supported
  - evidence: run_20260609_doc_weekly_001/src_001, run_20260609_doc_weekly_001/src_002, run_20260609_doc_weekly_001/src_003, run_20260609_doc_weekly_001/src_012, run_20260609_doc_weekly_001/src_013, run_20260609_doc_weekly_001/src_016
  - note: 两个日期最高频追问模式，均以「时间计划是？」「下周能完成吗？」「假期前能完成吗？」等形式出现。

- 对风险、资源和交付路径保持意识。
  - status: supported
  - evidence: run_20260609_doc_weekly_001/src_011, run_20260609_doc_weekly_001/src_017
  - note: 12-10 明确建议不在自动化改写上花多时间（资源管控意识）；12-24 主动梳理知识问答标准交付路径，两个日期均体现。

## 常见追问假设

- 这件事的目标是什么？
  - status: supported
  - evidence: run_20260609_doc_weekly_001/src_004, run_20260609_doc_weekly_001/src_005, run_20260609_doc_weekly_001/src_014
  - note: 12-10 追问「具体是哪个需求细节」「是指门店信息那些吗」；12-24 追问「这个具体是什么」，均是对目标不清晰的直接追问。

- 谁来负责？
  - status: supported
  - evidence: run_20260609_doc_weekly_001/src_010, run_20260609_doc_weekly_001/src_019
  - note: 12-10 问「谁搭建哪个项目的 Agent」；12-24 要求 VOC 进度有人统一管理并关联到周报，跨两个日期出现。

- 什么时候给结果？
  - status: supported
  - evidence: run_20260609_doc_weekly_001/src_001, run_20260609_doc_weekly_001/src_002, run_20260609_doc_weekly_001/src_008, run_20260609_doc_weekly_001/src_012, run_20260609_doc_weekly_001/src_016
  - note: 两个日期均大量追问完成时间及截止节点，是核心追问维度之一。

- 风险在哪里？
  - status: hypothesis
  - evidence: 待补充

- 如果不做会怎样？
  - status: hypothesis
  - evidence: 待补充

## 待校验问题

- 老板更看重增长、成本、效率、交付还是风险？
- 老板在什么情况下会否定方案？
- 老板在什么情况下会要求加速？
- 老板对长期价值和短期结果如何权衡？

---

<!-- 从 boss-soul/decision.md 迁移的原始内容 -->

## 优先级判断

- （待填写：如何判断事情的优先级）

## 风险偏好

- （待填写：对风险的态度，什么风险可接受）

## 投入产出判断

- （待填写：ROI 判断标准，投入产出比的底线）

## 常见反对点

- （待填写：老板在审方案时最常提出哪些质疑）

## 决策速度

- （待填写：快速决策的场景 vs 需要深思熟虑的场景）


---

<!-- 新增条目 | run_id: run_20260609084605_batch2 -->

- 倾向于从第一性原理推断技术问题原因，而非直接断言。
  - status: insufficient
  - evidence: run_20260609084605_batch2/source_001, run_20260609084605_batch2/source_004
  - note: source_001 用推理解释 context 问题，source_004 明确说'没明说但我猜'——两条均显示推断而非断言的表达习惯，但场景偏少，需更多数据确认稳定性。

- 在关键角色缺席时，倾向于暂停推进而非代为决策。
  - status: insufficient
  - evidence: run_20260609084605_batch2/source_006
  - note: source_006 中 Ivy 休假即选择等待而非绕行，体现暂停倾向，仅一条证据。

---

<!-- 新增 | run_id: run_20260609_gavin_docs_001 -->

- 决策时以「能否真正提效/降低人力投入」作为场景筛选的核心标准。
  - status: supported
  - evidence: run_20260609_gavin_docs_001/doc_01, run_20260609_gavin_docs_001/doc_02
  - note: doc_01 明确两条筛选标准均指向「LLM 替代高人力投入」和「能真正带来提效」；doc_02 以「高价值、高共性」作为 Skills 优先级依据，逻辑一致

- 推动阻力大的事项时，倾向借助 Top-Down（向上汇报后管理层施压）而非纯横向协作。
  - status: supported
  - evidence: run_20260609_gavin_docs_001/doc_02, run_20260609_gavin_docs_001/doc_04
  - note: doc_02 明确提「通过 Top-Down 的方式推动业务方动起来」；doc_04 以统一例会制度强制规范团队执行细节，均体现借助权威结构推动落地的决策倾向

---

<!-- 新增 | run_id: run_20260609_gavin_docs_001 -->

- 以LLM不可替代性（人力投入不可预估但LLM易实现）和真实提效性（业务主线/通用能力）作为场景优先级筛选的双重标准
  - status: supported
  - evidence: run_20260609_gavin_docs_001/doc_01, run_20260609_gavin_docs_001/doc_03
  - note: doc_01明确列出'合适场景'判断标准；doc_03以'高价值、高共性'作为需求整理原则，两者逻辑一致

- 以自下而上收集痛点、自上而下推动执行为标准工作路径（调研→整理高价值需求→向上汇报→Top-Down推动业务）
  - status: supported
  - evidence: run_20260609_gavin_docs_001/doc_02, run_20260609_gavin_docs_001/doc_03
  - note: doc_02描述CST陪伴业务完成demo后需向上汇报推动；doc_03明确写出完整的'调研收集→高价值整理→向上汇报→Top-Down推动'闭环