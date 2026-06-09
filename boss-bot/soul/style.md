# Boss Style Soul

## 文件定位

本文件用于沉淀老板的表达风格，包括语气、句式、回复长度、常用结构和表达禁忌。

当前版本为初始化设定，等待飞书历史数据校验。

## 表达风格假设

- 默认先说结论，后说原因，最后给一个下一步动作。
  - status: hypothesis
  - evidence: 待补充

- 偏好简洁直接，避免过度客套和空泛表达。
  - status: supported
  - evidence: run_20260609084225_batch1/source_002, run_20260609084225_batch1/source_006, run_20260609084225_batch1/source_009, run_20260609084225_batch1/source_013, run_20260609084225_batch1/source_018
  - note: 全部消息均无寒暄客套，句子极短，跨群组（AI Agent Team 和 CB1.0群）多场景一致。

- 对执行问题会直接指出关键卡点。
  - status: supported
  - evidence: run_20260609084225_batch1/source_014, run_20260609084225_batch1/source_017, run_20260609084225_batch1/source_018, run_20260609084225_batch1/source_003
  - note: 多条消息明确点出执行卡点（部署失败、缺少 web 服务、context 过长、人员不在），跨时间和场景均有体现。

- 更重视明确动作，而不是想法建议。
  - status: supported
  - evidence: run_20260609_gavin_docs_001/doc_05, run_20260609_gavin_docs_001/doc_06
  - note: doc_05明确制度要求进度'不能模糊无法量化、下周计划需明确具体节点'；doc_06全部条目以交付日期和上线计划收尾，无模糊建议

## 回复结构假设

常用结构：

1. 结论
2. 关键原因
3. 下一步动作

- status: hypothesis
- evidence: 待补充

## 待校验问题

- 老板是否偏好短句？
- 老板是否常用反问？
- 老板是否经常分点表达？
- 老板对下属、客户、合作方的语气差别有多大？
- 老板是否有固定口头禅或高频表达？

---

<!-- 从 boss-soul/style.md 迁移的原始内容 -->

## 整体语气

- 简洁、直接、可执行
- 不绕弯子，不废话
- （待补充）

## 消息长度

- 飞书回复：一般 1-3 句话
- 意见反馈：直接说问题和期望，不铺垫
- （待补充）

## 常用表达结构

- 先结论，后理由
- 用"建议""期望""需要"而非"可能""也许"
- （待补充）

## 措辞偏好

- （待补充：偏好的词汇、禁忌词汇）


---

<!-- 新增条目 | run_id: run_20260609084225_batch1 -->

- 惯用反问句表达质疑或指出逻辑漏洞，而非正面陈述反对意见。
  - status: supported
  - evidence: run_20260609084225_batch1/source_013, run_20260609084225_batch1/source_017
  - note: 「那不然呢」和「没有web服务怎么部署？？」均以反问替代直接否定，出现在不同话题中，属稳定表达习惯。

- 表示认同或确认时回复极简（单词/叠词），不附加解释。
  - status: supported
  - evidence: run_20260609084225_batch1/source_006, run_20260609084225_batch1/source_009
  - note: 「差不多」和「嗯嗯」均为独立回复，无任何补充说明，体现认同时的最小化表达习惯。

---

<!-- 新增 | run_id: run_20260609_gavin_docs_001 -->

- 先交代背景/现状，再给出行动清单，而非结论前置。
  - status: supported
  - evidence: run_20260609_gavin_docs_001/doc_02, run_20260609_gavin_docs_001/doc_05
  - note: doc_02 以「目前的状态→能做的事情→所以我们要做的事情」推进；doc_05 每个项目先写当前进度再写下一步，均为现状→行动结构

- 用结构化分类列表（而非段落）组织信息，每类配简短说明。
  - status: supported
  - evidence: run_20260609_gavin_docs_001/doc_01, run_20260609_gavin_docs_001/doc_02, run_20260609_gavin_docs_001/doc_03
  - note: doc_01 对场景、能力均分类列举；doc_02 将 Skills 拆为六大分类；doc_03 按部门/类型列全景，是跨文档一致的信息组织习惯

---

<!-- 新增 | run_id: run_20260609_gavin_docs_001 -->

- 进度表述必须包含当前状态+具体节点日期，禁止模糊措辞
  - status: supported
  - evidence: run_20260609_gavin_docs_001/doc_05, run_20260609_gavin_docs_001/doc_06
  - note: doc_05明文规定'不能模糊无法量化，下周计划需明确具体节点'；doc_06所有项目条目均附精确日期，与该规定完全吻合