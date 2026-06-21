#!/usr/bin/env python3
"""
Merge #perm (07 权限体系) + #decision (12 关键决策) into one page.
Layout: 2-column grid
  Left:  2 conclusion-cards stacked (Bot定位 / 配置管理暂缓)
  Right: 2 perm-cards stacked (飞书平台层 / 代码层)
Nav: 13 → 12, remove 关键决策, rename 权限体系→产品角色
"""
import shutil, re

MERGED_SECTION = '''\
<!-- 7. 产品角色设计 -->
<div class="section" id="perm">
  <div class="section-label">产品角色设计</div>
  <div class="section-title">Bot 定位 · 权限体系 · 配置管理</div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;flex:1;min-height:0;">

    <!-- 左列：产品决策 -->
    <div style="display:flex;flex-direction:column;gap:10px;min-height:0;">

      <!-- 决策A: Bot定位 -->
      <div class="conclusion-card" style="flex:1;min-height:0;padding:12px 14px;overflow:hidden;">
        <div class="conclusion-tag">架构决策</div>
        <div class="conclusion-icon" style="font-size:20px;margin-bottom:6px;">🤖</div>
        <div class="conclusion-title">无需区分多个 Bot，定位统一为老板代理人</div>
        <div class="conclusion-body" style="font-size:12px;">
          老板和员工使用的是<strong>同一个 Bot</strong>，回复口吻始终模拟老板本人说话——员工发文档，批注显示为老板写的；员工问问题，回复是老板风格的答复。这与"数字分身"定位完全一致。<br><br>
          拆成多个 Bot（老板专用 / 员工专用）的唯一好处是功能隔离，但当前员工侧功能本来就少，隔离价值低，两套 App ID + 两个 OAuth + 两个 WebSocket 连接的运维成本远大于收益。<br><br>
          <strong>功能层面的权限隔离已在代码层完成</strong>，无需靠拆 Bot 实现。
        </div>
      </div>

      <!-- 决策B: 配置管理暂缓 -->
      <div class="conclusion-card" style="flex:1;min-height:0;padding:12px 14px;overflow:hidden;">
        <div class="conclusion-tag orange">风险提示</div>
        <div class="conclusion-icon" style="font-size:20px;margin-bottom:6px;">⚠️</div>
        <div class="conclusion-title">管理员 / 员工自主配置 Agent 的业务实现难点</div>
        <div class="conclusion-body" style="font-size:12px;">
          由非技术人员通过自然语言管理 Agent 配置，在业务层面面临以下核心风险：
        </div>
        <div class="risk-list">
          <div class="risk-item" style="padding:5px 10px;font-size:11px;"><strong>意图歧义</strong>——"把 review 风格改简洁一点"，AI 无法确定改哪里、改多少，容易误改关键规则</div>
          <div class="risk-item" style="padding:5px 10px;font-size:11px;"><strong>富文本修改风险</strong>——Soul / Skill 是 Markdown，通过聊天编辑等于让 AI 代写代码，一次误操作影响所有用户</div>
          <div class="risk-item" style="padding:5px 10px;font-size:11px;"><strong>无法直观 Review</strong>——聊天界面看不到改动前后对比，确认成本高</div>
          <div class="risk-item" style="padding:5px 10px;font-size:11px;"><strong>配置生效需重启</strong>——改完还需触发重启，对非技术人员不直观</div>
        </div>
        <div class="conclusion-body" style="font-size:12px;margin-top:8px;">
          <strong>当前结论：暂缓，由产品团队通过 VSCode 管理配置后台。</strong>等第二阶段架构稳定、配置项收敛后再评估。
        </div>
      </div>

    </div>

    <!-- 右列：权限体系 -->
    <div style="display:flex;flex-direction:column;gap:10px;min-height:0;">

      <!-- 第一层: 飞书平台权限 -->
      <div class="perm-card" style="flex:1;min-height:0;overflow:hidden;">
        <div class="perm-card-head"><div class="dot"></div>第一层：飞书平台权限（控制 Bot 能调哪些 API）</div>
        <div class="perm-sublabel" style="border-top:none;margin-top:0;padding:4px 20px;">应用级权限（Bot 本身）</div>
        <div class="perm-item" style="padding:5px 16px;"><span class="perm-scope">im:message</span><span class="perm-desc">读取群聊消息，用于日报收集</span></div>
        <div class="perm-item" style="padding:5px 16px;"><span class="perm-scope">contact</span><span class="perm-desc">解析用户姓名</span></div>
        <div class="perm-item" style="padding:5px 16px;"><span class="perm-scope">drive</span><span class="perm-desc">文档列表访问</span></div>
        <div class="perm-sublabel" style="padding:4px 20px;">用户授权（老板本人 OAuth）</div>
        <div class="perm-item" style="padding:5px 16px;"><span class="perm-scope">im:chat</span><span class="perm-desc">获取老板所在群列表（日报）</span></div>
        <div class="perm-item" style="padding:5px 16px;"><span class="perm-scope">wiki</span><span class="perm-desc">解析飞书知识库文档链接</span></div>
        <div class="perm-item" style="padding:5px 16px;"><span class="perm-scope">docx:readonly</span><span class="perm-desc">读取文档正文内容（AI 分析用）</span></div>
        <div class="perm-item" style="padding:5px 16px;"><span class="perm-scope">drive:write</span><span class="perm-desc">以老板身份在文档里写批注</span></div>
        <div class="token-note" style="padding:8px 14px;font-size:11px;">⚠️ 读文档 + 写批注必须用老板本人授权的 token，不能用 Bot 应用的 token——批注在飞书中显示为老板本人发出。</div>
      </div>

      <!-- 第二层: 代码层权限 -->
      <div class="perm-card" style="flex:1;min-height:0;overflow:hidden;">
        <div class="perm-card-head"><div class="dot" style="background:#34C759"></div>第二层：代码层权限（控制谁能用什么功能）</div>
        <table class="role-table">
          <thead><tr><th>角色</th><th>判断方式</th><th>可用功能</th></tr></thead>
          <tbody>
            <tr class="boss-row">
              <td style="padding:7px 10px;"><span class="role-badge badge-boss">Boss</span></td>
              <td style="font-size:12px;color:#6b7a95;padding:7px 10px;">open_id 固定值</td>
              <td style="font-size:12px;padding:7px 10px;">全部功能（含数据蒸馏、Skill 生成）</td>
            </tr>
            <tr>
              <td style="padding:7px 10px;"><span class="role-badge badge-employee">员工</span></td>
              <td style="font-size:12px;color:#6b7a95;padding:7px 10px;">open_id 在白名单中</td>
              <td style="font-size:12px;padding:7px 10px;">文档预审 + 通用对话</td>
            </tr>
            <tr>
              <td style="padding:7px 10px;"><span class="role-badge badge-other">其他人</span></td>
              <td style="font-size:12px;color:#6b7a95;padding:7px 10px;">不在任何列表</td>
              <td style="font-size:12px;color:#4a5568;padding:7px 10px;">静默忽略，不回复不提示</td>
            </tr>
            <tr>
              <td style="padding:7px 10px;"><span class="role-badge badge-admin">Admin</span><span class="badge-deferred">暂缓</span></td>
              <td style="font-size:12px;color:#6b7a95;padding:7px 10px;">ADMIN_OPEN_IDS</td>
              <td style="font-size:12px;color:#4a5568;padding:7px 10px;">管理配置（第二阶段）</td>
            </tr>
          </tbody>
        </table>
        <div style="padding:10px 16px;font-size:11px;color:#6b7a95;border-top:1px solid #1e2530;">
          <strong style="color:#e2e8f0;">回复语境区分</strong><br>
          老板发消息 → AI 收到"对话者是老板本人，直接简短"<br>
          员工发消息 → AI 收到"对话者是员工，上级对下属沟通风格"<br>
          <span style="color:#4a5568;font-size:10px;">同一个 Bot，同一套人格，根据发送者动态调整语境</span>
        </div>
      </div>

    </div>
  </div>
</div>'''

OLD_NAV = '''\
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

NEW_NAV = '''\
    <button class="nav-item active" data-idx="0"><span class="nav-num">01</span>概览</button>
    <button class="nav-item" data-idx="1"><span class="nav-num">02</span>系统架构</button>
    <button class="nav-item" data-idx="2"><span class="nav-num">03</span>Skill 能力</button>
    <button class="nav-item" data-idx="3"><span class="nav-num">04</span>维度对比</button>
    <button class="nav-item" data-idx="4"><span class="nav-num">05</span>Eval 结果</button>
    <button class="nav-item" data-idx="5"><span class="nav-num">06</span>Bot 架构</button>
    <button class="nav-item" data-idx="6"><span class="nav-num">07</span>产品角色</button>
    <button class="nav-item" data-idx="7"><span class="nav-num">08</span>技术选型</button>
    <button class="nav-item" data-idx="8"><span class="nav-num">09</span>框架对比</button>
    <button class="nav-item" data-idx="9"><span class="nav-num">10</span>框架分析</button>
    <button class="nav-item" data-idx="10"><span class="nav-num">11</span>方案评估</button>
    <button class="nav-item" data-idx="11"><span class="nav-num">12</span>进展计划</button>'''


def find_section(text, id_):
    """Return (start_of_div, end_after_closing_div)."""
    marker = f'<div class="section" id="{id_}"'
    start = text.index(marker)
    depth = 0
    i = start
    while i < len(text):
        if text[i:i+4] == '<div':
            depth += 1; i += 4
        elif text[i:i+6] == '</div>':
            depth -= 1; i += 6
            if depth == 0:
                return start, i
        else:
            i += 1
    raise ValueError(f'unclosed section: {id_}')


def process(src):
    shutil.copy(src, src.replace('.html', '-pre-merge-perm-decision.html'))
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()

    # ── Step 1: remove #decision section (+ its comment) ─────────────────────
    dc_start, dc_end = find_section(html, 'decision')
    dc_comment = '<!-- 13. 关键决策 -->\n'
    if dc_comment in html and html.index(dc_comment) < dc_start:
        dc_start = html.index(dc_comment)
    # consume trailing newline
    while dc_end < len(html) and html[dc_end] == '\n':
        dc_end += 1
    html = html[:dc_start] + html[dc_end:]

    # ── Step 2: replace #perm section (+ its comment) with merged section ────
    pm_start, pm_end = find_section(html, 'perm')
    pm_comment = '<!-- 8. 权限体系 -->\n'
    if pm_comment in html and html.index(pm_comment) < pm_start:
        pm_start = html.index(pm_comment)
    html = html[:pm_start] + MERGED_SECTION + '\n\n' + html[pm_end:]

    # ── Step 3: update nav ────────────────────────────────────────────────────
    assert OLD_NAV in html, 'Old nav block not found — check for whitespace differences'
    html = html.replace(OLD_NAV, NEW_NAV)

    with open(src, 'w', encoding='utf-8') as f:
        f.write(html)

    assert 'id="perm"' in html
    assert 'id="decision"' not in html, '#decision should be removed'
    sections = [m.group(1) for m in re.finditer(r'class="section" id="([^"]+)"', html)]
    nav_count = html.count('data-idx=')
    print(f'{src.split("/")[-1]}: {len(html.splitlines())} lines, nav={nav_count}, sections={sections}')


process('/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/index.html')
process('/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/architecture-report.html')
