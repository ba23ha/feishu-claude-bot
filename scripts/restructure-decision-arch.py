#!/usr/bin/env python3
"""
Combined restructure:

1. Page 02 (#overview):
   - 3 scenario cards: remove flex-stretch, compact padding
   - Bottom: replace slim 运作机制 strip with full 4-node AI layer (business language)

2. Pages 06/07/08 — Scheme B:
   - perm  → new 06 "产品决策"  : 2 decision cards side-by-side, full page
   - arch  → new 07 "架构 & 权限": 三端架构 + 双层权限 (AI 4-layer removed)
   - agent-arch → new 08 "服务流程": content unchanged, just reordered

3. Nav: 06系统架构→产品决策, 07服务流程→架构&权限, 08产品角色→服务流程
"""
import re

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


# ── PAGE 02: new overview ─────────────────────────────────────────────────────

NEW_OVERVIEW = '''\
<div class="section" id="overview">
  <div class="section-label">产品定位</div>
  <div class="section-title">Boss Copilot 的三项能力</div>
  <p style="color:#8b98b0;font-size:14px;margin-bottom:14px;">
    老板的飞书数字分身，提供两类 Skill 驱动场景 + 通用对话。Soul 人格是底层基础——989 行训练数据让所有回复的语气和判断始终像老板本人。
  </p>

  <!-- 三张场景卡（紧凑，不拉伸） -->
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:12px;">

    <!-- 文档批注 -->
    <div style="background:#141820;border:1px solid #1e2530;border-radius:14px;padding:16px;">
      <div style="font-size:22px;margin-bottom:7px;">🗂</div>
      <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#34C759;margin-bottom:4px;">员工 / 老板 · Skill</div>
      <div style="font-size:14px;font-weight:700;color:#fff;margin-bottom:12px;">文档预审 · 批注写入</div>
      <div style="display:flex;flex-direction:column;gap:7px;margin-bottom:12px;">
        <div style="display:flex;align-items:flex-start;gap:8px;"><div style="width:17px;height:17px;min-width:17px;background:rgba(52,199,89,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#34C759;margin-top:1px;">1</div><div style="font-size:12px;color:#8b98b0;line-height:1.5;">员工发文档链接给 Bot</div></div>
        <div style="display:flex;align-items:flex-start;gap:8px;"><div style="width:17px;height:17px;min-width:17px;background:rgba(52,199,89,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#34C759;margin-top:1px;">2</div><div style="font-size:12px;color:#8b98b0;line-height:1.5;">Bot 以老板视角分析文档</div></div>
        <div style="display:flex;align-items:flex-start;gap:8px;"><div style="width:17px;height:17px;min-width:17px;background:rgba(52,199,89,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#34C759;margin-top:1px;">3</div><div style="font-size:12px;color:#8b98b0;line-height:1.5;">批注以老板身份写入飞书</div></div>
      </div>
      <div style="padding-top:10px;border-top:1px solid #1e2530;display:flex;gap:14px;flex-wrap:wrap;">
        <div><div style="font-size:10px;color:#6b7a95;margin-bottom:2px;">触发方</div><div style="font-size:11px;font-weight:600;color:#e2e8f0;">员工主动</div></div>
        <div><div style="font-size:10px;color:#6b7a95;margin-bottom:2px;">输出</div><div style="font-size:11px;font-weight:600;color:#e2e8f0;">文档批注</div></div>
        <div><div style="font-size:10px;color:#6b7a95;margin-bottom:2px;">显示身份</div><div style="font-size:11px;font-weight:600;color:#34C759;">老板本人</div></div>
      </div>
    </div>

    <!-- 工作群日报 -->
    <div style="background:#141820;border:1px solid #1e2530;border-radius:14px;padding:16px;">
      <div style="font-size:22px;margin-bottom:7px;">📊</div>
      <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#4F8EF7;margin-bottom:4px;">老板专属 · Skill</div>
      <div style="font-size:14px;font-weight:700;color:#fff;margin-bottom:12px;">工作群日报 · 自动汇总</div>
      <div style="display:flex;flex-direction:column;gap:7px;margin-bottom:12px;">
        <div style="display:flex;align-items:flex-start;gap:8px;"><div style="width:17px;height:17px;min-width:17px;background:rgba(79,142,247,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#4F8EF7;margin-top:1px;">1</div><div style="font-size:12px;color:#8b98b0;line-height:1.5;">18:30 定时调度自动触发</div></div>
        <div style="display:flex;align-items:flex-start;gap:8px;"><div style="width:17px;height:17px;min-width:17px;background:rgba(79,142,247,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#4F8EF7;margin-top:1px;">2</div><div style="font-size:12px;color:#8b98b0;line-height:1.5;">抓取老板所在群当日消息</div></div>
        <div style="display:flex;align-items:flex-start;gap:8px;"><div style="width:17px;height:17px;min-width:17px;background:rgba(79,142,247,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#4F8EF7;margin-top:1px;">3</div><div style="font-size:12px;color:#8b98b0;line-height:1.5;">精简摘要推送到老板飞书</div></div>
      </div>
      <div style="padding-top:10px;border-top:1px solid #1e2530;display:flex;gap:14px;flex-wrap:wrap;">
        <div><div style="font-size:10px;color:#6b7a95;margin-bottom:2px;">触发方</div><div style="font-size:11px;font-weight:600;color:#e2e8f0;">定时自动</div></div>
        <div><div style="font-size:10px;color:#6b7a95;margin-bottom:2px;">输出</div><div style="font-size:11px;font-weight:600;color:#e2e8f0;">飞书私信</div></div>
        <div><div style="font-size:10px;color:#6b7a95;margin-bottom:2px;">可见范围</div><div style="font-size:11px;font-weight:600;color:#4F8EF7;">仅老板</div></div>
      </div>
    </div>

    <!-- 通用对话 -->
    <div style="background:#141820;border:1px solid #1e2530;border-radius:14px;padding:16px;">
      <div style="font-size:22px;margin-bottom:7px;">💬</div>
      <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#FF9500;margin-bottom:4px;">员工 / 老板 · 基础能力</div>
      <div style="font-size:14px;font-weight:700;color:#fff;margin-bottom:12px;">通用对话 · 实时回复</div>
      <div style="display:flex;flex-direction:column;gap:7px;margin-bottom:12px;">
        <div style="display:flex;align-items:flex-start;gap:8px;"><div style="width:17px;height:17px;min-width:17px;background:rgba(255,149,0,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#FF9500;margin-top:1px;">1</div><div style="font-size:12px;color:#8b98b0;line-height:1.5;">用户在 Bot 对话框发任意消息</div></div>
        <div style="display:flex;align-items:flex-start;gap:8px;"><div style="width:17px;height:17px;min-width:17px;background:rgba(255,149,0,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#FF9500;margin-top:1px;">2</div><div style="font-size:12px;color:#8b98b0;line-height:1.5;">Soul 人格直接驱动，无 Skill 注入</div></div>
        <div style="display:flex;align-items:flex-start;gap:8px;"><div style="width:17px;height:17px;min-width:17px;background:rgba(255,149,0,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#FF9500;margin-top:1px;">3</div><div style="font-size:12px;color:#8b98b0;line-height:1.5;">飞书消息即时回复</div></div>
      </div>
      <div style="padding-top:10px;border-top:1px solid #1e2530;display:flex;gap:14px;flex-wrap:wrap;">
        <div><div style="font-size:10px;color:#6b7a95;margin-bottom:2px;">触发方</div><div style="font-size:11px;font-weight:600;color:#e2e8f0;">员工 / 老板</div></div>
        <div><div style="font-size:10px;color:#6b7a95;margin-bottom:2px;">输出</div><div style="font-size:11px;font-weight:600;color:#e2e8f0;">飞书消息</div></div>
        <div><div style="font-size:10px;color:#6b7a95;margin-bottom:2px;">回复风格</div><div style="font-size:11px;font-weight:600;color:#FF9500;">老板语气</div></div>
      </div>
    </div>

  </div>

  <!-- AI 4层机制（业务语言，填满剩余高度） -->
  <div style="flex:1;min-height:0;display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:10px;">

    <div style="background:#141820;border:1px solid rgba(139,92,246,0.3);border-radius:12px;padding:16px 18px;display:flex;flex-direction:column;">
      <div style="font-size:22px;margin-bottom:8px;">🧠</div>
      <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#a78bfa;margin-bottom:5px;">① 人格底座</div>
      <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:8px;">Soul + 业务记忆</div>
      <div style="font-size:12px;color:#8b98b0;line-height:1.6;flex:1;">989 行 Soul 训练数据定义老板的语气、决策标准与禁忌词；3 个业务记忆文件存储人名、项目与专有词汇。所有回复的"底色"。</div>
    </div>

    <div style="background:#141820;border:1px solid rgba(139,92,246,0.18);border-radius:12px;padding:16px 18px;display:flex;flex-direction:column;">
      <div style="font-size:22px;margin-bottom:8px;">⚙️</div>
      <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#c4b5fd;margin-bottom:5px;">② 实时组装</div>
      <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:8px;">每次请求独立拼装</div>
      <div style="font-size:12px;color:#8b98b0;line-height:1.6;flex:1;">5 个 Soul 文件 + 3 个记忆文件在每次请求时读取合并，生成约 15K 字系统指令。配置改动无需重启即可生效。</div>
    </div>

    <div style="background:#141820;border:1px solid rgba(52,199,89,0.22);border-radius:12px;padding:16px 18px;display:flex;flex-direction:column;">
      <div style="font-size:22px;margin-bottom:8px;">⚡</div>
      <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#86efac;margin-bottom:5px;">③ 技能注入</div>
      <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:8px;">按场景动态加载 Skill</div>
      <div style="font-size:12px;color:#8b98b0;line-height:1.6;flex:1;">文档批注 → review_inline；日报 → daily_report；通用对话 → 不额外注入，仅靠人格底座驱动。同一套人格，不同任务精度。</div>
    </div>

    <div style="background:#141820;border:1px solid rgba(79,142,247,0.22);border-radius:12px;padding:16px 18px;display:flex;flex-direction:column;">
      <div style="font-size:22px;margin-bottom:8px;">📤</div>
      <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#93c5fd;margin-bottom:5px;">④ 飞书输出</div>
      <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:8px;">以老板身份交付结果</div>
      <div style="font-size:12px;color:#8b98b0;line-height:1.6;flex:1;">消息回复、文档批注（OAuth token 以老板本人身份写入），每次调用同步生成 JSONL 审计记录。</div>
    </div>

  </div>
</div>'''

# ── PAGE 06: 产品决策 (replaces old perm) ────────────────────────────────────

NEW_DECISION = '''\
<div class="section" id="perm">
  <div class="section-label">产品决策</div>
  <div class="section-title">两项核心设计判断</div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;flex:1;min-height:0;">

    <!-- 决策A: Bot定位 -->
    <div class="conclusion-card" style="padding:20px 22px;">
      <div class="conclusion-tag">架构决策</div>
      <div class="conclusion-icon" style="font-size:24px;margin-bottom:10px;">🤖</div>
      <div class="conclusion-title" style="font-size:16px;">无需区分多个 Bot，定位统一为老板代理人</div>
      <div class="conclusion-body">
        老板和员工使用的是<strong>同一个 Bot</strong>，回复口吻始终模拟老板本人说话——员工发文档，批注显示为老板写的；员工问问题，回复是老板风格的答复。这与"数字分身"定位完全一致。<br><br>
        拆成多个 Bot（老板专用 / 员工专用）的唯一好处是功能隔离，但当前员工侧功能本来就少，隔离价值低，两套 App ID + 两个 OAuth + 两个 WebSocket 连接的运维成本远大于收益。<br><br>
        <strong>功能层面的权限隔离已在代码层完成</strong>，无需靠拆 Bot 实现。
      </div>
    </div>

    <!-- 决策B: 配置管理暂缓 -->
    <div class="conclusion-card" style="padding:20px 22px;">
      <div class="conclusion-tag orange">风险提示</div>
      <div class="conclusion-icon" style="font-size:24px;margin-bottom:10px;">⚠️</div>
      <div class="conclusion-title" style="font-size:16px;">管理员 / 员工自主配置 Agent 的业务实现难点</div>
      <div class="conclusion-body">
        由非技术人员通过自然语言管理 Agent 配置，在业务层面面临以下核心风险：
      </div>
      <div class="risk-list">
        <div class="risk-item"><strong>意图歧义</strong>——"把 review 风格改简洁一点"，AI 无法确定改哪里、改多少，容易误改关键规则</div>
        <div class="risk-item"><strong>富文本修改风险</strong>——Soul / Skill 是 Markdown，通过聊天编辑等于让 AI 代写代码，一次误操作影响所有用户</div>
        <div class="risk-item"><strong>无法直观 Review</strong>——聊天界面看不到改动前后对比，确认成本高</div>
        <div class="risk-item"><strong>配置生效需重启</strong>——改完还需触发重启，对非技术人员不直观</div>
      </div>
      <div class="conclusion-body" style="margin-top:12px;">
        <strong>当前结论：暂缓，由产品团队通过 VSCode 管理配置后台。</strong>等第二阶段架构稳定、配置项收敛后再评估。
      </div>
    </div>

  </div>
</div>'''

# ── PAGE 07: 架构 & 权限 (replaces old arch, removes AI 4-layer) ─────────────

NEW_ARCH_PERM = '''\
<div class="section" id="arch">
  <div class="section-label">架构 & 权限</div>
  <div class="section-title">三端架构 · 双层权限设计</div>

  <div class="arch-flow" style="margin-bottom:10px;">
    <div class="arch-node">
      <div class="arch-node-icon">📱</div>
      <div class="arch-node-label">端 A</div>
      <div class="arch-node-title">飞书客户端</div>
      <div class="arch-node-body">使用者：老板、员工白名单<br>载体：飞书 App（手机 / 桌面）<br><br>· 发消息 / 发文档链接<br>· 查看 Bot 批注结果</div>
    </div>
    <div class="arch-node">
      <div class="arch-node-icon">☁️</div>
      <div class="arch-node-label">端 B</div>
      <div class="arch-node-title">飞书开放平台</div>
      <div class="arch-node-body">使用者：系统自动<br>载体：WebSocket 长连接（飞书云端）<br><br>· 把用户消息转发给服务器<br>· 把服务器回复传回给用户</div>
    </div>
    <div class="arch-node">
      <div class="arch-node-icon">🖥️</div>
      <div class="arch-node-label">端 C</div>
      <div class="arch-node-title">自建服务器</div>
      <div class="arch-node-body">使用者：全自动运行，崩溃自动恢复<br>载体：本地 Mac，Node.js<br><br>· 全部业务逻辑<br>· 调用 Claude AI / 飞书 API</div>
    </div>
  </div>

  <div class="arch-chain" style="margin-bottom:14px;">
    <span>用户发消息</span><span class="sep">→</span>
    <span>飞书推 WebSocket 事件</span><span class="sep">→</span>
    <span>服务器权限校验 + 任务路由</span><span class="sep">→</span>
    <span>读文档 + Claude 分析</span><span class="sep">→</span>
    <span>写批注 / 发回复</span><span class="sep">→</span>
    <span>用户看到结果</span>
  </div>

  <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
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

# ── NAV ───────────────────────────────────────────────────────────────────────

OLD_NAV = '''\
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

NEW_NAV = '''\
    <button class="nav-item active" data-idx="0"><span class="nav-num">01</span>概览</button>
    <button class="nav-item" data-idx="1"><span class="nav-num">02</span>产品全景</button>
    <button class="nav-item" data-idx="2"><span class="nav-num">03</span>Skill 能力</button>
    <button class="nav-item" data-idx="3"><span class="nav-num">04</span>日报测试</button>
    <button class="nav-item" data-idx="4"><span class="nav-num">05</span>批注测试</button>
    <button class="nav-item" data-idx="5"><span class="nav-num">06</span>产品决策</button>
    <button class="nav-item" data-idx="6"><span class="nav-num">07</span>架构 & 权限</button>
    <button class="nav-item" data-idx="7"><span class="nav-num">08</span>服务流程</button>
    <button class="nav-item" data-idx="8"><span class="nav-num">09</span>技术选型</button>
    <button class="nav-item" data-idx="9"><span class="nav-num">10</span>框架对比</button>
    <button class="nav-item" data-idx="10"><span class="nav-num">11</span>差距与局限</button>
    <button class="nav-item" data-idx="11"><span class="nav-num">12</span>进展计划</button>'''

# ── SECTION ORDER ─────────────────────────────────────────────────────────────

SECTION_IDS = ['overview', 'skills', 'skilleval-dr', 'skilleval-lr',
               'arch', 'agent-arch', 'perm',
               'tech-compare', 'framework-compare', 'framework-gap', 'status']

NEW_ORDER = ['overview', 'skills', 'skilleval-dr', 'skilleval-lr',
             'perm', 'arch', 'agent-arch',
             'tech-compare', 'framework-compare', 'framework-gap', 'status']


def process(src):
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()

    positions = {id_: find_section(html, id_) for id_ in SECTION_IDS}
    raw = {id_: html[s:e] for id_, (s, e) in positions.items()}

    preamble  = html[:min(s for s, _ in positions.values())]
    postamble = html[max(e for _, e in positions.values()):]

    modified = dict(raw)
    modified['overview'] = NEW_OVERVIEW
    modified['perm']     = NEW_DECISION
    modified['arch']     = NEW_ARCH_PERM
    # agent-arch: raw content unchanged

    body = '\n\n'.join(modified[id_] for id_ in NEW_ORDER)
    html = preamble + body + postamble

    assert OLD_NAV in html, 'OLD_NAV not found'
    html = html.replace(OLD_NAV, NEW_NAV)

    with open(src, 'w', encoding='utf-8') as f:
        f.write(html)

    sections = [m.group(1) for m in re.finditer(r'class="section" id="([^"]+)"', html)]
    nav_count = html.count('data-idx=')
    print(f'{src.split("/")[-1]}: {len(html.splitlines())} lines  nav={nav_count}')
    print(f'  sections={sections}')

    assert nav_count == 12, f'expected 12 nav, got {nav_count}'
    assert sections[4] == 'perm',       f'pos4 should be perm, got {sections[4]}'
    assert sections[5] == 'arch',       f'pos5 should be arch, got {sections[5]}'
    assert sections[6] == 'agent-arch', f'pos6 should be agent-arch, got {sections[6]}'
    assert '两项核心设计判断' in html,      '产品决策 title missing'
    assert '三端架构 · 双层权限设计' in html, '架构权限 title missing'
    assert '人格底座' in html,             'AI layer box 1 missing'
    assert '实时组装' in html,             'AI layer box 2 missing'
    assert '技能注入' in html,             'AI layer box 3 missing'
    assert '飞书输出' in html,             'AI layer box 4 missing'
    assert 'AI 层 — Agent 分层结构' not in html, 'old AI layer should be removed from arch'
    print('  ✓ all assertions passed')


for doc in DOCS:
    process(doc)
    print()
