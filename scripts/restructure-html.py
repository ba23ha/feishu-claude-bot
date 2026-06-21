#!/usr/bin/env python3
"""
Restructure docs/index.html:
1. Split #skilleval into 3 pages (dr / ri / gap)
2. Split #framework-compare into 2 pages (table / analysis)
3. Move skilleval pages after #skills (靠拢)
4. Update navigation 12 → 15 items
"""

import re, shutil, os

src = '/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/index.html'
# backup
shutil.copy(src, src.replace('.html', '-pre-restructure.html'))

with open(src, 'r', encoding='utf-8') as f:
    html = f.read()

# ── helper: extract a top-level div block starting at `marker` ───────────────
def extract_block(text, marker):
    """Return (block_str, before_idx, after_idx) for the first div starting at/after marker."""
    start = text.index(marker)
    # find the opening <div at start
    div_start = text.rindex('<div', 0, start + len(marker))
    depth = 0
    i = div_start
    while i < len(text):
        if text[i:i+4] == '<div':
            depth += 1
            i += 4
        elif text[i:i+6] == '</div>':
            depth -= 1
            i += 6
            if depth == 0:
                return text[div_start:i], div_start, i
        else:
            i += 1
    raise ValueError(f"Unmatched div at marker: {marker[:60]}")

# ── extract all current sections ─────────────────────────────────────────────
heroes, h_s, h_e         = extract_block(html, '<div class="hero"')
arch_b, a_s, a_e         = extract_block(html, 'id="arch"')
skills_b, sk_s, sk_e     = extract_block(html, 'id="skills"')
agarch_b, ag_s, ag_e     = extract_block(html, 'id="agent-arch"')
flow_b, fl_s, fl_e       = extract_block(html, 'id="flow"')
perm_b, pe_s, pe_e       = extract_block(html, 'id="perm"')
techc_b, tc_s, tc_e      = extract_block(html, 'id="tech-compare"')
framec_b, fc_s, fc_e     = extract_block(html, 'id="framework-compare"')
eval_b, ev_s, ev_e       = extract_block(html, 'id="eval"')
skillev_b, se_s, se_e    = extract_block(html, 'id="skilleval"')
decision_b, dc_s, dc_e   = extract_block(html, 'id="decision"')
status_b, st_s, st_e     = extract_block(html, 'id="status"')

# ── split #framework-compare ─────────────────────────────────────────────────
# The section has: table + legend (keep in page A) | 2 advantage/gap cards (page B)
# Split point: the grid div holding the two cards starts with:
split_marker_fc = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">'
fc_split_idx = framec_b.index(split_marker_fc)

# page A: table + legend
framec_a = (
    framec_b[:fc_split_idx].rstrip()
    + '\n</div>\n'  # close section
)
# page B: advantage/gap cards in new section
framec_cards = framec_b[fc_split_idx:].rstrip()
# Remove the trailing </div> of the original section (last one)
if framec_cards.endswith('</div>'):
    framec_cards = framec_cards[:-6]  # remove outer section-closing </div>
framec_b_new = (
    '<div class="section" id="framework-gap">\n'
    '  <div class="section-label">框架对比</div>\n'
    '  <div class="section-title">与成熟框架的优势 &amp; 差距</div>\n'
    + framec_cards
    + '\n</div>\n'
)

# ── split #skilleval into 3 sections ─────────────────────────────────────────
se = skillev_b

# --- page A: skilleval-dr ---
# Contains: section header, intro, methodology box, daily_report block
# daily_report block starts right after methodology box closing div
# review_inline separator starts with this marker:
ri_sep_marker = '<!-- review_inline 分隔 -->'
ri_sep_idx = se.index(ri_sep_marker)

# Build page A (modify section id, keep content up to ri_sep_idx)
se_a_inner = se[se.index('>')+1:ri_sep_idx]  # content after opening <div ...>
skillev_dr = (
    '<div class="section" id="skilleval-dr">\n'
    '  <div class="section-label">测试验证</div>\n'
    '  <div class="section-title">日报 Skill 测试对比</div>\n'
    '  <p style="color:#8b98b0;font-size:14px;margin-bottom:28px;max-width:680px;">'
    '通过 Eval 框架对比通用模型（无 Skill）与 Soul + Skill 在同一输入下的输出差异，量化 Skill 建设的价值。'
    '共 12 个测试用例，下方为 daily_report（日报生成）的测试结果。</p>\n'
    + se[se.index('\n', se.index('>')):ri_sep_idx].lstrip('\n')
    + '</div>\n'
)

# --- page B: skilleval-ri ---
# Contains: review_inline content
# data gap section starts with:
gap_marker = '<!-- 数据缺口 -->'
gap_idx = se.index(gap_marker)

ri_content = se[ri_sep_idx:gap_idx].strip()
skillev_ri = (
    '<div class="section" id="skilleval-ri">\n'
    '  <div class="section-label">测试验证</div>\n'
    '  <div class="section-title">文档批注 Skill 测试对比</div>\n'
    + ri_content
    + '\n</div>\n'
)

# --- page C: skilleval-gap ---
gap_content = se[gap_idx:].rstrip()
# Remove trailing </div> of original section
if gap_content.endswith('</div>'):
    gap_content = gap_content[:-6]
skillev_gap = (
    '<div class="section" id="skilleval-gap">\n'
    '  <div class="section-label">测试验证</div>\n'
    '  <div class="section-title">当前测试数据缺口</div>\n'
    + gap_content
    + '\n</div>\n'
)

# ── assemble new fp-container contents ───────────────────────────────────────
fp_open = '<div class="fp-container" id="fp-container">'
fp_close_marker = '\n<script>'
fp_start = html.index(fp_open) + len(fp_open)
fp_end = html.index(fp_close_marker)

new_body = (
    '\n\n'
    '<!-- Hero -->\n' + heroes + '\n\n'
    '<!-- 1. 系统架构 -->\n' + arch_b + '\n\n'
    '<!-- 2. Skill 能力 -->\n' + skills_b + '\n\n'
    '<!-- 3. 日报测试 -->\n' + skillev_dr + '\n'
    '<!-- 4. 批注测试 -->\n' + skillev_ri + '\n'
    '<!-- 5. 数据缺口 -->\n' + skillev_gap + '\n'
    '<!-- 6. Agent 架构 -->\n' + agarch_b + '\n\n'
    '<!-- 7. 服务器流程 -->\n' + flow_b + '\n\n'
    '<!-- 8. 权限体系 -->\n' + perm_b + '\n\n'
    '<!-- 9. 技术选型 -->\n' + techc_b + '\n\n'
    '<!-- 10. 框架对比·表 -->\n' + framec_a + '\n'
    '<!-- 11. 框架对比·分析 -->\n' + framec_b_new + '\n'
    '<!-- 12. 方案评估 -->\n' + eval_b + '\n\n'
    '<!-- 13. 关键决策 -->\n' + decision_b + '\n\n'
    '<!-- 14. 进展计划 -->\n' + status_b + '\n'
)

html_new = html[:fp_start] + new_body + html[fp_end:]

# ── update navigation ─────────────────────────────────────────────────────────
old_nav = '''    <button class="nav-item active" data-idx="0"><span class="nav-num">01</span>概览</button>
    <button class="nav-item" data-idx="1"><span class="nav-num">02</span>系统架构</button>
    <button class="nav-item" data-idx="2"><span class="nav-num">03</span>Skill 能力</button>
    <button class="nav-item" data-idx="3"><span class="nav-num">04</span>Agent 架构</button>
    <button class="nav-item" data-idx="4"><span class="nav-num">05</span>服务器流程</button>
    <button class="nav-item" data-idx="5"><span class="nav-num">06</span>权限体系</button>
    <button class="nav-item" data-idx="6"><span class="nav-num">07</span>技术选型</button>
    <button class="nav-item" data-idx="7"><span class="nav-num">08</span>框架对比</button>
    <button class="nav-item" data-idx="8"><span class="nav-num">09</span>方案评估</button>
    <button class="nav-item" data-idx="9"><span class="nav-num">10</span>测试对比</button>
    <button class="nav-item" data-idx="10"><span class="nav-num">11</span>关键决策</button>
    <button class="nav-item" data-idx="11"><span class="nav-num">12</span>进展计划</button>'''

new_nav = '''    <button class="nav-item active" data-idx="0"><span class="nav-num">01</span>概览</button>
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

html_new = html_new.replace(old_nav, new_nav)

# ── write output ──────────────────────────────────────────────────────────────
with open(src, 'w', encoding='utf-8') as f:
    f.write(html_new)

print(f"Done. Lines: {len(html_new.splitlines())}")

# Quick sanity checks
for id_ in ['skilleval-dr', 'skilleval-ri', 'skilleval-gap', 'framework-gap']:
    assert f'id="{id_}"' in html_new, f"Missing: {id_}"
print("All section IDs present.")

nav_count = html_new.count('class="nav-item"')
print(f"Nav items: {nav_count}")
