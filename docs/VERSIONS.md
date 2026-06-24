# 演示文档版本索引

生产站点：https://quiet-taiyaki-6a325a.netlify.app  
草稿预览：`https://<deploy-id>--quiet-taiyaki-6a325a.netlify.app/<文件名>`

---

## 当前工作版本

| 文件 | 描述 |
|------|------|
| `index.html` | 当前主文档（12页，06-11为旧版叙事，是 plan-a/b 的生成基础） |
| `architecture-report.html` | 与 index.html 始终保持同步的镜像版本 |
| `index-plan-a.html` | **方案A**：06移至08后 · 重设计为Bot设计/结构验证/演进方向三段式 · 09-11改为决策支撑叙事 |
| `index-plan-b.html` | **方案B**：06下半改为Skill场景规划 · 09-11聚焦架构探索 |

---

## 快照存档（index-pre-*）

时间从旧到新，每个文件是「做某改动前」的状态。

| 文件 | 页数 | 关键特征 |
|------|------|---------|
| `index-pre-restructure.html` | 11页 | 第一次大重构前；Skills页刚加入；07/08是独立的Agent架构+服务流程 |
| `index-pre-split-agent.html` | 11页 | agent-arch拆分前；Eval为12场景合并大表；perm包含Bot定位+权限+配置管理三合一 |
| `index-pre-merge-perm-decision.html` | 12页 | 权限决策并入arch页前；09/10/11已是选型对比三联页 |
| `index-pre-fix06.html` | 12页 | 06页布局修复前；双层权限已独立成页 |
| `index-pre-0406.html` | 14页 | 04-06页重构前；有独立的「当前测试数据缺口」页；日报/批注eval各一页 |
| `index-pre-merge0708.html` | 13页 | 07+08合并前；Agent架构与服务流程各占一页 |
| `index-pre-lr.html` | 11页 | review_inline eval页加入前；只有日报eval |
| `index-pre-eval-rebuild.html` | 12页 | eval页重建前；有「维度对比双列视图」实验页 |
| `index-pre-scheme-b.html` | 12页 | scheme-b方案前；eval测试结果页结构不同 |
| **`index-pre-plan-ab.html`** | **12页** | **plan-a/b生成前的基础版本，与 index.html 内容一致** |

> ⭐ **你要找的版本**：`index-pre-plan-ab.html`
> 09页=「技术选型 & 方案优势」（Claude Code CLI vs LangChain详细对比）
> 10页=「与主流 Agent 框架对比」（4框架×8维度大表）
> 11页=「架构差距与运维局限」（优势+差距+4条运维局限清单）
> 草稿预览：https://6a37a897e467cdd5d8f89fff--quiet-taiyaki-6a325a.netlify.app/index-pre-plan-ab.html

---

## 早期架构报告存档（archive-v*）

这批文件是演示文档合并前、独立的「架构报告」页面，仅包含架构相关页面（无hero/skills/eval）。

| 文件 | 页数 | 关键特征 |
|------|------|---------|
| `archive-v1.html` | 5页 | 最早版本；三端架构+双层权限+服务流程+决策+选型对比 |
| `archive-v2.html` ~ `archive-v9.html` | 5页 | 布局与内容的渐进迭代，结构基本一致 |
| `archive-v9-arch.html` | 5页 | v9的arch页单独调整版 |
| `archive-v10.html` | 5页 | 最后一版独立架构报告；「当前方案优势与局限」内容微调 |
| `archive-v10-arch.html` | 5页 | v10的arch页单独调整版 |
| `archive-pre-overview.html` | — | 概览页加入前的存档 |
| `archive-pre-overview-report.html` | — | 概览报告页的早期版本 |

---

## 版本管理说明

- **命名规则**：`index-pre-<改动名>.html` = 做该改动前的快照
- **生成脚本**：`scripts/` 下的 Python 脚本记录每次改动的具体变换，可配合对应 pre-* 文件重现任意版本
- **Netlify**：每次 `netlify deploy` 生成永久 draft URL，用 `restoreSiteDeploy` API 可回滚生产版本
