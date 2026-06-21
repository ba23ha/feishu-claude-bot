#!/usr/bin/env python3
"""
Major page restructure:

Old order (12):
  hero, arch(02), skills(03), skilleval-dr(04), skilleval-lr(05),
  agent-arch(06), perm(07), tech-compare(08), framework-compare(09),
  framework-gap(10), eval(11), status(12)

New order (11):
  hero, skills(02), skilleval-dr(03), skilleval-lr(04),
  arch(05), agent-arch(06), perm(07),
  tech-compare+pros(08), framework-compare(09), framework-gap+cons(10),
  status(11)

Changes:
  - skills/skilleval-dr/skilleval-lr move before arch
  - tech-compare: append eval pros as "当前方案优势"
  - framework-gap: rename labels + append eval cons as "运维局限"
  - eval: deleted (content absorbed)
  - Nav: 12 → 11 items
"""
import shutil, re

DOCS = [
    '/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/index.html',
    '/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/architecture-report.html',
]

SECTION_IDS = [
    'arch', 'skills', 'skilleval-dr', 'skilleval-lr',
    'agent-arch', 'perm', 'tech-compare', 'framework-compare',
    'framework-gap', 'eval', 'status',
]

NEW_ORDER = [
    'skills', 'skilleval-dr', 'skilleval-lr',
    'arch', 'agent-arch', 'perm',
    'tech-compare', 'framework-compare', 'framework-gap',
    'status',
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


# ── Content to inject into tech-compare ──────────────────────────────────────

PROS_ADDON = '''
  <!-- ── 当前方案优势 ─────────────────────────────────────────────────── -->
  <div style="margin-top:16px;">
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
'''

# ── Content to inject into framework-gap ─────────────────────────────────────

CONS_ADDON = '''
  <!-- ── 运维局限 ────────────────────────────────────────────────────── -->
  <div style="margin-top:16px;">
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
'''

# ── Nav ───────────────────────────────────────────────────────────────────────

OLD_NAV = '''\
    <button class="nav-item active" data-idx="0"><span class="nav-num">01</span>概览</button>
    <button class="nav-item" data-idx="1"><span class="nav-num">02</span>系统架构</button>
    <button class="nav-item" data-idx="2"><span class="nav-num">03</span>Skill 能力</button>
    <button class="nav-item" data-idx="3"><span class="nav-num">04</span>日报测试</button>
    <button class="nav-item" data-idx="4"><span class="nav-num">05</span>批注测试</button>
    <button class="nav-item" data-idx="5"><span class="nav-num">06</span>服务流程</button>
    <button class="nav-item" data-idx="6"><span class="nav-num">07</span>产品角色</button>
    <button class="nav-item" data-idx="7"><span class="nav-num">08</span>技术选型</button>
    <button class="nav-item" data-idx="8"><span class="nav-num">09</span>框架对比</button>
    <button class="nav-item" data-idx="9"><span class="nav-num">10</span>差距与局限</button>
    <button class="nav-item" data-idx="10"><span class="nav-num">11</span>进展计划</button>'''

# (already 11-item from previous restructure — if file still has 12, handle below)
OLD_NAV_12 = '''\
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

NEW_NAV = '''\
    <button class="nav-item active" data-idx="0"><span class="nav-num">01</span>概览</button>
    <button class="nav-item" data-idx="1"><span class="nav-num">02</span>Skill 能力</button>
    <button class="nav-item" data-idx="2"><span class="nav-num">03</span>日报测试</button>
    <button class="nav-item" data-idx="3"><span class="nav-num">04</span>批注测试</button>
    <button class="nav-item" data-idx="4"><span class="nav-num">05</span>系统架构</button>
    <button class="nav-item" data-idx="5"><span class="nav-num">06</span>服务流程</button>
    <button class="nav-item" data-idx="6"><span class="nav-num">07</span>产品角色</button>
    <button class="nav-item" data-idx="7"><span class="nav-num">08</span>技术选型</button>
    <button class="nav-item" data-idx="8"><span class="nav-num">09</span>框架对比</button>
    <button class="nav-item" data-idx="9"><span class="nav-num">10</span>差距与局限</button>
    <button class="nav-item" data-idx="10"><span class="nav-num">11</span>进展计划</button>'''


def process(src):
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract positions
    positions = {id_: find_section(html, id_) for id_ in SECTION_IDS}
    raw = {id_: html[s:e] for id_, (s, e) in positions.items()}

    # Preamble = everything before the earliest section start
    preamble = html[:min(s for s, _ in positions.values())]
    # Postamble = everything after the latest section end
    postamble = html[max(e for _, e in positions.values()):]

    # ── Modify tech-compare ───────────────────────────────────────────────────
    tc = raw['tech-compare']
    tc = tc.replace(
        '<div class="section-title">以模型为底层 vs 成熟 Agent 框架</div>',
        '<div class="section-title">技术选型 & 方案优势</div>'
    )
    # Append pros before the section's closing </div>
    tc = tc[:tc.rfind('</div>')] + PROS_ADDON + '</div>'

    # ── Modify framework-gap ──────────────────────────────────────────────────
    fg = raw['framework-gap']
    fg = fg.replace(
        '<div class="section-label">框架对比</div>',
        '<div class="section-label">局限与差距</div>'
    )
    fg = fg.replace(
        '<div class="section-title">与成熟框架的优势 &amp; 差距</div>',
        '<div class="section-title">架构差距与运维局限</div>'
    )
    # Append cons before the section's closing </div>
    fg = fg[:fg.rfind('</div>')] + CONS_ADDON + '</div>'

    # ── Reassemble ────────────────────────────────────────────────────────────
    modified = {**raw, 'tech-compare': tc, 'framework-gap': fg}
    body = '\n\n'.join(modified[id_] for id_ in NEW_ORDER)
    html = preamble + body + postamble

    # ── Nav ───────────────────────────────────────────────────────────────────
    if OLD_NAV_12 in html:
        html = html.replace(OLD_NAV_12, NEW_NAV)
    elif OLD_NAV in html:
        html = html.replace(OLD_NAV, NEW_NAV)
    else:
        raise AssertionError('Nav not found in ' + src)

    with open(src, 'w', encoding='utf-8') as f:
        f.write(html)

    sections = [m.group(1) for m in re.finditer(r'class="section" id="([^"]+)"', html)]
    nav_count = html.count('data-idx=')
    print(f'{src.split("/")[-1]}: {len(html.splitlines())} lines  nav={nav_count}')
    print(f'  sections={sections}')
    assert 'id="eval"' not in html,         'eval should be gone'
    assert html.index('id="skills"') < html.index('id="arch"'), 'skills before arch'
    assert html.index('id="arch"') < html.index('id="agent-arch"'), 'arch before agent-arch'
    assert nav_count == 11, f'expected 11 nav items, got {nav_count}'


for doc in DOCS:
    process(doc)
    print()
