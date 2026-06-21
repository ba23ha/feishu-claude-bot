#!/usr/bin/env python3
"""
Rebuild #skilleval-ri page:
- Title: "测试结果"
- Layout: DR table (left) | RI table (right), side by side
- Bottom: compact data-note banner (revised copy)
- Nav: "Eval 结果" → "测试结果"
"""
import shutil, re

NEW_SECTION = '''\
<!-- 4. 测试结果 -->
<div class="section" id="skilleval-ri">
  <div class="section-label">测试验证</div>
  <div class="section-title">测试结果</div>

  <!-- 两表并排 -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;flex:1;min-height:0;margin-bottom:10px;">

    <!-- 左列: daily_report -->
    <div style="display:flex;flex-direction:column;min-height:0;overflow:hidden;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-shrink:0;">
        <div style="width:20px;height:20px;background:rgba(79,142,247,0.1);border:1px solid rgba(79,142,247,0.25);border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:11px;flex-shrink:0;">📋</div>
        <span style="font-size:12px;font-weight:700;color:#4F8EF7;">daily_report</span>
        <div style="flex:1;height:1px;background:#1e2530;"></div>
        <span style="font-size:10px;color:#4a5568;white-space:nowrap;">2026-06-16</span>
      </div>
      <div style="background:#141820;border:1px solid #1e2530;border-radius:10px;overflow:hidden;flex:1;min-height:0;">
        <table style="width:100%;border-collapse:collapse;font-size:11px;">
          <thead>
            <tr style="background:#0d1018;">
              <th style="padding:6px 10px;text-align:left;color:#6b7a95;font-weight:700;font-size:10px;letter-spacing:1px;text-transform:uppercase;width:30%;">场景</th>
              <th style="padding:6px 8px;text-align:center;color:#8b98b0;font-weight:700;font-size:10px;width:10%;">通用</th>
              <th style="padding:6px 8px;text-align:center;color:#34C759;font-weight:700;font-size:10px;width:10%;">加入后</th>
              <th style="padding:6px 10px;text-align:left;color:#6b7a95;font-weight:700;font-size:10px;letter-spacing:1px;text-transform:uppercase;">关键观察</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-top:1px solid #1a2030;">
              <td style="padding:6px 10px;color:#e2e8f0;">
                <div style="display:flex;align-items:baseline;gap:5px;margin-bottom:1px;">
                  <span style="font-size:10px;color:#4F8EF7;font-weight:700;white-space:nowrap;">DR-01</span>
                  <span style="font-weight:600;font-size:11px;">混合场景</span>
                </div>
                <div style="font-size:10px;color:#6b7a95;">紧急 + 跟踪 + 正向进展并存</div>
              </td>
              <td style="padding:6px 8px;text-align:center;color:#8b98b0;">854</td>
              <td style="padding:6px 8px;text-align:center;color:#34C759;">517</td>
              <td style="padding:6px 10px;color:#8b98b0;font-size:11px;">精简 40%，行动建议点名具体人和截止</td>
            </tr>
            <tr style="border-top:1px solid #1a2030;">
              <td style="padding:6px 10px;color:#e2e8f0;">
                <div style="display:flex;align-items:baseline;gap:5px;margin-bottom:1px;">
                  <span style="font-size:10px;color:#34C759;font-weight:700;white-space:nowrap;">DR-02</span>
                  <span style="font-weight:600;font-size:11px;">无异常日</span>
                </div>
                <div style="font-size:10px;color:#6b7a95;">全是正向进展，验证省略逻辑</div>
              </td>
              <td style="padding:6px 8px;text-align:center;color:#8b98b0;">463</td>
              <td style="padding:6px 8px;text-align:center;color:#34C759;">282</td>
              <td style="padding:6px 10px;color:#8b98b0;font-size:11px;">正确省略"需注意"和"今天必做"区块</td>
            </tr>
            <tr style="border-top:1px solid #1a2030;">
              <td style="padding:6px 10px;color:#e2e8f0;">
                <div style="display:flex;align-items:baseline;gap:5px;margin-bottom:1px;">
                  <span style="font-size:10px;color:#FF9500;font-weight:700;white-space:nowrap;">DR-03</span>
                  <span style="font-weight:600;font-size:11px;">高噪音日</span>
                </div>
                <div style="font-size:10px;color:#6b7a95;">大量闲聊打卡，有效内容仅 2 条</div>
              </td>
              <td style="padding:6px 8px;text-align:center;color:#8b98b0;">331</td>
              <td style="padding:6px 8px;text-align:center;color:#8b98b0;">332</td>
              <td style="padding:6px 10px;color:#8b98b0;font-size:11px;">字数相近；加入后多识别出销售承诺未对齐的隐性风险</td>
            </tr>
            <tr style="border-top:1px solid #1a2030;">
              <td style="padding:6px 10px;color:#e2e8f0;">
                <div style="display:flex;align-items:baseline;gap:5px;margin-bottom:1px;">
                  <span style="font-size:10px;color:#FF6B6B;font-weight:700;white-space:nowrap;">DR-04</span>
                  <span style="font-weight:600;font-size:11px;">三级群异常</span>
                </div>
                <div style="font-size:10px;color:#6b7a95;">L3 群生产故障，验证重大异常突破</div>
              </td>
              <td style="padding:6px 8px;text-align:center;color:#8b98b0;">314</td>
              <td style="padding:6px 8px;text-align:center;color:#8b98b0;">305</td>
              <td style="padding:6px 10px;color:#8b98b0;font-size:11px;">加入后额外指出无复盘方案存在再发风险</td>
            </tr>
            <tr style="border-top:1px solid #1a2030;">
              <td style="padding:6px 10px;color:#e2e8f0;">
                <div style="display:flex;align-items:baseline;gap:5px;margin-bottom:1px;">
                  <span style="font-size:10px;color:#FF6B6B;font-weight:700;white-space:nowrap;">DR-05</span>
                  <span style="font-weight:600;font-size:11px;">双紧急并存</span>
                </div>
                <div style="font-size:10px;color:#6b7a95;">决策悬空 + 时间风险同时出现</div>
              </td>
              <td style="padding:6px 8px;text-align:center;color:#8b98b0;">651</td>
              <td style="padding:6px 8px;text-align:center;color:#34C759;">480</td>
              <td style="padding:6px 10px;color:#8b98b0;font-size:11px;">通用输出 Markdown 表格；加入后两条 🔴 分别对应行动</td>
            </tr>
            <tr style="border-top:1px solid #1a2030;">
              <td style="padding:6px 10px;color:#e2e8f0;">
                <div style="display:flex;align-items:baseline;gap:5px;margin-bottom:1px;">
                  <span style="font-size:10px;color:#8b5cf6;font-weight:700;white-space:nowrap;">DR-06</span>
                  <span style="font-weight:600;font-size:11px;">纯妙记场景</span>
                </div>
                <div style="font-size:10px;color:#6b7a95;">无群消息仅会议纪要</div>
              </td>
              <td style="padding:6px 8px;text-align:center;color:#8b98b0;">429</td>
              <td style="padding:6px 8px;text-align:center;color:#FF6B6B;">超时</td>
              <td style="padding:6px 10px;color:#FF9500;font-size:11px;">系统提示词 15K 字 + 120s 上限，已调整至 180s 待复测</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 右列: review_inline -->
    <div style="display:flex;flex-direction:column;min-height:0;overflow:hidden;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-shrink:0;">
        <div style="width:20px;height:20px;background:rgba(52,199,89,0.1);border:1px solid rgba(52,199,89,0.25);border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:11px;flex-shrink:0;">📝</div>
        <span style="font-size:12px;font-weight:700;color:#34C759;">review_inline</span>
        <div style="flex:1;height:1px;background:#1e2530;"></div>
        <span style="font-size:10px;color:#4a5568;white-space:nowrap;">2026-06-17</span>
      </div>
      <div style="background:#141820;border:1px solid #1e2530;border-radius:10px;overflow:hidden;flex:1;min-height:0;">
        <table style="width:100%;border-collapse:collapse;font-size:11px;">
          <thead>
            <tr style="background:#0d1018;">
              <th style="padding:6px 10px;text-align:left;color:#6b7a95;font-weight:700;font-size:10px;letter-spacing:1px;text-transform:uppercase;width:32%;">场景</th>
              <th style="padding:6px 10px;text-align:left;color:#6b7a95;font-weight:700;font-size:10px;letter-spacing:1px;text-transform:uppercase;">关键观察</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-top:1px solid #1a2030;">
              <td style="padding:6px 10px;color:#e2e8f0;">
                <div style="display:flex;align-items:baseline;gap:5px;margin-bottom:1px;">
                  <span style="font-size:10px;color:#4F8EF7;font-weight:700;white-space:nowrap;">RI-01</span>
                  <span style="font-weight:600;font-size:11px;">计划文档</span>
                </div>
                <div style="font-size:10px;color:#6b7a95;">时间紧，全程无负责人，风险写「暂无」</div>
              </td>
              <td style="padding:6px 10px;color:#8b98b0;font-size:11px;">通用输出 Markdown 分析；加入后直接追问缺失的人和日期</td>
            </tr>
            <tr style="border-top:1px solid #1a2030;">
              <td style="padding:6px 10px;color:#e2e8f0;">
                <div style="display:flex;align-items:baseline;gap:5px;margin-bottom:1px;">
                  <span style="font-size:10px;color:#34C759;font-weight:700;white-space:nowrap;">RI-02</span>
                  <span style="font-weight:600;font-size:11px;">方案文档</span>
                </div>
                <div style="font-size:10px;color:#6b7a95;">目标停留「提升体验」，无 ROI，无竞品</div>
              </td>
              <td style="padding:6px 10px;color:#8b98b0;font-size:11px;">通用出现「建议补充」；加入后「GMV 增长多少？投 3 人 3 个月要给数字」</td>
            </tr>
            <tr style="border-top:1px solid #1a2030;">
              <td style="padding:6px 10px;color:#e2e8f0;">
                <div style="display:flex;align-items:baseline;gap:5px;margin-bottom:1px;">
                  <span style="font-size:10px;color:#FF9500;font-weight:700;white-space:nowrap;">RI-03</span>
                  <span style="font-weight:600;font-size:11px;">周报</span>
                </div>
                <div style="font-size:10px;color:#6b7a95;">下周计划全是「继续推进」，无节点无验收</div>
              </td>
              <td style="padding:6px 10px;color:#8b98b0;font-size:11px;">通用出现 2 个禁忌词；加入后聚焦 4 条无节点的下周计划</td>
            </tr>
            <tr style="border-top:1px solid #1a2030;">
              <td style="padding:6px 10px;color:#e2e8f0;">
                <div style="display:flex;align-items:baseline;gap:5px;margin-bottom:1px;">
                  <span style="font-size:10px;color:#FF6B6B;font-weight:700;white-space:nowrap;">RI-04</span>
                  <span style="font-weight:600;font-size:11px;">复盘文档</span>
                </div>
                <div style="font-size:10px;color:#6b7a95;">根因写「系统压力过大」，无人无期</div>
              </td>
              <td style="padding:6px 10px;color:#8b98b0;font-size:11px;">加入后批注均 10 字「压力为什么大？这不是根因～」</td>
            </tr>
            <tr style="border-top:1px solid #1a2030;">
              <td style="padding:6px 10px;color:#e2e8f0;">
                <div style="display:flex;align-items:baseline;gap:5px;margin-bottom:1px;">
                  <span style="font-size:10px;color:#FF6B6B;font-weight:700;white-space:nowrap;">RI-05</span>
                  <span style="font-weight:600;font-size:11px;">需求说明</span>
                </div>
                <div style="font-size:10px;color:#6b7a95;">功能需求 4 条，无验收标准</div>
              </td>
              <td style="padding:6px 10px;color:#8b98b0;font-size:11px;">通用出现 3 个禁忌词；加入后「20 人天怎么算出来的～给个出处」</td>
            </tr>
            <tr style="border-top:1px solid #1a2030;">
              <td style="padding:6px 10px;color:#e2e8f0;">
                <div style="display:flex;align-items:baseline;gap:5px;margin-bottom:1px;">
                  <span style="font-size:10px;color:#8b5cf6;font-weight:700;white-space:nowrap;">RI-06</span>
                  <span style="font-weight:600;font-size:11px;">会议纪要</span>
                </div>
                <div style="font-size:10px;color:#6b7a95;">4 条行动项全无责任人和截止日期</div>
              </td>
              <td style="padding:6px 10px;color:#8b98b0;font-size:11px;">通用建议表格输出；加入后精确批注 4 条无人认领的行动项</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>

  <!-- 测试数据说明横幅 -->
  <div style="background:rgba(255,149,0,0.05);border:1px solid rgba(255,149,0,0.2);border-radius:10px;padding:12px 20px;flex-shrink:0;">
    <div style="font-size:11px;font-weight:700;color:#FF9500;margin-bottom:8px;">⚠ 测试数据说明 — 两个 Skill 均使用手写模拟数据，原因各异</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:8px;">
      <div style="font-size:12px;color:#8b98b0;line-height:1.6;">
        <strong style="color:#e2e8f0;">日报</strong>：真实数据量过大（151 个群），单次运行 token 成本高，暂不适合用于自动化测试
      </div>
      <div style="font-size:12px;color:#8b98b0;line-height:1.6;">
        <strong style="color:#e2e8f0;">批注</strong>：历史批注散落在群聊对话或发生在线下，无法结构化收集作为基准数据
      </div>
    </div>
    <div style="display:flex;gap:24px;font-size:11px;">
      <span><span style="color:#34C759;font-weight:700;">✓ 已验证</span><span style="color:#6b7a95;margin-left:6px;">输出格式规范性 · 口吻一致性 · 批注数量克制</span></span>
      <span><span style="color:#4a5568;font-weight:700;">○ 待验证</span><span style="color:#6b7a95;margin-left:6px;">对真实生产场景的泛化能力（待积累真实样本后再评估）</span></span>
    </div>
  </div>

</div>'''

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
    shutil.copy(src, src.replace('.html', '-pre-eval-rebuild.html'))
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace #skilleval-ri section
    sec_start, sec_end = find_section(html, 'skilleval-ri')
    # Include preceding comment if present
    comment = '<!-- 4. Eval 结果 -->\n'
    if comment in html and html.index(comment) < sec_start:
        sec_start = html.index(comment)
    html = html[:sec_start] + NEW_SECTION + '\n' + html[sec_end:]

    # Update nav label
    html = html.replace(
        '<button class="nav-item" data-idx="5"><span class="nav-num">06</span>Eval 结果</button>',
        '<button class="nav-item" data-idx="5"><span class="nav-num">06</span>测试结果</button>'
    )

    with open(src, 'w', encoding='utf-8') as f:
        f.write(html)

    sections = [m.group(1) for m in re.finditer(r'class="section" id="([^"]+)"', html)]
    nav_count = html.count('data-idx=')
    print(f'{src.split("/")[-1]}: {len(html.splitlines())} lines, nav={nav_count}, sections={sections}')
    assert 'id="skilleval-ri"' in html
    assert '测试结果' in html

process('/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/index.html')
process('/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/architecture-report.html')
