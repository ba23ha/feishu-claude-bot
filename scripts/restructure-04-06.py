#!/usr/bin/env python3
"""
Restructure pages 04-06:
- Page 04: compact method strip + 6 dimension cards (3 DR + 3 RI)
- Page 05: DR eval table + RI eval table + data gap
- Page 06: delete
- Nav: 15 → 14
"""
import shutil

def process(src):
    shutil.copy(src, src.replace('.html', '-pre-0406.html'))
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()

    # ── extract blocks we need ────────────────────────────────────────────────
    def between(text, start_marker, end_marker):
        s = text.index(start_marker) + len(start_marker)
        e = text.index(end_marker, s)
        return text[s:e]

    # DR dimension cards (3 cards, the grid div)
    dr_dims_start = '  <!-- 三个维度对比 -->'
    dr_dims_end   = '  <!-- eval 真实结果 -->'
    dr_dims = between(html, dr_dims_start, dr_dims_end).strip()

    # DR eval table
    dr_eval_start = '  <!-- eval 真实结果 -->'
    dr_eval_end   = '\n  </div>\n\n<!-- 4. 批注测试 -->'
    dr_eval = between(html, dr_eval_start, dr_eval_end).strip()

    # RI dimension cards + separator
    ri_dims_start = '<!-- review_inline 分隔 -->'
    ri_dims_end   = '  <!-- RI eval 结果表 -->'
    ri_dims = between(html, ri_dims_start, ri_dims_end).strip()

    # RI eval table
    ri_eval_start = '  <!-- RI eval 结果表 -->'
    ri_eval_end   = '\n</div>\n\n<!-- 5. 数据缺口 -->'
    ri_eval = between(html, ri_eval_start, ri_eval_end).strip()

    # Data gap content (just the orange box)
    gap_start = '<!-- 数据缺口 -->\n'
    gap_end   = '\n</div>\n'   # closing div of skilleval-gap section
    gap_idx   = html.index(gap_start)
    gap_section_close = html.index('\n</div>\n', gap_idx + len(gap_start))
    data_gap = html[gap_idx + len(gap_start):gap_section_close].strip()

    # ── build new page 04 ─────────────────────────────────────────────────────
    new_04 = '''\
<!-- 3. 维度对比 -->
<div class="section" id="skilleval-dr">
  <div class="section-label">测试验证</div>
  <div class="section-title">Skill 效果验证 — 核心维度对比</div>

  <!-- 方法论 compact -->
  <div style="display:flex;align-items:center;gap:10px;background:#141820;border:1px solid #1e2530;border-radius:10px;padding:10px 20px;margin-bottom:20px;flex-wrap:wrap;">
    <span style="font-size:11px;font-weight:700;color:#6b7a95;letter-spacing:1px;text-transform:uppercase;white-space:nowrap;margin-right:8px;">测试方法</span>
    <div class="flow-node" style="padding:5px 14px;font-size:12px;">同一组模拟输入</div>
    <span style="color:#2d3748;font-size:14px;">→</span>
    <div class="flow-node highlight" style="padding:5px 14px;font-size:12px;">通用模型（无 Skill）</div>
    <span style="color:#2d3748;font-size:14px;">vs</span>
    <div class="flow-node green" style="padding:5px 14px;font-size:12px;">Soul + Skill</div>
    <span style="color:#2d3748;font-size:14px;">→</span>
    <div class="flow-node" style="padding:5px 14px;font-size:12px;">对比格式 / 口吻 / 关键信息 / 禁忌词</div>
  </div>

  <!-- daily_report 分隔 -->
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
    <div style="width:28px;height:28px;background:rgba(79,142,247,0.1);border:1px solid rgba(79,142,247,0.25);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px;">📋</div>
    <div style="font-size:14px;font-weight:700;color:#fff;">daily_report — 日报生成</div>
    <div style="flex:1;height:1px;background:#1e2530;margin-left:8px;"></div>
  </div>

''' + dr_dims + '''

  <!-- review_inline 分隔 -->
  <div style="display:flex;align-items:center;gap:12px;margin:18px 0 14px;">
    <div style="width:28px;height:28px;background:rgba(52,199,89,0.1);border:1px solid rgba(52,199,89,0.25);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px;">📝</div>
    <div style="font-size:14px;font-weight:700;color:#fff;">review_inline — 文档批注</div>
    <div style="flex:1;height:1px;background:#1e2530;margin-left:8px;"></div>
  </div>

''' + ri_dims + '''
</div>
'''

    # ── build new page 05 ─────────────────────────────────────────────────────
    new_05 = '''\
<!-- 4. Eval 结果 -->
<div class="section" id="skilleval-ri">
  <div class="section-label">测试验证</div>
  <div class="section-title">Eval 测试结果 — 12 个场景</div>

  <!-- DR eval -->
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
    <div style="width:22px;height:22px;background:rgba(79,142,247,0.1);border:1px solid rgba(79,142,247,0.25);border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:12px;">📋</div>
    <span style="font-size:13px;font-weight:700;color:#4F8EF7;">daily_report</span>
    <div style="flex:1;height:1px;background:#1e2530;"></div>
  </div>

''' + dr_eval + '''

  <!-- RI eval -->
  <div style="display:flex;align-items:center;gap:10px;margin:18px 0 12px;">
    <div style="width:22px;height:22px;background:rgba(52,199,89,0.1);border:1px solid rgba(52,199,89,0.25);border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:12px;">📝</div>
    <span style="font-size:13px;font-weight:700;color:#34C759;">review_inline</span>
    <div style="flex:1;height:1px;background:#1e2530;"></div>
  </div>

''' + ri_eval + '''

  <!-- 数据缺口 -->
  <div style="margin-top:20px;">
''' + data_gap + '''
  </div>

</div>
'''

    # ── replace old sections 04/05/06 with new 04/05 ─────────────────────────
    old_block_start = '<!-- 3. 日报测试 -->\n<div class="section" id="skilleval-dr">'
    old_block_end   = '\n</div>\n\n'  # end of skilleval-gap closing

    # find end of skilleval-gap
    gap_section_open = html.index('<div class="section" id="skilleval-gap">')
    # find its closing </div>
    depth = 0
    i = gap_section_open
    while i < len(html):
        if html[i:i+4] == '<div':
            depth += 1; i += 4
        elif html[i:i+6] == '</div>':
            depth -= 1; i += 6
            if depth == 0:
                break
        else:
            i += 1
    old_end_idx = i  # right after </div> of skilleval-gap

    # find start of old block
    old_start_idx = html.index('<!-- 3. 日报测试 -->')

    # skip any trailing newlines after skilleval-gap
    while old_end_idx < len(html) and html[old_end_idx] == '\n':
        old_end_idx += 1

    html_new = html[:old_start_idx] + new_04 + '\n' + new_05 + '\n' + html[old_end_idx:]

    # ── update nav 15 → 14 ───────────────────────────────────────────────────
    old_nav = '''\
    <button class="nav-item active" data-idx="0"><span class="nav-num">01</span>概览</button>
    <button class="nav-item" data-idx="1"><span class="nav-num">02</span>系统架构</button>
    <button class="nav-item" data-idx="2"><span class="nav-num">03</span>Skill 能力</button>
    <button class="nav-item" data-idx="3"><span class="nav-num">04</span>日报测试</button>
    <button class="nav-item" data-idx="4"><span class="nav-num">05</span>批注测试</button>
    <button class="nav-item" data-idx="5"><span class="nav-num">06</span>数据缺口</button>
    <button class="nav-item" data-idx="6"><span class="nav-num">07</span>Agent 架构</button>
    <button class="nav-item" data-idx="7"><span class="nav-num">08</span>服务器流程</button>
    <button class="nav-item" data-idx="8"><span class="nav-num">09</span>权限体系</button>
    <button class="nav-item" data-idx="9"><span class="nav-num">10</span>技术选型</button>
    <button class="nav-item" data-idx="10"><span class="nav-num">11</span>框架对比</button>
    <button class="nav-item" data-idx="11"><span class="nav-num">12</span>框架分析</button>
    <button class="nav-item" data-idx="12"><span class="nav-num">13</span>方案评估</button>
    <button class="nav-item" data-idx="13"><span class="nav-num">14</span>关键决策</button>
    <button class="nav-item" data-idx="14"><span class="nav-num">15</span>进展计划</button>'''

    new_nav = '''\
    <button class="nav-item active" data-idx="0"><span class="nav-num">01</span>概览</button>
    <button class="nav-item" data-idx="1"><span class="nav-num">02</span>系统架构</button>
    <button class="nav-item" data-idx="2"><span class="nav-num">03</span>Skill 能力</button>
    <button class="nav-item" data-idx="3"><span class="nav-num">04</span>维度对比</button>
    <button class="nav-item" data-idx="4"><span class="nav-num">05</span>Eval 结果</button>
    <button class="nav-item" data-idx="5"><span class="nav-num">06</span>Agent 架构</button>
    <button class="nav-item" data-idx="6"><span class="nav-num">07</span>服务器流程</button>
    <button class="nav-item" data-idx="7"><span class="nav-num">08</span>权限体系</button>
    <button class="nav-item" data-idx="8"><span class="nav-num">09</span>技术选型</button>
    <button class="nav-item" data-idx="9"><span class="nav-num">10</span>框架对比</button>
    <button class="nav-item" data-idx="10"><span class="nav-num">11</span>框架分析</button>
    <button class="nav-item" data-idx="11"><span class="nav-num">12</span>方案评估</button>
    <button class="nav-item" data-idx="12"><span class="nav-num">13</span>关键决策</button>
    <button class="nav-item" data-idx="13"><span class="nav-num">14</span>进展计划</button>'''

    html_new = html_new.replace(old_nav, new_nav)

    with open(src, 'w', encoding='utf-8') as f:
        f.write(html_new)

    # sanity checks
    assert 'id="skilleval-gap"' not in html_new, "skilleval-gap should be deleted"
    assert 'id="skilleval-dr"' in html_new
    assert 'id="skilleval-ri"' in html_new
    nav_count = html_new.count('class="nav-item"') + html_new.count('class="nav-item active"')
    print(f"{src}: {len(html_new.splitlines())} lines, nav={nav_count}, gap_deleted=OK")

process('/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/index.html')
process('/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/architecture-report.html')
