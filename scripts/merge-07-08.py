#!/usr/bin/env python3
"""
Merge #agent-arch (07) + #flow (08) into one page.
- Top half: 4-layer Agent arch (compact, no intro para)
- Divider
- Bottom half: compressed server flow (no flow-desc, no legend, tight padding)
Nav: 14 → 13
"""
import shutil, re

def process(src):
    shutil.copy(src, src.replace('.html', '-pre-merge0708.html'))
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()

    # ── find & extract both sections ─────────────────────────────────────────
    def extract_section(text, id_):
        marker = f'id="{id_}"'
        start = text.index(f'<div class="section" {marker}')
        depth = 0
        i = start
        while i < len(text):
            if text[i:i+4] == '<div':
                depth += 1; i += 4
            elif text[i:i+6] == '</div>':
                depth -= 1; i += 6
                if depth == 0:
                    return start, i, text[start:i]
            else:
                i += 1
        raise ValueError(f"unclosed div for {id_}")

    ag_start, ag_end, agent_html = extract_section(html, 'agent-arch')
    fl_start, fl_end, flow_html  = extract_section(html, 'flow')

    # ── build compact agent-arch (upper half) ────────────────────────────────
    # Extract just the 4-block grid (between grid div and its closing)
    grid_start = agent_html.index('<div style="display:grid;grid-template-columns:1fr 28px')
    # find closing of that grid div
    depth = 0
    i = grid_start
    while i < len(agent_html):
        if agent_html[i:i+4] == '<div':
            depth += 1; i += 4
        elif agent_html[i:i+6] == '</div>':
            depth -= 1; i += 6
            if depth == 0:
                break
        else:
            i += 1
    grid_html = agent_html[grid_start:i]

    # Reduce block padding from 18px 16px → 12px 14px
    grid_html = grid_html.replace('padding:18px 16px', 'padding:12px 14px')
    # Remove bottom margin that was 36px
    grid_html = grid_html.replace('margin-bottom:36px', 'margin-bottom:0')

    agent_compact = grid_html

    # ── build compact flow (lower half) ──────────────────────────────────────
    # 1. Remove all flow-desc divs (with their content)
    flow_c = re.sub(r'\s*<div class="flow-desc">[^<]*</div>', '', flow_html)
    # 2. Remove the flow-legend block
    flow_c = re.sub(r'\s*<div class="flow-legend">.*?</div>\s*', '\n', flow_c, flags=re.DOTALL)
    # 3. Compact flow-always: reduce padding-top and margin-top
    flow_c = flow_c.replace('padding-top: 24px;\n    border-top: 1px dashed #1e2530;\n    margin-top: 24px;',
                             'padding-top: 12px;\n    border-top: 1px dashed #1e2530;\n    margin-top: 12px;')
    # 4. Reduce flow-wrap padding from 32px 28px → 14px 20px
    flow_c = flow_c.replace('padding: 32px 28px', 'padding: 14px 20px')
    # 5. Make v-lines shorter (16px → 8px)
    flow_c = flow_c.replace('height: 16px;\n  background: #2d3748;', 'height: 8px;\n  background: #2d3748;')
    # also inline style version
    flow_c = flow_c.replace(
        '<div class="v-line"></div>',
        '<div style="width:2px;height:8px;background:#2d3748;margin:0 auto;"></div>'
    )
    # 6. Remove the "分支说明" gap (60px → 28px)
    flow_c = flow_c.replace('gap:60px;margin-bottom:4px', 'gap:40px;margin-bottom:2px')
    # 7. Reduce fork/merge line heights from 28px → 16px
    flow_c = flow_c.replace(
        'style="position:relative;height:28px;margin:0 60px;"',
        'style="position:relative;height:16px;margin:0 60px;"'
    )
    # 8. Reduce branch grid gap
    flow_c = flow_c.replace('display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-bottom:0',
                             'display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:0')

    # Extract just the flow-wrap div (strip outer section wrapper)
    fw_start = flow_c.index('<div class="flow-wrap">')
    fw_depth = 0
    fi = fw_start
    while fi < len(flow_c):
        if flow_c[fi:fi+4] == '<div':
            fw_depth += 1; fi += 4
        elif flow_c[fi:fi+6] == '</div>':
            fw_depth -= 1; fi += 6
            if fw_depth == 0:
                break
        else:
            fi += 1
    flow_wrap_html = flow_c[fw_start:fi]

    # ── assemble merged section ───────────────────────────────────────────────
    merged = '''\
<div class="section" id="agent-arch">
  <div class="section-label">架构解析</div>
  <div class="section-title">Bot 完整处理架构 · AI 层 + 服务层</div>

  <!-- AI 层: 4层架构 -->
  <div style="font-size:10px;font-weight:700;color:#6b7a95;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;">AI 层 — Agent 分层结构</div>
''' + agent_compact + '''

  <!-- 分隔 -->
  <div style="display:flex;align-items:center;gap:12px;margin:14px 0 10px;">
    <div style="flex:1;height:1px;background:#1e2530;"></div>
    <span style="font-size:10px;font-weight:700;color:#6b7a95;letter-spacing:1.5px;text-transform:uppercase;white-space:nowrap;">服务层 — 请求处理流程</span>
    <div style="flex:1;height:1px;background:#1e2530;"></div>
  </div>

''' + flow_wrap_html + '''
</div>
'''

    # ── replace old two sections with merged ─────────────────────────────────
    # Find the comment before agent-arch and the end of flow
    # Comment before agent-arch
    comment_before = '<!-- 6. Agent 架构 -->\n'
    if comment_before in html:
        replace_start = html.index(comment_before)
    else:
        replace_start = ag_start

    # End of flow section
    replace_end = fl_end

    # Skip trailing whitespace/newlines
    while replace_end < len(html) and html[replace_end] == '\n':
        replace_end += 1

    html_new = html[:replace_start] + '<!-- 6. Bot 架构 -->\n' + merged + '\n' + html[replace_end:]

    # ── update nav: remove "07 服务器流程", renumber 06→14 ───────────────────
    old_nav = '''\
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

    new_nav = '''\
    <button class="nav-item active" data-idx="0"><span class="nav-num">01</span>概览</button>
    <button class="nav-item" data-idx="1"><span class="nav-num">02</span>系统架构</button>
    <button class="nav-item" data-idx="2"><span class="nav-num">03</span>Skill 能力</button>
    <button class="nav-item" data-idx="3"><span class="nav-num">04</span>维度对比</button>
    <button class="nav-item" data-idx="4"><span class="nav-num">05</span>Eval 结果</button>
    <button class="nav-item" data-idx="5"><span class="nav-num">06</span>Bot 架构</button>
    <button class="nav-item" data-idx="6"><span class="nav-num">07</span>权限体系</button>
    <button class="nav-item" data-idx="7"><span class="nav-num">08</span>技术选型</button>
    <button class="nav-item" data-idx="8"><span class="nav-num">09</span>框架对比</button>
    <button class="nav-item" data-idx="9"><span class="nav-num">10</span>框架分析</button>
    <button class="nav-item" data-idx="10"><span class="nav-num">11</span>方案评估</button>
    <button class="nav-item" data-idx="11"><span class="nav-num">12</span>关键决策</button>
    <button class="nav-item" data-idx="12"><span class="nav-num">13</span>进展计划</button>'''

    html_new = html_new.replace(old_nav, new_nav)

    with open(src, 'w', encoding='utf-8') as f:
        f.write(html_new)

    # sanity checks
    assert 'id="agent-arch"' in html_new
    assert 'id="flow"' not in html_new, "#flow should be merged away"
    nav_count = html_new.count('nav-item')
    sections = [m.group(1) for m in re.finditer(r'class="section" id="([^"]+)"', html_new)]
    print(f"{src.split('/')[-1]}: {len(html_new.splitlines())} lines, nav≈{nav_count}, sections={sections}")

process('/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/index.html')
process('/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/architecture-report.html')
