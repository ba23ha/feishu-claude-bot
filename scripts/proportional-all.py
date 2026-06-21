#!/usr/bin/env python3
"""
Apply proportional layouts to all presentation sections.
Each main content area gets flex:1 so it fills the available 100vh height.
"""

DOCS = [
    '/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/index.html',
    '/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/architecture-report.html',
]


def find_section(html, id_):
    marker = f'<div class="section" id="{id_}"'
    start = html.index(marker)
    depth = 0; i = start
    while i < len(html):
        if html[i:i+4] == '<div': depth += 1; i += 4
        elif html[i:i+6] == '</div>': depth -= 1; i += 6
        else: i += 1
        if depth == 0: return start, i
    raise ValueError(id_)


# ── #skills ──────────────────────────────────────────────────────────────────
NEW_SKILLS = '''\
<div class="section" id="skills">
  <div class="section-label">第二阶段</div>
  <div class="section-title">Skill 能力说明</div>
  <p style="color:#8b98b0;font-size:14px;margin-bottom:14px;flex-shrink:0;">
    Skill 是在 Soul 人格基础上叠加的场景化提示词，解决「通用模型不知道老板要什么格式、什么信息密度、什么判断标准」的问题。
    目前已激活 2 个 Skill。
  </p>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;flex:1;min-height:0;">

    <!-- daily_report -->
    <div class="conclusion-card" style="border-color:#2a3448;display:flex;flex-direction:column;">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;flex-shrink:0;">
        <div style="width:40px;height:40px;background:rgba(79,142,247,0.1);border:1px solid rgba(79,142,247,0.25);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;">📋</div>
        <div>
          <div style="font-size:15px;font-weight:700;color:#fff;">日报 daily_report</div>
          <div style="font-size:12px;color:#4F8EF7;margin-top:2px;">每日 18:30 自动触发</div>
        </div>
      </div>
      <div style="display:flex;flex-direction:column;flex:1;justify-content:space-between;">
        <div style="background:#0d1018;border-radius:8px;padding:12px 14px;">
          <div style="font-size:11px;font-weight:700;color:#4a5568;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;">数据来源</div>
          <div style="font-size:13px;color:#8b98b0;line-height:1.7;">
            · 151 个群聊（user token 逐群拉取当日消息）<br>
            · 飞书妙记（user token 按时间窗自动扫描）
          </div>
        </div>
        <div style="background:#0d1018;border-radius:8px;padding:12px 14px;">
          <div style="font-size:11px;font-weight:700;color:#4a5568;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;">群分级策略</div>
          <div style="font-size:13px;color:#8b98b0;line-height:1.7;">
            · 一级（7个）：核心团队，低门槛纳入<br>
            · 二级（60+）：业务群，仅实质内容<br>
            · 三级：默认忽略，重大异常除外<br>
            · 新群：按名称模式自动推断级别
          </div>
        </div>
        <div style="background:#0d1018;border-radius:8px;padding:12px 14px;">
          <div style="font-size:11px;font-weight:700;color:#4a5568;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;">AI 判断逻辑</div>
          <div style="font-size:13px;color:#8b98b0;line-height:1.7;">
            不是汇总，是判断。核心问题：今天不看，明天会不会出问题？
          </div>
        </div>
        <div style="background:#0d1018;border-radius:8px;padding:12px 14px;">
          <div style="font-size:11px;font-weight:700;color:#4a5568;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;">输出结构</div>
          <div style="font-size:13px;color:#8b98b0;line-height:1.7;">
            昨日动态（🔴🟡🟢 三级）<br>
            → 需要特别注意（决策缺失/时间风险/无人接手）<br>
            → 今日行动建议（今天必做 / 今天内跟进）
          </div>
        </div>
      </div>
    </div>

    <!-- review_inline -->
    <div class="conclusion-card" style="border-color:#2a3448;display:flex;flex-direction:column;">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;flex-shrink:0;">
        <div style="width:40px;height:40px;background:rgba(52,199,89,0.1);border:1px solid rgba(52,199,89,0.25);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;">📝</div>
        <div>
          <div style="font-size:15px;font-weight:700;color:#fff;">文档预审 review_inline</div>
          <div style="font-size:12px;color:#34C759;margin-top:2px;">老板主动触发 · 写入前需确认</div>
        </div>
      </div>
      <div style="display:flex;flex-direction:column;flex:1;justify-content:space-between;">
        <div style="background:#0d1018;border-radius:8px;padding:12px 14px;">
          <div style="font-size:11px;font-weight:700;color:#4a5568;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;">触发方式</div>
          <div style="font-size:13px;color:#8b98b0;line-height:1.7;">
            · 飞书文档链接 / 文档卡片转发<br>
            · 说"帮我批注这个文档"<br>
            · 仅老板或授权用户可触发
          </div>
        </div>
        <div style="background:#0d1018;border-radius:8px;padding:12px 14px;">
          <div style="font-size:11px;font-weight:700;color:#4a5568;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;">13 项核心能力</div>
          <div style="font-size:13px;color:#8b98b0;line-height:1.8;">
            文档接入 · 类型判断（8种）· 老板上下文加载<br>
            业务问题识别（14类）· 划线文本选择<br>
            批注草稿生成 · 优先级排序（≤5条）<br>
            预览确认 · 飞书写入（inline→整篇→消息）<br>
            权限控制 · 安全边界 · 审计记录 · 反馈校准
          </div>
        </div>
        <div style="background:#0d1018;border-radius:8px;padding:12px 14px;">
          <div style="font-size:11px;font-weight:700;color:#4a5568;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;">批注流程</div>
          <div style="font-size:13px;color:#8b98b0;line-height:1.7;">
            读文档 → 判类型 → 识别问题 → 生成 JSON 预览<br>
            → 老板确认 → 写入飞书评论区
          </div>
        </div>
        <div style="background:#0d1018;border-radius:8px;padding:12px 14px;">
          <div style="font-size:11px;font-weight:700;color:#4a5568;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;">评论风格约束</div>
          <div style="font-size:13px;color:#8b98b0;line-height:1.7;">
            1句话内 · 追问式 · 禁止"建议/否则"<br>
            高优先 → 影响决策 / 推进阻塞 / 风险敞口
          </div>
        </div>
      </div>
    </div>
  </div>
</div>'''


# ── #skilleval-dr ─────────────────────────────────────────────────────────────
NEW_SKILLEVAL_DR = '''\
<div class="section" id="skilleval-dr">
  <div class="section-label">测试验证</div>
  <div class="section-title">daily_report · 日报生成</div>

  <div style="flex:1;min-height:0;display:grid;grid-template-rows:auto 1fr;gap:12px;">

    <!-- 方法条 -->
    <div style="display:flex;align-items:center;gap:10px;background:#141820;border:1px solid #1e2530;border-radius:10px;padding:10px 20px;flex-wrap:wrap;">
      <span style="font-size:12px;font-weight:700;color:#6b7a95;letter-spacing:1px;text-transform:uppercase;white-space:nowrap;margin-right:8px;">测试方法</span>
      <div class="flow-node" style="padding:5px 14px;font-size:13px;">同一组模拟输入</div>
      <span style="color:#2d3748;font-size:14px;">→</span>
      <div class="flow-node highlight" style="padding:5px 14px;font-size:13px;">通用模型（无 Skill）</div>
      <span style="color:#2d3748;font-size:14px;">vs</span>
      <div class="flow-node green" style="padding:5px 14px;font-size:13px;">Soul + Skill</div>
      <span style="color:#2d3748;font-size:14px;">→</span>
      <div class="flow-node" style="padding:5px 14px;font-size:13px;">对比格式 / 口吻 / 关键信息 / 禁忌词</div>
    </div>

    <!-- 两列：对比表 | 测试结果 -->
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;min-height:0;">

      <!-- 左：核心维度对比 -->
      <div style="display:flex;flex-direction:column;min-height:0;">
        <div style="font-size:11px;font-weight:700;color:#6b7a95;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;flex-shrink:0;">核心维度对比</div>
        <div style="background:#141820;border:1px solid #1e2530;border-radius:12px;overflow:hidden;flex:1;min-height:0;">
          <table style="width:100%;border-collapse:collapse;font-size:13px;">
            <thead>
              <tr style="background:#0d1018;">
                <th style="padding:8px 14px;text-align:left;color:#6b7a95;font-weight:700;font-size:11px;letter-spacing:1px;text-transform:uppercase;width:22%;">核心差异</th>
                <th style="padding:8px 14px;text-align:left;color:#8b98b0;font-weight:700;font-size:11px;width:39%;">通用模型</th>
                <th style="padding:8px 14px;text-align:left;color:#34C759;font-weight:700;font-size:11px;width:39%;">加入 Skill 后</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-top:1px solid #1a2030;">
                <td style="padding:10px 14px;color:#e2e8f0;font-weight:700;vertical-align:top;">格式一致性</td>
                <td style="padding:10px 14px;color:#6b7a95;vertical-align:top;line-height:1.55;">每次结构不同，有时按群分组，有时按时间排列，无固定格式</td>
                <td style="padding:10px 14px;color:#6b7a95;vertical-align:top;line-height:1.55;">固定三段式（昨日动态 → 需特别注意 → 今日行动），老板形成阅读预期</td>
              </tr>
              <tr style="border-top:1px solid #1a2030;">
                <td style="padding:10px 14px;color:#e2e8f0;font-weight:700;vertical-align:top;">噪音过滤</td>
                <td style="padding:10px 14px;color:#6b7a95;vertical-align:top;line-height:1.55;">倾向"全面"，把"收到""了解""早上好"等也纳入，字数普遍 800+</td>
                <td style="padding:10px 14px;color:#6b7a95;vertical-align:top;line-height:1.55;">以「今天不看明天有没有麻烦」为过滤标准，高噪音场景仅输出 2 条有效信息</td>
              </tr>
              <tr style="border-top:1px solid #1a2030;">
                <td style="padding:10px 14px;color:#e2e8f0;font-weight:700;vertical-align:top;">行动可执行度</td>
                <td style="padding:10px 14px;color:#6b7a95;vertical-align:top;line-height:1.55;">建议停留在"持续关注""跟进推进"等泛化动词，无法直接执行</td>
                <td style="padding:10px 14px;color:#6b7a95;vertical-align:top;line-height:1.55;">要求「动词 + 对象 + 目标 + 今天的原因」，如"催 Yuki 今天核对预算表漏项，6/17 截止"</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 右：Eval 测试结果 -->
      <div style="display:flex;flex-direction:column;min-height:0;">
        <div style="font-size:11px;font-weight:700;color:#6b7a95;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;flex-shrink:0;">Eval 测试结果（2026-06-16）</div>
        <div style="background:#141820;border:1px solid #1e2530;border-radius:12px;overflow:hidden;flex:1;min-height:0;">
          <table style="width:100%;border-collapse:collapse;font-size:13px;">
            <thead>
              <tr style="background:#0d1018;">
                <th style="padding:8px 14px;text-align:left;color:#6b7a95;font-weight:700;font-size:11px;letter-spacing:1px;text-transform:uppercase;width:36%;">场景</th>
                <th style="padding:8px 10px;text-align:center;color:#8b98b0;font-weight:700;font-size:11px;width:9%;">通用</th>
                <th style="padding:8px 10px;text-align:center;color:#34C759;font-weight:700;font-size:11px;width:9%;">加入后</th>
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
      </div>

    </div>
  </div>
</div>'''


# ── #skilleval-lr ─────────────────────────────────────────────────────────────
NEW_SKILLEVAL_LR = '''\
<div class="section" id="skilleval-lr">
  <div class="section-label">测试验证</div>
  <div class="section-title">review_inline · 文档批注</div>

  <div style="flex:1;min-height:0;display:grid;grid-template-columns:1fr 1fr;gap:14px;">

    <!-- 左：核心维度对比 -->
    <div style="display:flex;flex-direction:column;min-height:0;">
      <div style="font-size:11px;font-weight:700;color:#6b7a95;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;flex-shrink:0;">核心维度对比</div>
      <div style="background:#141820;border:1px solid #1e2530;border-radius:12px;overflow:hidden;flex:1;min-height:0;">
        <table style="width:100%;border-collapse:collapse;font-size:13px;">
          <thead>
            <tr style="background:#0d1018;">
              <th style="padding:8px 16px;text-align:left;color:#6b7a95;font-weight:700;font-size:11px;letter-spacing:1px;text-transform:uppercase;width:22%;">核心差异</th>
              <th style="padding:8px 16px;text-align:left;color:#8b98b0;font-weight:700;font-size:11px;width:39%;">通用模型</th>
              <th style="padding:8px 16px;text-align:left;color:#34C759;font-weight:700;font-size:11px;width:39%;">加入 Skill 后</th>
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
    </div>

    <!-- 右：Eval 测试结果 + 测试说明 -->
    <div style="display:flex;flex-direction:column;min-height:0;">
      <div style="font-size:11px;font-weight:700;color:#6b7a95;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;flex-shrink:0;">Eval 测试结果（2026-06-17）</div>
      <div style="background:#141820;border:1px solid #1e2530;border-radius:12px;overflow:hidden;flex:1;min-height:0;">
        <table style="width:100%;border-collapse:collapse;font-size:13px;">
          <thead>
            <tr style="background:#0d1018;">
              <th style="padding:8px 14px;text-align:left;color:#6b7a95;font-weight:700;font-size:11px;letter-spacing:1px;text-transform:uppercase;width:34%;">场景</th>
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
      <div style="background:rgba(255,149,0,0.05);border:1px solid rgba(255,149,0,0.2);border-radius:10px;padding:10px 14px;margin-top:10px;flex-shrink:0;">
        <div style="font-size:11px;font-weight:700;color:#FF9500;margin-bottom:6px;">⚠ 测试数据说明 — 两个 Skill 均使用手写模拟数据</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:6px;">
          <div style="font-size:11px;color:#8b98b0;line-height:1.5;"><strong style="color:#e2e8f0;">日报</strong>：真实数据量过大（151 个群），token 成本高，暂不适合自动化测试</div>
          <div style="font-size:11px;color:#8b98b0;line-height:1.5;"><strong style="color:#e2e8f0;">批注</strong>：历史批注散落群聊或发生线下，无法结构化收集作为基准数据</div>
        </div>
        <div style="display:flex;gap:20px;font-size:11px;">
          <span><span style="color:#34C759;font-weight:700;">✓ 已验证</span><span style="color:#6b7a95;margin-left:6px;">格式规范性 · 口吻一致性 · 批注数量克制</span></span>
          <span><span style="color:#4a5568;font-weight:700;">○ 待验证</span><span style="color:#6b7a95;margin-left:6px;">对真实生产场景的泛化能力</span></span>
        </div>
      </div>
    </div>

  </div>
</div>'''


# ── #perm ─────────────────────────────────────────────────────────────────────
NEW_PERM = '''\
<div class="section" id="perm">
  <div class="section-label">产品决策</div>
  <div class="section-title">两项核心设计判断</div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;flex:1;min-height:0;">

    <!-- 决策A: Bot定位 -->
    <div class="conclusion-card" style="padding:20px 22px;display:flex;flex-direction:column;">
      <div class="conclusion-tag">架构决策</div>
      <div class="conclusion-icon" style="font-size:24px;margin-bottom:10px;">🤖</div>
      <div class="conclusion-title" style="font-size:16px;">无需区分多个 Bot，定位统一为老板代理人</div>
      <div class="conclusion-body" style="flex:1;">
        老板和员工使用的是<strong>同一个 Bot</strong>，回复口吻始终模拟老板本人说话——员工发文档，批注显示为老板写的；员工问问题，回复是老板风格的答复。这与"数字分身"定位完全一致。<br><br>
        拆成多个 Bot（老板专用 / 员工专用）的唯一好处是功能隔离，但当前员工侧功能本来就少，隔离价值低，两套 App ID + 两个 OAuth + 两个 WebSocket 连接的运维成本远大于收益。<br><br>
        <strong>功能层面的权限隔离已在代码层完成</strong>，无需靠拆 Bot 实现。
      </div>
    </div>

    <!-- 决策B: 配置管理暂缓 -->
    <div class="conclusion-card" style="padding:20px 22px;display:flex;flex-direction:column;">
      <div class="conclusion-tag orange">风险提示</div>
      <div class="conclusion-icon" style="font-size:24px;margin-bottom:10px;">⚠️</div>
      <div class="conclusion-title" style="font-size:16px;">管理员 / 员工自主配置 Agent 的业务实现难点</div>
      <div class="conclusion-body">
        由非技术人员通过自然语言管理 Agent 配置，在业务层面面临以下核心风险：
      </div>
      <div class="risk-list" style="flex:1;">
        <div class="risk-item"><strong>意图歧义</strong>——"把 review 风格改简洁一点"，AI 无法确定改哪里、改多少，容易误改关键规则</div>
        <div class="risk-item"><strong>富文本修改风险</strong>——Soul / Skill 是 Markdown，通过聊天编辑等于让 AI 代写代码，一次误操作影响所有用户</div>
        <div class="risk-item"><strong>无法直观 Review</strong>——聊天界面看不到改动前后对比，确认成本高</div>
        <div class="risk-item"><strong>配置生效需重启</strong>——改完还需触发重启，对非技术人员不直观</div>
      </div>
      <div class="conclusion-body" style="margin-top:12px;">
        <strong>当前结论：暂缓，由产品团队通过 VSCode 管理配置后台。</strong>等第二阶段架构稳定、配置项收敛后再评估。
      </div>
    </div>

  </div>
</div>'''


# ── #tech-compare ─────────────────────────────────────────────────────────────
NEW_TECH_COMPARE = '''\
<div class="section" id="tech-compare">
  <div class="section-label">技术选型</div>
  <div class="section-title">技术选型 & 方案优势</div>
  <div class="conclusion-card full" style="border-radius:14px;flex:1;min-height:0;overflow:hidden;">
    <div class="conclusion-tag red">选型分析</div>
    <div class="conclusion-icon">⚖️</div>
    <div class="conclusion-title">用 Claude Code 作为底层 vs 成熟 AI 框架（如 LangChain / Hermes）的对比</div>
    <div class="vs-grid">
      <div>
        <div class="vs-col-head ours">当前方案：Claude Code CLI</div>
        <div class="vs-col-body">
          <div class="vs-item"><strong>Skill 形式：</strong>Markdown 文件注入 prompt，无正式 registry</div>
          <div class="vs-item"><strong>工具调用：</strong>靠提示词让模型输出 JSON，手写解析 + 重试</div>
          <div class="vs-item"><strong>记忆管理：</strong>每次请求手动注入 Soul + Memory 文件</div>
          <div class="vs-item"><strong>模型绑定：</strong>强依赖 Claude，切换模型需重写调用层</div>
          <div class="vs-item"><strong>部署依赖：</strong>必须在装有 Claude Code 的机器上运行</div>
          <div class="vs-item"><strong>零 AI 成本：</strong>✅ 调用本地 CLI，不计费</div>
          <div class="vs-item"><strong>迭代速度：</strong>✅ 改 Markdown 文件即可调整行为</div>
        </div>
      </div>
      <div>
        <div class="vs-col-head theirs">成熟框架：LangChain / Hermes 类</div>
        <div class="vs-col-body">
          <div class="vs-item"><strong>Skill 形式：</strong>标准 Tool / Function 定义，带 schema 校验</div>
          <div class="vs-item"><strong>工具调用：</strong>原生 Function Calling，结构化输出有保障</div>
          <div class="vs-item"><strong>记忆管理：</strong>内置向量数据库 / 会话管理，自动检索</div>
          <div class="vs-item"><strong>多模型支持：</strong>可同时使用多个模型，按任务选择</div>
          <div class="vs-item"><strong>部署灵活：</strong>独立服务，可容器化部署到任意云</div>
          <div class="vs-item"><strong>成本：</strong>⚠️ 按 Token 计费，高频使用成本高</div>
          <div class="vs-item"><strong>迭代速度：</strong>⚠️ 需要写代码修改 Tool 定义</div>
        </div>
      </div>
    </div>
    <div class="conclusion-body" style="margin-top:16px;padding-top:14px;border-top:1px solid #1e2530;">
      <strong>选型说明：</strong>Claude Code 的 Skill 体系是 Markdown 注入 prompt，不是标准的 Tool / Function Calling，<strong>没有 schema 校验、没有 registry、没有结构化输出保障</strong>，完全依赖 prompt 工程和手写重试逻辑。<br><br><strong>决策依据：</strong>零成本迭代优先，用最少依赖跑通业务闭环，验证可行后第二阶段再做框架升级。
    </div>
  </div>

  <div style="margin-top:12px;flex-shrink:0;">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
      <div style="flex:1;height:1px;background:#1e2530;"></div>
      <span style="font-size:11px;font-weight:700;color:#34C759;letter-spacing:1.5px;text-transform:uppercase;white-space:nowrap;">当前方案优势</span>
      <div style="flex:1;height:1px;background:#1e2530;"></div>
    </div>
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;">
      <div style="background:#141820;border:1px solid #1e2530;border-radius:10px;padding:10px 12px;">
        <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:4px;">零 AI 成本</div>
        <div style="font-size:12px;color:#6b7a95;line-height:1.45;">调用本机 CLI，不走 API 计费</div>
      </div>
      <div style="background:#141820;border:1px solid #1e2530;border-radius:10px;padding:10px 12px;">
        <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:4px;">数据不出内网</div>
        <div style="font-size:12px;color:#6b7a95;line-height:1.45;">全部本机处理，不上传第三方</div>
      </div>
      <div style="background:#141820;border:1px solid #1e2530;border-radius:10px;padding:10px 12px;">
        <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:4px;">部署简单</div>
        <div style="font-size:12px;color:#6b7a95;line-height:1.45;">一台 Mac 30 分钟完成部署</div>
      </div>
      <div style="background:#141820;border:1px solid #1e2530;border-radius:10px;padding:10px 12px;">
        <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:4px;">产品团队可迭代</div>
        <div style="font-size:12px;color:#6b7a95;line-height:1.45;">改 Markdown 即可调整 AI 行为</div>
      </div>
      <div style="background:#141820;border:1px solid #1e2530;border-radius:10px;padding:10px 12px;">
        <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:4px;">权限隔离清晰</div>
        <div style="font-size:12px;color:#6b7a95;line-height:1.45;">双层控制，非授权用户无感知</div>
      </div>
    </div>
  </div>
</div>'''


# ── #framework-compare ────────────────────────────────────────────────────────
NEW_FRAMEWORK_COMPARE = '''\
<div class="section" id="framework-compare">
  <div class="section-label">框架对比</div>
  <div class="section-title">与主流 Agent 框架对比</div>

  <div style="background:#141820;border:1px solid #1e2530;border-radius:12px;overflow:hidden;flex:1;min-height:0;">
    <table style="width:100%;border-collapse:collapse;font-size:12px;">
      <thead>
        <tr style="background:#0d1018;">
          <th style="padding:11px 16px;text-align:left;color:#6b7a95;font-weight:700;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;width:24%;">能力维度</th>
          <th style="padding:11px 14px;text-align:center;color:#a78bfa;font-weight:700;font-size:11px;width:19%;">当前方案</th>
          <th style="padding:11px 14px;text-align:center;color:#f97316;font-weight:700;font-size:11px;width:19%;">Hermes<div style="font-size:9px;color:#6b7a95;font-weight:400;margin-top:1px;">NousResearch</div></th>
          <th style="padding:11px 14px;text-align:center;color:#22d3ee;font-weight:700;font-size:11px;width:19%;">OpenClaw<div style="font-size:9px;color:#6b7a95;font-weight:400;margin-top:1px;">openclaw/openclaw</div></th>
          <th style="padding:11px 14px;text-align:center;color:#4ade80;font-weight:700;font-size:11px;width:19%;">pi-agent<div style="font-size:9px;color:#6b7a95;font-weight:400;margin-top:1px;">earendil-works/pi</div></th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:10px 16px;color:#e2e8f0;font-weight:600;font-size:12px;">人设 / 角色定制<div style="font-size:10px;color:#6b7a95;font-weight:400;margin-top:2px;">风格、决策偏好、忌讳</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">精细 5 维度 Soul</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">⭕</div><div style="font-size:10px;color:#FF9500;margin-top:2px;">依赖基座模型</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">SOUL.md 配置</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">⭕</div><div style="font-size:10px;color:#FF9500;margin-top:2px;">系统提示词</div></td>
        </tr>
        <tr style="border-top:1px solid #1a2030;background:rgba(255,255,255,0.01);">
          <td style="padding:10px 16px;color:#e2e8f0;font-weight:600;font-size:12px;">业务长期记忆<div style="font-size:10px;color:#6b7a95;font-weight:400;margin-top:2px;">项目 / 人员 / 术语持久化</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">⭕</div><div style="font-size:10px;color:#FF9500;margin-top:2px;">手工 .md 维护</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">自动持久化</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">内置记忆模块</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">JSONL 会话持久化</div></td>
        </tr>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:10px 16px;color:#e2e8f0;font-weight:600;font-size:12px;">细分场景技能<div style="font-size:10px;color:#6b7a95;font-weight:400;margin-top:2px;">特定任务类型的行为规范</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">手写 Skill .md</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">Skill 自动创建 + 进化</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">162+ 生产模板</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">Skills + 扩展系统</div></td>
        </tr>
        <tr style="border-top:1px solid #1a2030;background:rgba(255,255,255,0.01);">
          <td style="padding:10px 16px;color:#e2e8f0;font-weight:600;font-size:12px;">多步任务规划<div style="font-size:10px;color:#6b7a95;font-weight:400;margin-top:2px;">分解 → 执行 → 反思循环</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">❌</div><div style="font-size:10px;color:#FF6B6B;margin-top:2px;">无规划能力</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">Agent loop + 反思</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">Agent loop</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">Agent loop + 工具调用</div></td>
        </tr>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:10px 16px;color:#e2e8f0;font-weight:600;font-size:12px;">工具调用编排<div style="font-size:10px;color:#6b7a95;font-weight:400;margin-top:2px;">外部 API 动态调用与组合</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">⭕</div><div style="font-size:10px;color:#FF9500;margin-top:2px;">手动硬编码</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">动态工具调用</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">20+ 平台原生工具</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">内置文件 / Bash 工具</div></td>
        </tr>
        <tr style="border-top:1px solid #1a2030;background:rgba(255,255,255,0.01);">
          <td style="padding:10px 16px;color:#e2e8f0;font-weight:600;font-size:12px;">多智能体协作<div style="font-size:10px;color:#6b7a95;font-weight:400;margin-top:2px;">多 Agent 分工并行</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">❌</div><div style="font-size:10px;color:#FF6B6B;margin-top:2px;">单 Agent</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">⭕</div><div style="font-size:10px;color:#FF9500;margin-top:2px;">Workspace 共享</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">Managed Agents</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">⭕</div><div style="font-size:10px;color:#FF9500;margin-top:2px;">Subagent 扩展</div></td>
        </tr>
        <tr style="border-top:1px solid #1a2030;">
          <td style="padding:10px 16px;color:#e2e8f0;font-weight:600;font-size:12px;">Skill 自我进化<div style="font-size:10px;color:#6b7a95;font-weight:400;margin-top:2px;">从经验中自动优化技能</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">❌</div><div style="font-size:10px;color:#FF6B6B;margin-top:2px;">手工更新</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">Curator 7 日周期优化</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">❌</div><div style="font-size:10px;color:#FF6B6B;margin-top:2px;">手工维护</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">❌</div><div style="font-size:10px;color:#FF6B6B;margin-top:2px;">手工维护</div></td>
        </tr>
        <tr style="border-top:1px solid #1a2030;background:rgba(255,255,255,0.01);">
          <td style="padding:10px 16px;color:#e2e8f0;font-weight:600;font-size:12px;">业务平台集成<div style="font-size:10px;color:#6b7a95;font-weight:400;margin-top:2px;">飞书消息 / 文档 / 日历</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">飞书深度集成</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">18 个平台</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">✅</div><div style="font-size:10px;color:#34C759;margin-top:2px;">含飞书 20+ 平台</div></td>
          <td style="padding:10px 14px;text-align:center;"><div style="font-size:15px;">⭕</div><div style="font-size:10px;color:#FF9500;margin-top:2px;">Slack + 可扩展</div></td>
        </tr>
      </tbody>
    </table>
  </div>

  <div style="display:flex;gap:20px;margin-top:10px;justify-content:flex-end;flex-shrink:0;">
    <span style="font-size:11px;color:#6b7a95;">✅ 完整支持</span>
    <span style="font-size:11px;color:#6b7a95;">⭕ 部分支持 / 需配置</span>
    <span style="font-size:11px;color:#6b7a95;">❌ 不支持</span>
  </div>
</div>'''


# ── #framework-gap ────────────────────────────────────────────────────────────
NEW_FRAMEWORK_GAP = '''\
<div class="section" id="framework-gap">
  <div class="section-label">局限与差距</div>
  <div class="section-title">架构差距与运维局限</div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;flex:1;min-height:0;">
    <div style="background:rgba(52,199,89,0.04);border:1px solid rgba(52,199,89,0.2);border-radius:12px;padding:20px;display:flex;flex-direction:column;">
      <div style="font-size:12px;font-weight:700;color:#34C759;margin-bottom:12px;letter-spacing:0.5px;">当前方案的核心优势</div>
      <div style="font-size:12px;color:#8b98b0;line-height:1.9;flex:1;">
        <span style="color:#e2e8f0;font-weight:600;">人设精细度</span>：5 个维度的 Soul 文件是通用框架没有的专项投入，输出风格一致性显著优于 system prompt 单段描述<br>
        <span style="color:#e2e8f0;font-weight:600;">飞书深度集成</span>：消息接收、文档批注写入、日报推送全部原生对接，通用框架均需额外开发<br>
        <span style="color:#e2e8f0;font-weight:600;">无框架锁定</span>：纯 Node.js 实现，依赖链短，调试链路清晰，迁移模型零成本
      </div>
    </div>
    <div style="background:rgba(255,149,0,0.04);border:1px solid rgba(255,149,0,0.2);border-radius:12px;padding:20px;display:flex;flex-direction:column;">
      <div style="font-size:12px;font-weight:700;color:#FF9500;margin-bottom:12px;letter-spacing:0.5px;">与成熟框架的主要差距</div>
      <div style="font-size:12px;color:#8b98b0;line-height:1.9;flex:1;">
        <span style="color:#e2e8f0;font-weight:600;">无规划能力</span>：只能处理单步任务，复杂需求（如「整理本周所有项目进展并汇总」）无法分解执行<br>
        <span style="color:#e2e8f0;font-weight:600;">记忆靠手工</span>：glossary / people-map 需人工维护，LangGraph 等框架支持自动向量化写入<br>
        <span style="color:#e2e8f0;font-weight:600;">无多 Agent</span>：日报生成与批注审阅串行依赖同一 Agent，无法并行分工、互相校验
      </div>
    </div>
  </div>

  <div style="margin-top:12px;flex-shrink:0;">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
      <div style="flex:1;height:1px;background:#1e2530;"></div>
      <span style="font-size:11px;font-weight:700;color:#FF9500;letter-spacing:1.5px;text-transform:uppercase;white-space:nowrap;">运维局限</span>
      <div style="flex:1;height:1px;background:#1e2530;"></div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
      <div style="background:#141820;border:1px solid rgba(255,107,107,0.15);border-radius:10px;padding:10px 14px;">
        <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:3px;">依赖本地 Mac</div>
        <div style="font-size:12px;color:#6b7a95;line-height:1.45;margin-bottom:5px;">机器休眠、断电、系统更新会导致服务中断</div>
        <div style="font-size:11px;color:#4F8EF7;">→ 第二阶段：迁移至独立服务器</div>
      </div>
      <div style="background:#141820;border:1px solid rgba(255,107,107,0.15);border-radius:10px;padding:10px 14px;">
        <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:3px;">OAuth Token 需定期维护</div>
        <div style="font-size:12px;color:#6b7a95;line-height:1.45;margin-bottom:5px;">飞书授权 refresh token 有效期约 30 天</div>
        <div style="font-size:11px;color:#4F8EF7;">→ 可加自动检测 + 主动提醒</div>
      </div>
      <div style="background:#141820;border:1px solid rgba(255,107,107,0.15);border-radius:10px;padding:10px 14px;">
        <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:3px;">白名单扩展需重启</div>
        <div style="font-size:12px;color:#6b7a95;line-height:1.45;margin-bottom:5px;">新增员工需修改配置文件，约有 2–3 秒中断</div>
        <div style="font-size:11px;color:#4F8EF7;">→ 第二阶段：改为热更新</div>
      </div>
      <div style="background:#141820;border:1px solid rgba(255,107,107,0.15);border-radius:10px;padding:10px 14px;">
        <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:3px;">日报依赖网络稳定性</div>
        <div style="font-size:12px;color:#6b7a95;line-height:1.45;margin-bottom:5px;">18:30 定时任务若网络故障会静默失败</div>
        <div style="font-size:11px;color:#4F8EF7;">→ 第二阶段：加失败重试 + 告警</div>
      </div>
    </div>
  </div>
</div>'''


SECTION_MAP = {
    'skills':            NEW_SKILLS,
    'skilleval-dr':      NEW_SKILLEVAL_DR,
    'skilleval-lr':      NEW_SKILLEVAL_LR,
    'perm':              NEW_PERM,
    'tech-compare':      NEW_TECH_COMPARE,
    'framework-compare': NEW_FRAMEWORK_COMPARE,
    'framework-gap':     NEW_FRAMEWORK_GAP,
}


def process(src):
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()

    for id_, new_html in SECTION_MAP.items():
        s, e = find_section(html, id_)
        html = html[:s] + new_html + html[e:]

    # Simple targeted replacements for agent-arch and status
    html = html.replace(
        '<div class="flow-wrap">',
        '<div class="flow-wrap" style="flex:1;min-height:0;overflow:hidden;">'
    )
    html = html.replace(
        '<div class="progress-bar-wrap" style="max-width:400px;margin-bottom:32px;">',
        '<div class="progress-bar-wrap" style="max-width:400px;margin-bottom:12px;">'
    )
    html = html.replace(
        '<div class="status-grid" style="grid-template-columns:1fr 1fr;">',
        '<div class="status-grid" style="grid-template-columns:1fr 1fr;flex:1;min-height:0;">'
    )

    with open(src, 'w', encoding='utf-8') as f:
        f.write(html)

    lines = len(html.splitlines())
    print(f'{src.split("/")[-1]}: {lines} lines  ✓')


for doc in DOCS:
    process(doc)

print('\nAll sections updated.')
