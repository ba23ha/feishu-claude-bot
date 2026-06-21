#!/usr/bin/env python3
"""
Scheme B: per-skill pages
- #skilleval-dr → daily_report 完整页（方法条 + 效果对比表 + eval表）
- #skilleval-lr → review_inline 完整页（效果对比表 + eval表 + 数据说明）
- #skilleval-ri → 删除
- Nav: 13 → 12
"""
import shutil, re

# ── Page 04: daily_report ─────────────────────────────────────────────────────

DR_PAGE = '''\
<!-- 3. 日报测试 -->
<div class="section" id="skilleval-dr">
  <div class="section-label">测试验证</div>
  <div class="section-title">daily_report · 日报生成</div>

  <!-- 方法条 -->
  <div style="display:flex;align-items:center;gap:10px;background:#141820;border:1px solid #1e2530;border-radius:10px;padding:10px 20px;margin-bottom:16px;flex-wrap:wrap;">
    <span style="font-size:12px;font-weight:700;color:#6b7a95;letter-spacing:1px;text-transform:uppercase;white-space:nowrap;margin-right:8px;">测试方法</span>
    <div class="flow-node" style="padding:5px 14px;font-size:13px;">同一组模拟输入</div>
    <span style="color:#2d3748;font-size:14px;">→</span>
    <div class="flow-node highlight" style="padding:5px 14px;font-size:13px;">通用模型（无 Skill）</div>
    <span style="color:#2d3748;font-size:14px;">vs</span>
    <div class="flow-node green" style="padding:5px 14px;font-size:13px;">Soul + Skill</div>
    <span style="color:#2d3748;font-size:14px;">→</span>
    <div class="flow-node" style="padding:5px 14px;font-size:13px;">对比格式 / 口吻 / 关键信息 / 禁忌词</div>
  </div>

  <!-- 效果对比表 -->
  <div style="font-size:11px;font-weight:700;color:#6b7a95;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;">核心维度对比</div>
  <div style="background:#141820;border:1px solid #1e2530;border-radius:12px;overflow:hidden;margin-bottom:14px;">
    <table style="width:100%;border-collapse:collapse;font-size:13px;">
      <thead>
        <tr style="background:#0d1018;">
          <th style="padding:8px 16px;text-align:left;color:#6b7a95;font-weight:700;font-size:11px;letter-spacing:1px;text-transform:uppercase;width:18%;">核心差异</th>
          <th style="padding:8px 16px;text-align:left;color:#8b98b0;font-weight:700;font-size:11px;width:41%;">通用模型</th>
          <th style="padding:8px 16px;text-align:left;color:#34C759;font-weight:700;font-size:11px;width:41%;">加入 Skill 后</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:10px 16px;color:#e2e8f0;font-weight:700;vertical-align:top;">格式一致性</td>
          <td style="padding:10px 16px;color:#6b7a95;vertical-align:top;line-height:1.55;">每次结构不同，有时按群分组，有时按时间排列，无固定格式</td>
          <td style="padding:10px 16px;color:#6b7a95;vertical-align:top;line-height:1.55;">固定三段式（昨日动态 → 需特别注意 → 今日行动），老板形成阅读预期</td>
        </tr>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:10px 16px;color:#e2e8f0;font-weight:700;vertical-align:top;">噪音过滤</td>
          <td style="padding:10px 16px;color:#6b7a95;vertical-align:top;line-height:1.55;">倾向"全面"，把"收到""了解""早上好"等也纳入，字数普遍 800+</td>
          <td style="padding:10px 16px;color:#6b7a95;vertical-align:top;line-height:1.55;">以「今天不看明天有没有麻烦」为过滤标准，高噪音场景仅输出 2 条有效信息</td>
        </tr>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:10px 16px;color:#e2e8f0;font-weight:700;vertical-align:top;">行动可执行度</td>
          <td style="padding:10px 16px;color:#6b7a95;vertical-align:top;line-height:1.55;">建议停留在"持续关注""跟进推进"等泛化动词，无法直接执行</td>
          <td style="padding:10px 16px;color:#6b7a95;vertical-align:top;line-height:1.55;">要求「动词 + 对象 + 目标 + 今天的原因」，如"催 Yuki 今天核对预算表漏项，6/17 截止"</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- 分隔 -->
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
    <div style="flex:1;height:1px;background:#1e2530;"></div>
    <span style="font-size:11px;font-weight:700;color:#6b7a95;letter-spacing:1.5px;text-transform:uppercase;white-space:nowrap;">Eval 测试结果（2026-06-16）</span>
    <div style="flex:1;height:1px;background:#1e2530;"></div>
  </div>

  <!-- DR eval 表 -->
  <div style="background:#141820;border:1px solid #1e2530;border-radius:12px;overflow:hidden;">
    <table style="width:100%;border-collapse:collapse;font-size:13px;">
      <thead>
        <tr style="background:#0d1018;">
          <th style="padding:8px 14px;text-align:left;color:#6b7a95;font-weight:700;font-size:11px;letter-spacing:1px;text-transform:uppercase;width:26%;">场景</th>
          <th style="padding:8px 10px;text-align:center;color:#8b98b0;font-weight:700;font-size:11px;width:8%;">通用</th>
          <th style="padding:8px 10px;text-align:center;color:#34C759;font-weight:700;font-size:11px;width:8%;">加入后</th>
          <th style="padding:8px 14px;text-align:left;color:#6b7a95;font-weight:700;font-size:11px;letter-spacing:1px;text-transform:uppercase;">关键观察</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:8px 14px;color:#e2e8f0;">
            <div style="display:flex;align-items:baseline;gap:6px;margin-bottom:2px;">
              <span style="font-size:11px;color:#4F8EF7;font-weight:700;white-space:nowrap;">DR-01</span>
              <span style="font-weight:600;">混合场景</span>
            </div>
            <div style="font-size:11px;color:#6b7a95;">紧急 + 跟踪 + 正向进展并存，验证三色分级和行动优先级</div>
          </td>
          <td style="padding:8px 10px;text-align:center;color:#8b98b0;">854</td>
          <td style="padding:8px 10px;text-align:center;color:#34C759;">517</td>
          <td style="padding:8px 14px;color:#8b98b0;">精简 40%，行动建议点名具体人和截止</td>
        </tr>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:8px 14px;color:#e2e8f0;">
            <div style="display:flex;align-items:baseline;gap:6px;margin-bottom:2px;">
              <span style="font-size:11px;color:#34C759;font-weight:700;white-space:nowrap;">DR-02</span>
              <span style="font-weight:600;">无异常日</span>
            </div>
            <div style="font-size:11px;color:#6b7a95;">全是正向进展，验证需注意和今天必做区块是否正确省略</div>
          </td>
          <td style="padding:8px 10px;text-align:center;color:#8b98b0;">463</td>
          <td style="padding:8px 10px;text-align:center;color:#34C759;">282</td>
          <td style="padding:8px 14px;color:#8b98b0;">正确省略"需注意"和"今天必做"区块</td>
        </tr>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:8px 14px;color:#e2e8f0;">
            <div style="display:flex;align-items:baseline;gap:6px;margin-bottom:2px;">
              <span style="font-size:11px;color:#FF9500;font-weight:700;white-space:nowrap;">DR-03</span>
              <span style="font-weight:600;">高噪音日</span>
            </div>
            <div style="font-size:11px;color:#6b7a95;">大量闲聊打卡，验证过滤能力，有效内容仅 2 条</div>
          </td>
          <td style="padding:8px 10px;text-align:center;color:#8b98b0;">331</td>
          <td style="padding:8px 10px;text-align:center;color:#8b98b0;">332</td>
          <td style="padding:8px 14px;color:#8b98b0;">字数相近；加入后多识别出销售承诺未对齐的隐性风险</td>
        </tr>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:8px 14px;color:#e2e8f0;">
            <div style="display:flex;align-items:baseline;gap:6px;margin-bottom:2px;">
              <span style="font-size:11px;color:#FF6B6B;font-weight:700;white-space:nowrap;">DR-04</span>
              <span style="font-weight:600;">三级群异常</span>
            </div>
            <div style="font-size:11px;color:#6b7a95;">L3 群生产系统故障，验证重大异常突破默认忽略</div>
          </td>
          <td style="padding:8px 10px;text-align:center;color:#8b98b0;">314</td>
          <td style="padding:8px 10px;text-align:center;color:#8b98b0;">305</td>
          <td style="padding:8px 14px;color:#8b98b0;">加入后额外指出无复盘方案存在再发风险</td>
        </tr>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:8px 14px;color:#e2e8f0;">
            <div style="display:flex;align-items:baseline;gap:6px;margin-bottom:2px;">
              <span style="font-size:11px;color:#FF6B6B;font-weight:700;white-space:nowrap;">DR-05</span>
              <span style="font-weight:600;">双紧急并存</span>
            </div>
            <div style="font-size:11px;color:#6b7a95;">决策悬空 + 时间风险同时出现，验证行动建议分别对应</div>
          </td>
          <td style="padding:8px 10px;text-align:center;color:#8b98b0;">651</td>
          <td style="padding:8px 10px;text-align:center;color:#34C759;">480</td>
          <td style="padding:8px 14px;color:#8b98b0;">通用模型输出 Markdown 表格；加入后两条 🔴 分别对应行动</td>
        </tr>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:8px 14px;color:#e2e8f0;">
            <div style="display:flex;align-items:baseline;gap:6px;margin-bottom:2px;">
              <span style="font-size:11px;color:#8b5cf6;font-weight:700;white-space:nowrap;">DR-06</span>
              <span style="font-weight:600;">纯妙记场景</span>
            </div>
            <div style="font-size:11px;color:#6b7a95;">无群消息仅会议纪要，验证会议结论融入而非单独列块</div>
          </td>
          <td style="padding:8px 10px;text-align:center;color:#8b98b0;">429</td>
          <td style="padding:8px 10px;text-align:center;color:#FF6B6B;">超时</td>
          <td style="padding:8px 14px;color:#FF9500;">系统提示词 15K 字 + 120s 上限，已调整至 180s 待复测</td>
        </tr>
      </tbody>
    </table>
  </div>

</div>'''

# ── Page 05: review_inline ────────────────────────────────────────────────────

RI_PAGE = '''\
<!-- 4. 批注测试 -->
<div class="section" id="skilleval-lr">
  <div class="section-label">测试验证</div>
  <div class="section-title">review_inline · 文档批注</div>

  <!-- 效果对比表 -->
  <div style="font-size:11px;font-weight:700;color:#6b7a95;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;">核心维度对比</div>
  <div style="background:#141820;border:1px solid #1e2530;border-radius:12px;overflow:hidden;margin-bottom:14px;">
    <table style="width:100%;border-collapse:collapse;font-size:13px;">
      <thead>
        <tr style="background:#0d1018;">
          <th style="padding:8px 16px;text-align:left;color:#6b7a95;font-weight:700;font-size:11px;letter-spacing:1px;text-transform:uppercase;width:18%;">核心差异</th>
          <th style="padding:8px 16px;text-align:left;color:#8b98b0;font-weight:700;font-size:11px;width:41%;">通用模型</th>
          <th style="padding:8px 16px;text-align:left;color:#34C759;font-weight:700;font-size:11px;width:41%;">加入 Skill 后</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:10px 16px;color:#e2e8f0;font-weight:700;vertical-align:top;">输出格式结构化</td>
          <td style="padding:10px 16px;color:#6b7a95;vertical-align:top;line-height:1.55;">自由输出段落式意见，有时附表格，格式不固定，无法直接对接写入接口（0 / 6）</td>
          <td style="padding:10px 16px;color:#6b7a95;vertical-align:top;line-height:1.55;">全部输出标准 JSON，可直接写入飞书（6 / 6）</td>
        </tr>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:10px 16px;color:#e2e8f0;font-weight:700;vertical-align:top;">评论口吻一致性</td>
          <td style="padding:10px 16px;color:#6b7a95;vertical-align:top;line-height:1.55;">「建议补充…」「需要注意…」「否则…」等解释型措辞，像顾问不像老板（平均 1.7 个禁忌词）</td>
          <td style="padding:10px 16px;color:#6b7a95;vertical-align:top;line-height:1.55;">追问式口吻（「谁来跟？」「时间计划是？」「没看懂～」），评论均长稳定（平均 0.2 个禁忌词）</td>
        </tr>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:10px 16px;color:#e2e8f0;font-weight:700;vertical-align:top;">批注数量克制</td>
          <td style="padding:10px 16px;color:#6b7a95;vertical-align:top;line-height:1.55;">倾向穷举所有问题，输出 6–10 条，含大量低价值细节批注，老板容易产生抵触（数量不定）</td>
          <td style="padding:10px 16px;color:#6b7a95;vertical-align:top;line-height:1.55;">6 个 case 全部输出恰好 5 条，优先选影响决策和推进的问题，低价值细节不过批（精确 5 条）</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- 分隔 -->
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
    <div style="flex:1;height:1px;background:#1e2530;"></div>
    <span style="font-size:11px;font-weight:700;color:#6b7a95;letter-spacing:1.5px;text-transform:uppercase;white-space:nowrap;">Eval 测试结果（2026-06-17）</span>
    <div style="flex:1;height:1px;background:#1e2530;"></div>
  </div>

  <!-- RI eval 表 -->
  <div style="background:#141820;border:1px solid #1e2530;border-radius:12px;overflow:hidden;margin-bottom:12px;">
    <table style="width:100%;border-collapse:collapse;font-size:13px;">
      <thead>
        <tr style="background:#0d1018;">
          <th style="padding:8px 14px;text-align:left;color:#6b7a95;font-weight:700;font-size:11px;letter-spacing:1px;text-transform:uppercase;width:28%;">场景</th>
          <th style="padding:8px 14px;text-align:left;color:#6b7a95;font-weight:700;font-size:11px;letter-spacing:1px;text-transform:uppercase;">关键观察</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:8px 14px;color:#e2e8f0;">
            <div style="display:flex;align-items:baseline;gap:6px;margin-bottom:2px;">
              <span style="font-size:11px;color:#4F8EF7;font-weight:700;white-space:nowrap;">RI-01</span>
              <span style="font-weight:600;">计划文档</span>
            </div>
            <div style="font-size:11px;color:#6b7a95;">时间节点过紧，全程无负责人，风险写「暂无」</div>
          </td>
          <td style="padding:8px 14px;color:#8b98b0;">通用模型输出 Markdown 分析；加入后直接追问缺失的人和日期</td>
        </tr>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:8px 14px;color:#e2e8f0;">
            <div style="display:flex;align-items:baseline;gap:6px;margin-bottom:2px;">
              <span style="font-size:11px;color:#34C759;font-weight:700;white-space:nowrap;">RI-02</span>
              <span style="font-weight:600;">方案文档</span>
            </div>
            <div style="font-size:11px;color:#6b7a95;">目标停留在「提升体验」，无 ROI 数字，无竞品参照</div>
          </td>
          <td style="padding:8px 14px;color:#8b98b0;">通用模型出现「建议补充」；加入后「GMV 增长多少？投 3 人 3 个月要给数字」</td>
        </tr>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:8px 14px;color:#e2e8f0;">
            <div style="display:flex;align-items:baseline;gap:6px;margin-bottom:2px;">
              <span style="font-size:11px;color:#FF9500;font-weight:700;white-space:nowrap;">RI-03</span>
              <span style="font-weight:600;">周报</span>
            </div>
            <div style="font-size:11px;color:#6b7a95;">下周计划全是「继续推进」「跟进」，无节点无验收</div>
          </td>
          <td style="padding:8px 14px;color:#8b98b0;">通用模型出现 2 个禁忌词；加入后聚焦 4 条无节点的下周计划</td>
        </tr>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:8px 14px;color:#e2e8f0;">
            <div style="display:flex;align-items:baseline;gap:6px;margin-bottom:2px;">
              <span style="font-size:11px;color:#FF6B6B;font-weight:700;white-space:nowrap;">RI-04</span>
              <span style="font-weight:600;">复盘文档</span>
            </div>
            <div style="font-size:11px;color:#6b7a95;">根因写「系统压力过大」，改进措施无人无期</div>
          </td>
          <td style="padding:8px 14px;color:#8b98b0;">加入后批注最短（均 10 字）「压力为什么大？这不是根因～」</td>
        </tr>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:8px 14px;color:#e2e8f0;">
            <div style="display:flex;align-items:baseline;gap:6px;margin-bottom:2px;">
              <span style="font-size:11px;color:#FF6B6B;font-weight:700;white-space:nowrap;">RI-05</span>
              <span style="font-weight:600;">需求说明</span>
            </div>
            <div style="font-size:11px;color:#6b7a95;">功能需求 4 条，无分类准确率要求，无验收标准</div>
          </td>
          <td style="padding:8px 14px;color:#8b98b0;">通用模型出现 3 个禁忌词；加入后「20 人天怎么算出来的～给个出处」</td>
        </tr>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:8px 14px;color:#e2e8f0;">
            <div style="display:flex;align-items:baseline;gap:6px;margin-bottom:2px;">
              <span style="font-size:11px;color:#8b5cf6;font-weight:700;white-space:nowrap;">RI-06</span>
              <span style="font-weight:600;">会议纪要</span>
            </div>
            <div style="font-size:11px;color:#6b7a95;">4 条行动项全无责任人和截止日期</div>
          </td>
          <td style="padding:8px 14px;color:#8b98b0;">通用模型建议表格输出；加入后精确批注 4 条无人认领的行动项</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- 测试数据说明 -->
  <div style="background:rgba(255,149,0,0.05);border:1px solid rgba(255,149,0,0.2);border-radius:10px;padding:12px 20px;">
    <div style="font-size:12px;font-weight:700;color:#FF9500;margin-bottom:8px;">⚠ 测试数据说明 — 两个 Skill 均使用手写模拟数据，原因各异</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:8px;">
      <div style="font-size:13px;color:#8b98b0;line-height:1.6;">
        <strong style="color:#e2e8f0;">日报</strong>：真实数据量过大（151 个群），单次运行 token 成本高，暂不适合用于自动化测试
      </div>
      <div style="font-size:13px;color:#8b98b0;line-height:1.6;">
        <strong style="color:#e2e8f0;">批注</strong>：历史批注散落在群聊对话或发生在线下，无法结构化收集作为基准数据
      </div>
    </div>
    <div style="display:flex;gap:24px;font-size:12px;">
      <span><span style="color:#34C759;font-weight:700;">✓ 已验证</span><span style="color:#6b7a95;margin-left:6px;">输出格式规范性 · 口吻一致性 · 批注数量克制</span></span>
      <span><span style="color:#4a5568;font-weight:700;">○ 待验证</span><span style="color:#6b7a95;margin-left:6px;">对真实生产场景的泛化能力（待积累真实样本后再评估）</span></span>
    </div>
  </div>

</div>'''

OLD_NAV = '''\
    <button class="nav-item active" data-idx="0"><span class="nav-num">01</span>概览</button>
    <button class="nav-item" data-idx="1"><span class="nav-num">02</span>系统架构</button>
    <button class="nav-item" data-idx="2"><span class="nav-num">03</span>Skill 能力</button>
    <button class="nav-item" data-idx="3"><span class="nav-num">04</span>维度对比</button>
    <button class="nav-item" data-idx="4"><span class="nav-num">05</span>维度双列</button>
    <button class="nav-item" data-idx="5"><span class="nav-num">06</span>测试结果</button>
    <button class="nav-item" data-idx="6"><span class="nav-num">07</span>服务流程</button>
    <button class="nav-item" data-idx="7"><span class="nav-num">08</span>产品角色</button>
    <button class="nav-item" data-idx="8"><span class="nav-num">09</span>技术选型</button>
    <button class="nav-item" data-idx="9"><span class="nav-num">10</span>框架对比</button>
    <button class="nav-item" data-idx="10"><span class="nav-num">11</span>框架分析</button>
    <button class="nav-item" data-idx="11"><span class="nav-num">12</span>方案评估</button>
    <button class="nav-item" data-idx="12"><span class="nav-num">13</span>进展计划</button>'''

NEW_NAV = '''\
    <button class="nav-item active" data-idx="0"><span class="nav-num">01</span>概览</button>
    <button class="nav-item" data-idx="1"><span class="nav-num">02</span>系统架构</button>
    <button class="nav-item" data-idx="2"><span class="nav-num">03</span>Skill 能力</button>
    <button class="nav-item" data-idx="3"><span class="nav-num">04</span>日报测试</button>
    <button class="nav-item" data-idx="4"><span class="nav-num">05</span>批注测试</button>
    <button class="nav-item" data-idx="5"><span class="nav-num">06</span>服务流程</button>
    <button class="nav-item" data-idx="6"><span class="nav-num">07</span>产品角色</button>
    <button class="nav-item" data-idx="7"><span class="nav-num">08</span>技术选型</button>
    <button class="nav-item" data-idx="8"><span class="nav-num">09</span>框架对比</button>
    <button class="nav-item" data-idx="9"><span class="nav-num">10</span>框架分析</button>
    <button class="nav-item" data-idx="10"><span class="nav-num">11</span>方案评估</button>
    <button class="nav-item" data-idx="11"><span class="nav-num">12</span>进展计划</button>'''


def find_section(html, id_):
    marker = f'<div class="section" id="{id_}"'
    start = html.index(marker)
    depth = 0; i = start
    while i < len(html):
        if html[i:i+4] == '<div':  depth += 1; i += 4
        elif html[i:i+6] == '</div>': depth -= 1; i += 6
        else: i += 1
        if depth == 0: return start, i
    raise ValueError(id_)


def process(src):
    shutil.copy(src, src.replace('.html', '-pre-scheme-b.html'))
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()

    # ── 1. Delete #skilleval-ri (测试结果 page, now merged into skill pages) ──
    ri_start, ri_end = find_section(html, 'skilleval-ri')
    # Include preceding comment
    for comment in ['<!-- 4. 测试结果 -->\n', '<!-- 4. Eval 结果 -->\n']:
        if comment in html and html.index(comment) < ri_start:
            ri_start = html.index(comment); break
    # Consume trailing newline
    while ri_end < len(html) and html[ri_end] == '\n':
        ri_end += 1
    html = html[:ri_start] + html[ri_end:]

    # ── 2. Replace #skilleval-lr with RI page ──────────────────────────────────
    lr_start, lr_end = find_section(html, 'skilleval-lr')
    for comment in ['<!-- 3b. 维度对比·双列 -->\n']:
        if comment in html and html.index(comment) < lr_start:
            lr_start = html.index(comment); break
    html = html[:lr_start] + RI_PAGE + '\n' + html[lr_end:]

    # ── 3. Replace #skilleval-dr with DR page ─────────────────────────────────
    dr_start, dr_end = find_section(html, 'skilleval-dr')
    for comment in ['<!-- 3. 维度对比 -->\n', '<!-- 3. 日报测试 -->\n']:
        if comment in html and html.index(comment) < dr_start:
            dr_start = html.index(comment); break
    html = html[:dr_start] + DR_PAGE + '\n' + html[dr_end:]

    # ── 4. Update nav ──────────────────────────────────────────────────────────
    assert OLD_NAV in html, 'Old nav not found'
    html = html.replace(OLD_NAV, NEW_NAV)

    with open(src, 'w', encoding='utf-8') as f:
        f.write(html)

    sections = [m.group(1) for m in re.finditer(r'class="section" id="([^"]+)"', html)]
    nav_count = html.count('data-idx=')
    print(f'{src.split("/")[-1]}: {len(html.splitlines())} lines, nav={nav_count}, sections={sections}')
    assert 'id="skilleval-dr"' in html
    assert 'id="skilleval-lr"' in html
    assert 'id="skilleval-ri"' not in html


process('/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/index.html')
process('/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/architecture-report.html')
