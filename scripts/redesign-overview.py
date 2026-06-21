#!/usr/bin/env python3
"""
Redesign page 02 #overview:
- Layout: grid-template-rows:2fr 36px 1fr so cards always get 2/3, AI boxes 1/3
- Cards: 3px colored top border, larger emoji, value line, brighter step text, footer margin-top:auto
- AI boxes: icon+label+title side-by-side, horizontal arrows, proportional height
- Divider row: "以上能力由以下 AI 机制共同驱动"
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


NEW_OVERVIEW = '''\
<div class="section" id="overview">
  <div class="section-label">产品定位</div>
  <div class="section-title">Boss Copilot 的三项能力</div>
  <p style="color:#8b98b0;font-size:14px;margin-bottom:14px;">
    老板的飞书数字分身——Soul 人格底座 + Skill 场景扩展，让 AI 始终以老板身份处理两类信息工作并随时响应对话。
  </p>

  <!-- 整体比例容器：卡片2份 / 分隔线固定 / 机制盒1份 -->
  <div style="flex:1;min-height:0;display:grid;grid-template-rows:2fr 36px 1fr;gap:0;">

    <!-- ① 三张能力卡 -->
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;min-height:0;">

      <!-- 文档批注 -->
      <div style="background:#141820;border:1px solid #1e2530;border-radius:14px;overflow:hidden;display:flex;flex-direction:column;min-height:0;">
        <div style="height:3px;background:#34C759;flex-shrink:0;"></div>
        <div style="padding:18px 20px 16px;flex:1;display:flex;flex-direction:column;min-height:0;">
          <div style="font-size:30px;margin-bottom:10px;flex-shrink:0;">🗂</div>
          <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#34C759;margin-bottom:5px;flex-shrink:0;">员工 / 老板 · Skill</div>
          <div style="font-size:16px;font-weight:700;color:#fff;margin-bottom:4px;flex-shrink:0;">文档预审 · 批注写入</div>
          <div style="font-size:12px;color:#6b7a95;margin-bottom:0;flex-shrink:0;">员工按需触发，批注以老板身份直接写入飞书</div>
          <div style="display:flex;flex-direction:column;gap:10px;flex:1;justify-content:center;">
            <div style="display:flex;align-items:center;gap:10px;">
              <div style="width:22px;height:22px;min-width:22px;background:rgba(52,199,89,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#34C759;">1</div>
              <div style="font-size:13px;color:#c8d0dc;font-weight:500;">员工发文档链接给 Bot</div>
            </div>
            <div style="display:flex;align-items:center;gap:10px;">
              <div style="width:22px;height:22px;min-width:22px;background:rgba(52,199,89,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#34C759;">2</div>
              <div style="font-size:13px;color:#c8d0dc;font-weight:500;">Bot 以老板视角分析文档内容</div>
            </div>
            <div style="display:flex;align-items:center;gap:10px;">
              <div style="width:22px;height:22px;min-width:22px;background:rgba(52,199,89,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#34C759;">3</div>
              <div style="font-size:13px;color:#c8d0dc;font-weight:500;">批注以老板身份写入飞书文档</div>
            </div>
          </div>
          <div style="padding-top:12px;margin-top:auto;border-top:1px solid #1e2530;display:flex;gap:20px;flex-shrink:0;">
            <div><div style="font-size:10px;color:#6b7a95;margin-bottom:3px;">触发方</div><div style="font-size:12px;font-weight:600;color:#e2e8f0;">员工主动</div></div>
            <div><div style="font-size:10px;color:#6b7a95;margin-bottom:3px;">输出形式</div><div style="font-size:12px;font-weight:600;color:#e2e8f0;">飞书文档批注</div></div>
            <div><div style="font-size:10px;color:#6b7a95;margin-bottom:3px;">显示身份</div><div style="font-size:12px;font-weight:600;color:#34C759;">老板本人</div></div>
          </div>
        </div>
      </div>

      <!-- 工作群日报 -->
      <div style="background:#141820;border:1px solid #1e2530;border-radius:14px;overflow:hidden;display:flex;flex-direction:column;min-height:0;">
        <div style="height:3px;background:#4F8EF7;flex-shrink:0;"></div>
        <div style="padding:18px 20px 16px;flex:1;display:flex;flex-direction:column;min-height:0;">
          <div style="font-size:30px;margin-bottom:10px;flex-shrink:0;">📊</div>
          <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#4F8EF7;margin-bottom:5px;flex-shrink:0;">老板专属 · Skill</div>
          <div style="font-size:16px;font-weight:700;color:#fff;margin-bottom:4px;flex-shrink:0;">工作群日报 · 自动汇总</div>
          <div style="font-size:12px;color:#6b7a95;margin-bottom:0;flex-shrink:0;">无需老板操作，定时推送全天工作群消息摘要</div>
          <div style="display:flex;flex-direction:column;gap:10px;flex:1;justify-content:center;">
            <div style="display:flex;align-items:center;gap:10px;">
              <div style="width:22px;height:22px;min-width:22px;background:rgba(79,142,247,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#4F8EF7;">1</div>
              <div style="font-size:13px;color:#c8d0dc;font-weight:500;">18:30 定时调度自动触发</div>
            </div>
            <div style="display:flex;align-items:center;gap:10px;">
              <div style="width:22px;height:22px;min-width:22px;background:rgba(79,142,247,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#4F8EF7;">2</div>
              <div style="font-size:13px;color:#c8d0dc;font-weight:500;">抓取老板所在群当日消息</div>
            </div>
            <div style="display:flex;align-items:center;gap:10px;">
              <div style="width:22px;height:22px;min-width:22px;background:rgba(79,142,247,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#4F8EF7;">3</div>
              <div style="font-size:13px;color:#c8d0dc;font-weight:500;">精简摘要推送到老板飞书</div>
            </div>
          </div>
          <div style="padding-top:12px;margin-top:auto;border-top:1px solid #1e2530;display:flex;gap:20px;flex-shrink:0;">
            <div><div style="font-size:10px;color:#6b7a95;margin-bottom:3px;">触发方</div><div style="font-size:12px;font-weight:600;color:#e2e8f0;">定时自动</div></div>
            <div><div style="font-size:10px;color:#6b7a95;margin-bottom:3px;">输出形式</div><div style="font-size:12px;font-weight:600;color:#e2e8f0;">飞书私信</div></div>
            <div><div style="font-size:10px;color:#6b7a95;margin-bottom:3px;">可见范围</div><div style="font-size:12px;font-weight:600;color:#4F8EF7;">仅老板</div></div>
          </div>
        </div>
      </div>

      <!-- 通用对话 -->
      <div style="background:#141820;border:1px solid #1e2530;border-radius:14px;overflow:hidden;display:flex;flex-direction:column;min-height:0;">
        <div style="height:3px;background:#FF9500;flex-shrink:0;"></div>
        <div style="padding:18px 20px 16px;flex:1;display:flex;flex-direction:column;min-height:0;">
          <div style="font-size:30px;margin-bottom:10px;flex-shrink:0;">💬</div>
          <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#FF9500;margin-bottom:5px;flex-shrink:0;">员工 / 老板 · 基础能力</div>
          <div style="font-size:16px;font-weight:700;color:#fff;margin-bottom:4px;flex-shrink:0;">通用对话 · 实时回复</div>
          <div style="font-size:12px;color:#6b7a95;margin-bottom:0;flex-shrink:0;">任意消息即时响应，以老板语气和思维方式回复</div>
          <div style="display:flex;flex-direction:column;gap:10px;flex:1;justify-content:center;">
            <div style="display:flex;align-items:center;gap:10px;">
              <div style="width:22px;height:22px;min-width:22px;background:rgba(255,149,0,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#FF9500;">1</div>
              <div style="font-size:13px;color:#c8d0dc;font-weight:500;">用户在 Bot 对话框发任意消息</div>
            </div>
            <div style="display:flex;align-items:center;gap:10px;">
              <div style="width:22px;height:22px;min-width:22px;background:rgba(255,149,0,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#FF9500;">2</div>
              <div style="font-size:13px;color:#c8d0dc;font-weight:500;">Soul 人格直接驱动，无 Skill 注入</div>
            </div>
            <div style="display:flex;align-items:center;gap:10px;">
              <div style="width:22px;height:22px;min-width:22px;background:rgba(255,149,0,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#FF9500;">3</div>
              <div style="font-size:13px;color:#c8d0dc;font-weight:500;">飞书消息即时回复</div>
            </div>
          </div>
          <div style="padding-top:12px;margin-top:auto;border-top:1px solid #1e2530;display:flex;gap:20px;flex-shrink:0;">
            <div><div style="font-size:10px;color:#6b7a95;margin-bottom:3px;">触发方</div><div style="font-size:12px;font-weight:600;color:#e2e8f0;">员工 / 老板</div></div>
            <div><div style="font-size:10px;color:#6b7a95;margin-bottom:3px;">输出形式</div><div style="font-size:12px;font-weight:600;color:#e2e8f0;">飞书消息</div></div>
            <div><div style="font-size:10px;color:#6b7a95;margin-bottom:3px;">回复风格</div><div style="font-size:12px;font-weight:600;color:#FF9500;">老板语气</div></div>
          </div>
        </div>
      </div>

    </div>

    <!-- ② 分隔行 -->
    <div style="display:flex;align-items:center;gap:14px;padding:0 2px;">
      <div style="flex:1;height:1px;background:#1e2530;"></div>
      <span style="font-size:11px;font-weight:600;color:#4a5568;letter-spacing:0.5px;white-space:nowrap;">以上能力由以下 AI 机制共同驱动</span>
      <div style="flex:1;height:1px;background:#1e2530;"></div>
    </div>

    <!-- ③ AI 4层机制（带箭头，比例高度） -->
    <div style="display:grid;grid-template-columns:1fr 32px 1fr 32px 1fr 32px 1fr;gap:0;min-height:0;">

      <div style="background:#141820;border:1px solid rgba(139,92,246,0.3);border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;min-height:0;overflow:hidden;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;flex-shrink:0;">
          <div style="font-size:26px;">🧠</div>
          <div>
            <div style="font-size:10px;font-weight:700;color:#a78bfa;letter-spacing:1px;text-transform:uppercase;margin-bottom:2px;">① 人格底座</div>
            <div style="font-size:13px;font-weight:700;color:#e2e8f0;">Soul + 业务记忆</div>
          </div>
        </div>
        <div style="font-size:11px;color:#8b98b0;line-height:1.6;flex:1;">989 行 Soul 训练数据定义老板的语气、决策标准与禁忌；3 个业务记忆文件存储人名、项目与专有词汇</div>
      </div>

      <div style="display:flex;align-items:center;justify-content:center;color:#2d3748;font-size:20px;flex-shrink:0;">→</div>

      <div style="background:#141820;border:1px solid rgba(139,92,246,0.18);border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;min-height:0;overflow:hidden;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;flex-shrink:0;">
          <div style="font-size:26px;">⚙️</div>
          <div>
            <div style="font-size:10px;font-weight:700;color:#c4b5fd;letter-spacing:1px;text-transform:uppercase;margin-bottom:2px;">② 实时组装</div>
            <div style="font-size:13px;font-weight:700;color:#e2e8f0;">每次请求独立拼装</div>
          </div>
        </div>
        <div style="font-size:11px;color:#8b98b0;line-height:1.6;flex:1;">5 Soul + 3 记忆文件拼成约 15K 字系统指令，每次请求实时读取，配置改动无需重启即生效</div>
      </div>

      <div style="display:flex;align-items:center;justify-content:center;color:#2d3748;font-size:20px;flex-shrink:0;">→</div>

      <div style="background:#141820;border:1px solid rgba(52,199,89,0.22);border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;min-height:0;overflow:hidden;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;flex-shrink:0;">
          <div style="font-size:26px;">⚡</div>
          <div>
            <div style="font-size:10px;font-weight:700;color:#86efac;letter-spacing:1px;text-transform:uppercase;margin-bottom:2px;">③ 技能注入</div>
            <div style="font-size:13px;font-weight:700;color:#e2e8f0;">按场景动态加载 Skill</div>
          </div>
        </div>
        <div style="font-size:11px;color:#8b98b0;line-height:1.6;flex:1;">批注→review_inline；日报→daily_report；通用对话不额外注入，仅靠人格底座驱动</div>
      </div>

      <div style="display:flex;align-items:center;justify-content:center;color:#2d3748;font-size:20px;flex-shrink:0;">→</div>

      <div style="background:#141820;border:1px solid rgba(79,142,247,0.22);border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;min-height:0;overflow:hidden;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;flex-shrink:0;">
          <div style="font-size:26px;">📤</div>
          <div>
            <div style="font-size:10px;font-weight:700;color:#93c5fd;letter-spacing:1px;text-transform:uppercase;margin-bottom:2px;">④ 飞书输出</div>
            <div style="font-size:13px;font-weight:700;color:#e2e8f0;">以老板身份交付结果</div>
          </div>
        </div>
        <div style="font-size:11px;color:#8b98b0;line-height:1.6;flex:1;">消息回复 / 文档批注（OAuth token 以老板身份写入）+ 每次调用同步生成 JSONL 审计记录</div>
      </div>

    </div>

  </div>
</div>'''


def process(src):
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()

    s, e = find_section(html, 'overview')
    html = html[:s] + NEW_OVERVIEW + html[e:]

    with open(src, 'w', encoding='utf-8') as f:
        f.write(html)

    sections = [m.group(1) for m in re.finditer(r'class="section" id="([^"]+)"', html)]
    nav_count = html.count('data-idx=')
    print(f'{src.split("/")[-1]}: {len(html.splitlines())} lines  nav={nav_count}')
    print(f'  sections={sections}')
    assert '2fr 36px 1fr' in html, 'grid ratio missing'
    assert '3px colored top border' not in html
    assert 'height:3px;background:#34C759' in html, 'green top border missing'
    assert 'margin-top:auto' in html, 'footer pin missing'
    assert '以上能力由以下 AI 机制共同驱动' in html, 'divider text missing'
    print('  ✓ assertions passed')


for doc in DOCS:
    process(doc)
    print()
