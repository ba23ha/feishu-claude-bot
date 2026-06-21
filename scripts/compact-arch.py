#!/usr/bin/env python3
"""
Compact page 07 #arch section:
- Three arch nodes: icon inline with label+title (one row), 12px body, no blank lines, padding 12px→saves ~92px
- arch-chain: padding 14px→10px, font 13px→12px, saves ~23px
- Permission cards: unchanged, but now get ~115px more breathing room (no overflow)
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


NEW_ARCH = '''\
<div class="section" id="arch">
  <div class="section-label">架构 & 权限</div>
  <div class="section-title">三端架构 · 双层权限设计</div>

  <!-- 三端架构：icon 内联横排，紧凑版 -->
  <div class="arch-flow" style="margin-bottom:10px;flex-shrink:0;">

    <div style="flex:1;padding:12px 16px;display:flex;flex-direction:column;gap:8px;">
      <div style="display:flex;align-items:center;gap:9px;">
        <span style="font-size:22px;line-height:1;flex-shrink:0;">📱</span>
        <div>
          <span style="font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#4F8EF7;">端 A</span>
          <span style="font-size:14px;font-weight:700;color:#fff;margin-left:8px;">飞书客户端</span>
        </div>
      </div>
      <div style="font-size:11px;color:#6b7a95;line-height:1.55;">使用者：老板、员工白名单<br>载体：飞书 App（手机 / 桌面）</div>
      <div style="font-size:12px;color:#c8d0dc;line-height:1.55;">· 发消息 / 发文档链接<br>· 查看 Bot 批注结果</div>
    </div>

    <div style="flex:1;padding:12px 16px;border-left:1px solid #1e2530;display:flex;flex-direction:column;gap:8px;">
      <div style="display:flex;align-items:center;gap:9px;">
        <span style="font-size:22px;line-height:1;flex-shrink:0;">☁️</span>
        <div>
          <span style="font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#4F8EF7;">端 B</span>
          <span style="font-size:14px;font-weight:700;color:#fff;margin-left:8px;">飞书开放平台</span>
        </div>
      </div>
      <div style="font-size:11px;color:#6b7a95;line-height:1.55;">使用者：系统自动<br>载体：WebSocket 长连接（飞书云端）</div>
      <div style="font-size:12px;color:#c8d0dc;line-height:1.55;">· 把用户消息转发给服务器<br>· 把服务器回复传回给用户</div>
    </div>

    <div style="flex:1;padding:12px 16px;border-left:1px solid #1e2530;display:flex;flex-direction:column;gap:8px;">
      <div style="display:flex;align-items:center;gap:9px;">
        <span style="font-size:22px;line-height:1;flex-shrink:0;">🖥️</span>
        <div>
          <span style="font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#4F8EF7;">端 C</span>
          <span style="font-size:14px;font-weight:700;color:#fff;margin-left:8px;">自建服务器</span>
        </div>
      </div>
      <div style="font-size:11px;color:#6b7a95;line-height:1.55;">使用者：全自动运行，崩溃自动恢复<br>载体：本地 Mac，Node.js</div>
      <div style="font-size:12px;color:#c8d0dc;line-height:1.55;">· 全部业务逻辑<br>· 调用 Claude AI / 飞书 API</div>
    </div>

  </div>

  <!-- 服务链路（紧凑版） -->
  <div class="arch-chain" style="margin-bottom:12px;padding:10px 18px;font-size:12px;flex-shrink:0;">
    <span>用户发消息</span><span class="sep">→</span>
    <span>飞书推 WebSocket 事件</span><span class="sep">→</span>
    <span>服务器权限校验 + 任务路由</span><span class="sep">→</span>
    <span>读文档 + Claude 分析</span><span class="sep">→</span>
    <span>写批注 / 发回复</span><span class="sep">→</span>
    <span>用户看到结果</span>
  </div>

  <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;flex-shrink:0;">
    <div style="flex:1;height:1px;background:#1e2530;"></div>
    <span style="font-size:10px;font-weight:700;color:#6b7a95;letter-spacing:1.5px;text-transform:uppercase;white-space:nowrap;">双层权限体系</span>
    <div style="flex:1;height:1px;background:#1e2530;"></div>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;flex:1;min-height:0;">

    <!-- 第一层: 飞书平台权限 -->
    <div class="perm-card" style="overflow:hidden;">
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
    <div class="perm-card" style="overflow:hidden;">
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
</div>'''


def process(src):
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()

    s, e = find_section(html, 'arch')
    html = html[:s] + NEW_ARCH + html[e:]

    with open(src, 'w', encoding='utf-8') as f:
        f.write(html)

    lines = len(html.splitlines())
    assert 'font-size:22px;line-height:1;flex-shrink:0;">📱' in html, 'inline icon missing'
    assert 'padding:10px 18px;font-size:12px' in html, 'compact chain missing'
    assert 'drive:write' in html, 'perm items missing'
    print(f'{src.split("/")[-1]}: {lines} lines  ✓')


for doc in DOCS:
    process(doc)
