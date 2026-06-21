#!/usr/bin/env python3
"""
Two changes:
1. Simplify Hero → badge + large title + one-line tagline + stats
2. Insert new #overview "产品全景" section after Hero
3. Nav: 11 → 12 items (insert 产品全景 as item 2)
"""
import shutil, re

DOCS = [
    '/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/index.html',
    '/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/architecture-report.html',
]

# ── New Hero ──────────────────────────────────────────────────────────────────

OLD_HERO = '''\
<!-- Hero -->
<div class="hero">
  <h1>Boss Copilot — <span>老板的飞书数字分身</span></h1>
  <div style="display:flex;flex-direction:column;gap:8px;margin-bottom:28px;">
    <div style="display:inline-flex;align-items:center;gap:10px;justify-content:center;">
      <span style="font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#34C759;background:rgba(52,199,89,0.1);border:1px solid rgba(52,199,89,0.2);padding:2px 10px;border-radius:20px;">员工 / 老板</span>
      <span style="font-size:15px;color:#8b98b0;">发文档链接给 Bot，老板视角的批注自动写入文档</span>
    </div>
    <div style="display:inline-flex;align-items:center;gap:10px;justify-content:center;">
      <span style="font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#4F8EF7;background:rgba(79,142,247,0.1);border:1px solid rgba(79,142,247,0.2);padding:2px 10px;border-radius:20px;">老板专属</span>
      <span style="font-size:15px;color:#8b98b0;">每天 18:30 自动收到工作群消息摘要，无需逐群翻看</span>
    </div>
  </div>
  <div class="hero-stats">
    <div class="stat"><div class="stat-num">82%</div><div class="stat-label">第一阶段完成度</div></div>
    <div class="stat"><div class="stat-num">3</div><div class="stat-label">系统端数</div></div>
    <div class="stat"><div class="stat-num">989</div><div class="stat-label">Soul 数据行数</div></div>
    <div class="stat"><div class="stat-num">2</div><div class="stat-label">核心 Skill</div></div>
  </div>
</div>'''

NEW_HERO = '''\
<!-- Hero -->
<div class="hero">
  <div class="hero-badge">BOSS COPILOT · 架构汇报</div>
  <h1 style="font-size:52px;letter-spacing:-0.5px;">Boss Copilot</h1>
  <p style="font-size:20px;color:#4F8EF7;font-weight:600;margin-bottom:8px;">老板的飞书数字分身</p>
  <p style="font-size:15px;color:#8b98b0;max-width:440px;margin:0 auto 32px;">让 AI 代替老板处理两件重复性信息工作</p>
  <div class="hero-stats">
    <div class="stat"><div class="stat-num">82%</div><div class="stat-label">第一阶段完成度</div></div>
    <div class="stat"><div class="stat-num">3</div><div class="stat-label">系统端数</div></div>
    <div class="stat"><div class="stat-num">989</div><div class="stat-label">Soul 数据行数</div></div>
    <div class="stat"><div class="stat-num">2</div><div class="stat-label">核心 Skill</div></div>
  </div>
</div>'''

# ── New overview section ──────────────────────────────────────────────────────

OVERVIEW_SECTION = '''
<!-- 0. 产品全景 -->
<div class="section" id="overview">
  <div class="section-label">产品定位</div>
  <div class="section-title">Boss Copilot 解决的两个问题</div>
  <p style="color:#8b98b0;font-size:14px;margin-bottom:20px;">
    老板每天要做两件重复性信息工作：审阅员工文档、翻看工作群消息。Boss Copilot 用 AI 完全代劳这两件事。
  </p>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;flex:1;min-height:0;margin-bottom:14px;">

    <!-- 文档批注 -->
    <div style="background:#141820;border:1px solid #1e2530;border-radius:16px;padding:24px;display:flex;flex-direction:column;">
      <div style="font-size:26px;margin-bottom:10px;">🗂</div>
      <div style="font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#34C759;margin-bottom:6px;">员工 / 老板</div>
      <div style="font-size:18px;font-weight:700;color:#fff;margin-bottom:16px;">文档预审 · 批注写入</div>

      <div style="display:flex;flex-direction:column;gap:10px;flex:1;">
        <div style="display:flex;align-items:flex-start;gap:10px;">
          <div style="width:20px;height:20px;min-width:20px;background:rgba(52,199,89,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#34C759;margin-top:1px;">1</div>
          <div style="font-size:13px;color:#8b98b0;line-height:1.5;">员工发文档链接给 Bot</div>
        </div>
        <div style="display:flex;align-items:flex-start;gap:10px;">
          <div style="width:20px;height:20px;min-width:20px;background:rgba(52,199,89,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#34C759;margin-top:1px;">2</div>
          <div style="font-size:13px;color:#8b98b0;line-height:1.5;">Bot 以老板视角分析文档内容</div>
        </div>
        <div style="display:flex;align-items:flex-start;gap:10px;">
          <div style="width:20px;height:20px;min-width:20px;background:rgba(52,199,89,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#34C759;margin-top:1px;">3</div>
          <div style="font-size:13px;color:#8b98b0;line-height:1.5;">批注以老板身份直接写入飞书文档</div>
        </div>
      </div>

      <div style="margin-top:16px;padding-top:14px;border-top:1px solid #1e2530;display:flex;gap:24px;">
        <div>
          <div style="font-size:10px;color:#6b7a95;margin-bottom:3px;text-transform:uppercase;letter-spacing:0.5px;">触发方</div>
          <div style="font-size:12px;font-weight:600;color:#e2e8f0;">员工主动发起</div>
        </div>
        <div>
          <div style="font-size:10px;color:#6b7a95;margin-bottom:3px;text-transform:uppercase;letter-spacing:0.5px;">输出形式</div>
          <div style="font-size:12px;font-weight:600;color:#e2e8f0;">飞书文档批注</div>
        </div>
        <div>
          <div style="font-size:10px;color:#6b7a95;margin-bottom:3px;text-transform:uppercase;letter-spacing:0.5px;">显示身份</div>
          <div style="font-size:12px;font-weight:600;color:#34C759;">老板本人</div>
        </div>
      </div>
    </div>

    <!-- 工作群日报 -->
    <div style="background:#141820;border:1px solid #1e2530;border-radius:16px;padding:24px;display:flex;flex-direction:column;">
      <div style="font-size:26px;margin-bottom:10px;">📊</div>
      <div style="font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#4F8EF7;margin-bottom:6px;">老板专属</div>
      <div style="font-size:18px;font-weight:700;color:#fff;margin-bottom:16px;">工作群日报 · 自动汇总</div>

      <div style="display:flex;flex-direction:column;gap:10px;flex:1;">
        <div style="display:flex;align-items:flex-start;gap:10px;">
          <div style="width:20px;height:20px;min-width:20px;background:rgba(79,142,247,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#4F8EF7;margin-top:1px;">1</div>
          <div style="font-size:13px;color:#8b98b0;line-height:1.5;">18:30 定时调度自动触发</div>
        </div>
        <div style="display:flex;align-items:flex-start;gap:10px;">
          <div style="width:20px;height:20px;min-width:20px;background:rgba(79,142,247,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#4F8EF7;margin-top:1px;">2</div>
          <div style="font-size:13px;color:#8b98b0;line-height:1.5;">抓取老板所在群当日全部消息</div>
        </div>
        <div style="display:flex;align-items:flex-start;gap:10px;">
          <div style="width:20px;height:20px;min-width:20px;background:rgba(79,142,247,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#4F8EF7;margin-top:1px;">3</div>
          <div style="font-size:13px;color:#8b98b0;line-height:1.5;">精简摘要推送到老板飞书</div>
        </div>
      </div>

      <div style="margin-top:16px;padding-top:14px;border-top:1px solid #1e2530;display:flex;gap:24px;">
        <div>
          <div style="font-size:10px;color:#6b7a95;margin-bottom:3px;text-transform:uppercase;letter-spacing:0.5px;">触发方</div>
          <div style="font-size:12px;font-weight:600;color:#e2e8f0;">定时自动触发</div>
        </div>
        <div>
          <div style="font-size:10px;color:#6b7a95;margin-bottom:3px;text-transform:uppercase;letter-spacing:0.5px;">输出形式</div>
          <div style="font-size:12px;font-weight:600;color:#e2e8f0;">飞书私信</div>
        </div>
        <div>
          <div style="font-size:10px;color:#6b7a95;margin-bottom:3px;text-transform:uppercase;letter-spacing:0.5px;">可见范围</div>
          <div style="font-size:12px;font-weight:600;color:#4F8EF7;">仅老板</div>
        </div>
      </div>
    </div>

  </div>

  <!-- 共同底座 -->
  <div style="background:#0d1016;border:1px solid #1e2530;border-radius:12px;padding:12px 20px;display:flex;align-items:center;gap:14px;">
    <div style="font-size:11px;font-weight:700;color:#6b7a95;letter-spacing:1px;text-transform:uppercase;white-space:nowrap;">共同底座</div>
    <div style="flex:1;height:1px;background:#1e2530;"></div>
    <div style="display:flex;gap:20px;align-items:center;">
      <span style="font-size:12px;color:#8b98b0;">🧠 Soul 人格</span>
      <span style="font-size:12px;color:#2d3748;">·</span>
      <span style="font-size:12px;color:#8b98b0;">⚡ Skill 场景词</span>
      <span style="font-size:12px;color:#2d3748;">·</span>
      <span style="font-size:12px;color:#8b98b0;">🤖 Claude Code</span>
      <span style="font-size:12px;color:#2d3748;">·</span>
      <span style="font-size:12px;color:#8b98b0;">📱 飞书 API</span>
    </div>
  </div>
</div>'''

# ── Nav ───────────────────────────────────────────────────────────────────────

OLD_NAV = '''\
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

NEW_NAV = '''\
    <button class="nav-item active" data-idx="0"><span class="nav-num">01</span>概览</button>
    <button class="nav-item" data-idx="1"><span class="nav-num">02</span>产品全景</button>
    <button class="nav-item" data-idx="2"><span class="nav-num">03</span>Skill 能力</button>
    <button class="nav-item" data-idx="3"><span class="nav-num">04</span>日报测试</button>
    <button class="nav-item" data-idx="4"><span class="nav-num">05</span>批注测试</button>
    <button class="nav-item" data-idx="5"><span class="nav-num">06</span>系统架构</button>
    <button class="nav-item" data-idx="6"><span class="nav-num">07</span>服务流程</button>
    <button class="nav-item" data-idx="7"><span class="nav-num">08</span>产品角色</button>
    <button class="nav-item" data-idx="8"><span class="nav-num">09</span>技术选型</button>
    <button class="nav-item" data-idx="9"><span class="nav-num">10</span>框架对比</button>
    <button class="nav-item" data-idx="10"><span class="nav-num">11</span>差距与局限</button>
    <button class="nav-item" data-idx="11"><span class="nav-num">12</span>进展计划</button>'''

INSERTION_MARKER = '\n\n<!-- 1. 系统架构 -->'
AFTER_OVERVIEW   = '\n\n<!-- 1. 系统架构 -->'


def process(src):
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()

    assert OLD_HERO in html, f'OLD_HERO not found in {src}'

    # 1. Replace hero
    html = html.replace(OLD_HERO, NEW_HERO)

    # 2. Insert overview section after new hero (before the skills section marker)
    assert INSERTION_MARKER in html, f'Insertion marker not found in {src}'
    html = html.replace(INSERTION_MARKER, OVERVIEW_SECTION + AFTER_OVERVIEW, 1)

    # 3. Update nav
    assert OLD_NAV in html, f'OLD_NAV not found in {src}'
    html = html.replace(OLD_NAV, NEW_NAV)

    with open(src, 'w', encoding='utf-8') as f:
        f.write(html)

    sections = [m.group(1) for m in re.finditer(r'class="section" id="([^"]+)"', html)]
    nav_count = html.count('data-idx=')
    print(f'{src.split("/")[-1]}: {len(html.splitlines())} lines  nav={nav_count}')
    print(f'  sections={sections}')
    assert 'id="overview"' in html, 'overview section missing'
    assert html.index('id="overview"') < html.index('id="skills"'), 'overview before skills'
    assert nav_count == 12, f'expected 12 nav items, got {nav_count}'
    print('  ✓ assertions passed')


for doc in DOCS:
    process(doc)
    print()
