#!/usr/bin/env python3
"""
1. Move AI layer (4-column grid) from page 06 (#agent-arch) into page 02 (#arch)
2. Replace page 06 with original vertical-branch server flow from backup
3. Nav: "Bot 架构" → "服务流程"
"""
import shutil, re

def find_section(html, id_):
    marker = f'<div class="section" id="{id_}"'
    start = html.index(marker)
    depth = 0
    i = start
    while i < len(html):
        if html[i:i+4] == '<div':
            depth += 1; i += 4
        elif html[i:i+6] == '</div>':
            depth -= 1; i += 6
            if depth == 0:
                return start, i
        else:
            i += 1
    raise ValueError(f'unclosed section: {id_}')


def extract_div(html, start):
    """Given start index of a <div, return (end_idx) after its closing </div>."""
    depth = 0
    i = start
    while i < len(html):
        if html[i:i+4] == '<div':
            depth += 1; i += 4
        elif html[i:i+6] == '</div>':
            depth -= 1; i += 6
            if depth == 0:
                return i
        else:
            i += 1
    raise ValueError('unclosed div')


def process(src, backup_src):
    shutil.copy(src, src.replace('.html', '-pre-split-agent.html'))
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()
    with open(backup_src, 'r', encoding='utf-8') as f:
        backup = f.read()

    # ── 1. Extract original #flow section from backup ─────────────────────────
    fl_start, fl_end = find_section(backup, 'flow')
    original_flow_html = backup[fl_start:fl_end]
    # Extract just the flow-wrap div
    fw_start_idx = original_flow_html.index('<div class="flow-wrap">')
    fw_end_idx   = extract_div(original_flow_html, fw_start_idx)
    flow_wrap_html = original_flow_html[fw_start_idx:fw_end_idx]

    # ── 2. Extract 4-column AI grid from current #agent-arch ──────────────────
    ag_start, ag_end = find_section(html, 'agent-arch')
    agent_html = html[ag_start:ag_end]
    grid_marker = '<div style="display:grid;grid-template-columns:1fr 28px'
    gd_start_in_agent = agent_html.index(grid_marker)
    gd_end_in_agent   = extract_div(agent_html, gd_start_in_agent)
    grid_html = agent_html[gd_start_in_agent:gd_end_in_agent]

    # ── 3. Build new page 06: pure flow section ────────────────────────────────
    new_flow_section = '''\
<!-- 6. 服务流程 -->
<div class="section" id="agent-arch">
  <div class="section-label">服务器端职责</div>
  <div class="section-title">服务器处理流程</div>
  ''' + flow_wrap_html + '''
</div>'''

    # Replace old agent-arch (+ comment) with new flow section
    ag_comment = '<!-- 6. Bot 架构 -->\n'
    if ag_comment in html:
        replace_start = html.index(ag_comment)
    else:
        replace_start = ag_start
    html = html[:replace_start] + new_flow_section + '\n\n' + html[ag_end:]

    # ── 4. Append AI grid to page 02 (#arch) ──────────────────────────────────
    arch_start, arch_end = find_section(html, 'arch')
    # arch_end is right after the section's final </div>
    # insert before that final </div>
    last_close = html.rfind('</div>', arch_start, arch_end)

    ai_insert = '''

  <!-- AI 层分隔 -->
  <div style="display:flex;align-items:center;gap:12px;margin:20px 0 14px;">
    <div style="flex:1;height:1px;background:#1e2530;"></div>
    <span style="font-size:10px;font-weight:700;color:#6b7a95;letter-spacing:1.5px;text-transform:uppercase;white-space:nowrap;">AI 层 — Agent 分层结构</span>
    <div style="flex:1;height:1px;background:#1e2530;"></div>
  </div>
''' + grid_html + '\n'

    html = html[:last_close] + ai_insert + '</div>' + html[arch_end:]

    # ── 5. Update nav label ────────────────────────────────────────────────────
    html = html.replace(
        '<button class="nav-item" data-idx="5"><span class="nav-num">06</span>Bot 架构</button>',
        '<button class="nav-item" data-idx="5"><span class="nav-num">06</span>服务流程</button>'
    )

    with open(src, 'w', encoding='utf-8') as f:
        f.write(html)

    sections = [m.group(1) for m in re.finditer(r'class="section" id="([^"]+)"', html)]
    nav_count = html.count('data-idx=')
    print(f'{src.split("/")[-1]}: {len(html.splitlines())} lines, nav={nav_count}, sections={sections}')
    assert 'id="agent-arch"' in html
    assert 'flow-wrap' in html


process(
    '/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/index.html',
    '/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/index-pre-merge0708.html'
)
process(
    '/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/architecture-report.html',
    '/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/architecture-report-pre-merge0708.html'
)
