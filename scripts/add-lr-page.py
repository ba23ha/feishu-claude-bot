#!/usr/bin/env python3
"""
After page 04 (#skilleval-dr), insert a new page (#skilleval-lr) with the
same content but daily_report on the left and review_inline on the right.
Nav: 12 → 13
"""
import shutil, re

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

def extract_div_end(html, start):
    depth = 0; i = start
    while i < len(html):
        if html[i:i+4] == '<div':  depth += 1; i += 4
        elif html[i:i+6] == '</div>': depth -= 1; i += 6
        else: i += 1
        if depth == 0: return i
    raise ValueError('unclosed')

OLD_NAV = '''\
    <button class="nav-item active" data-idx="0"><span class="nav-num">01</span>概览</button>
    <button class="nav-item" data-idx="1"><span class="nav-num">02</span>系统架构</button>
    <button class="nav-item" data-idx="2"><span class="nav-num">03</span>Skill 能力</button>
    <button class="nav-item" data-idx="3"><span class="nav-num">04</span>维度对比</button>
    <button class="nav-item" data-idx="4"><span class="nav-num">05</span>Eval 结果</button>
    <button class="nav-item" data-idx="5"><span class="nav-num">06</span>服务流程</button>
    <button class="nav-item" data-idx="6"><span class="nav-num">07</span>产品角色</button>
    <button class="nav-item" data-idx="7"><span class="nav-num">08</span>技术选型</button>
    <button class="nav-item" data-idx="8"><span class="nav-num">09</span>框架对比</button>
    <button class="nav-item" data-idx="9"><span class="nav-num">10</span>框架分析</button>
    <button class="nav-item" data-idx="10"><span class="nav-num">11</span>方案评估</button>
    <button class="nav-item" data-idx="11"><span class="nav-num">12</span>进展计划</button>'''

NEW_NAV = '''\
    <button class="nav-item active" data-idx="0"><span class="nav-num">01</span>概览</button>
    <button class="nav-item" data-idx="1"><span class="nav-num">02</span>系统架构</button>
    <button class="nav-item" data-idx="2"><span class="nav-num">03</span>Skill 能力</button>
    <button class="nav-item" data-idx="3"><span class="nav-num">04</span>维度对比</button>
    <button class="nav-item" data-idx="4"><span class="nav-num">05</span>维度双列</button>
    <button class="nav-item" data-idx="5"><span class="nav-num">06</span>Eval 结果</button>
    <button class="nav-item" data-idx="6"><span class="nav-num">07</span>服务流程</button>
    <button class="nav-item" data-idx="7"><span class="nav-num">08</span>产品角色</button>
    <button class="nav-item" data-idx="8"><span class="nav-num">09</span>技术选型</button>
    <button class="nav-item" data-idx="9"><span class="nav-num">10</span>框架对比</button>
    <button class="nav-item" data-idx="10"><span class="nav-num">11</span>框架分析</button>
    <button class="nav-item" data-idx="11"><span class="nav-num">12</span>方案评估</button>
    <button class="nav-item" data-idx="12"><span class="nav-num">13</span>进展计划</button>'''


def process(src):
    shutil.copy(src, src.replace('.html', '-pre-lr.html'))
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()

    sec_start, sec_end = find_section(html, 'skilleval-dr')
    sec = html[sec_start:sec_end]

    # ── Method strip ──────────────────────────────────────────────────────────
    ms_idx  = sec.index('<!-- 方法论 compact -->')
    ms_div  = sec.index('<div', ms_idx)
    ms_end  = extract_div_end(sec, ms_div)
    method_strip = sec[ms_div:ms_end]

    # ── DR separator div ──────────────────────────────────────────────────────
    dr_idx  = sec.index('<!-- daily_report 分隔 -->')
    dr_div  = sec.index('<div', dr_idx)
    dr_end  = extract_div_end(sec, dr_div)
    dr_sep  = sec[dr_div:dr_end]

    # DR subtitle + 3-col grid  (between DR sep end and RI comment)
    ri_comment = '<!-- review_inline 分隔 -->'
    ri_comment_idx = sec.index(ri_comment)
    dr_block = sec[dr_end:ri_comment_idx].strip()
    # Change 3-col → 1-col for the column view
    dr_block = dr_block.replace(
        'grid-template-columns:1fr 1fr 1fr;gap:16px;margin-bottom:28px;',
        'grid-template-columns:1fr;gap:10px;margin-bottom:0;'
    )

    # ── RI separator div ──────────────────────────────────────────────────────
    ri_div  = sec.index('<div', ri_comment_idx)
    ri_end  = extract_div_end(sec, ri_div)
    ri_sep  = sec[ri_div:ri_end]

    # RI subtitle + 3-col grid  (between RI sep end and section-closing </div>)
    ri_block = sec[ri_end:].strip()
    # Remove the section's closing </div>
    if ri_block.endswith('</div>'):
        ri_block = ri_block[:-6].rstrip()
    # Change 3-col → 1-col
    ri_block = ri_block.replace(
        'grid-template-columns:1fr 1fr 1fr;gap:16px;margin-bottom:28px;',
        'grid-template-columns:1fr;gap:10px;margin-bottom:0;'
    )

    # ── Build new page ─────────────────────────────────────────────────────────
    new_page = f'''\

<!-- 3b. 维度对比·双列 -->
<div class="section" id="skilleval-lr">
  <div class="section-label">测试验证</div>
  <div class="section-title">Skill 效果验证 — 维度对比双列视图</div>

  {method_strip}

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;flex:1;min-height:0;margin-top:16px;">

    <!-- 左列: daily_report -->
    <div style="display:flex;flex-direction:column;gap:10px;min-height:0;overflow:hidden;">
      {dr_sep}
      {dr_block}
    </div>

    <!-- 右列: review_inline -->
    <div style="display:flex;flex-direction:column;gap:10px;min-height:0;overflow:hidden;">
      {ri_sep}
      {ri_block}
    </div>

  </div>
</div>'''

    # Insert right after #skilleval-dr section
    html = html[:sec_end] + new_page + '\n' + html[sec_end:]

    # Update nav
    assert OLD_NAV in html, 'Old nav not found'
    html = html.replace(OLD_NAV, NEW_NAV)

    with open(src, 'w', encoding='utf-8') as f:
        f.write(html)

    sections = [m.group(1) for m in re.finditer(r'class="section" id="([^"]+)"', html)]
    nav_count = html.count('data-idx=')
    print(f'{src.split("/")[-1]}: {len(html.splitlines())} lines, nav={nav_count}, sections={sections}')
    assert 'id="skilleval-lr"' in html
    assert 'id="skilleval-dr"' in html


process('/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/index.html')
process('/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/architecture-report.html')
