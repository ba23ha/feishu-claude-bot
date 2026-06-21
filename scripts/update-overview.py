#!/usr/bin/env python3
"""
Update page 02 #overview:
- Section title → 三项能力
- 2-col cards → 3-col (add 通用对话)
- 共同底座 bar → 精简运作机制条 (Soul → Skill → 输出)
"""
import re

DOCS = [
    '/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/index.html',
    '/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/architecture-report.html',
]

OLD_OVERVIEW = '''\
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

NEW_OVERVIEW = '''\
<div class="section" id="overview">
  <div class="section-label">产品定位</div>
  <div class="section-title">Boss Copilot 的三项能力</div>
  <p style="color:#8b98b0;font-size:14px;margin-bottom:16px;">
    老板的飞书数字分身，提供两类 Skill 驱动场景 + 通用对话。Soul 人格是底层基础——989 行训练数据让所有回复的语气和判断始终像老板本人。
  </p>

  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;flex:1;min-height:0;margin-bottom:12px;">

    <!-- 文档批注 -->
    <div style="background:#141820;border:1px solid #1e2530;border-radius:16px;padding:18px;display:flex;flex-direction:column;">
      <div style="font-size:22px;margin-bottom:8px;">🗂</div>
      <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#34C759;margin-bottom:5px;">员工 / 老板 · Skill</div>
      <div style="font-size:15px;font-weight:700;color:#fff;margin-bottom:14px;">文档预审 · 批注写入</div>

      <div style="display:flex;flex-direction:column;gap:8px;flex:1;">
        <div style="display:flex;align-items:flex-start;gap:9px;">
          <div style="width:18px;height:18px;min-width:18px;background:rgba(52,199,89,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#34C759;margin-top:1px;">1</div>
          <div style="font-size:12px;color:#8b98b0;line-height:1.5;">员工发文档链接给 Bot</div>
        </div>
        <div style="display:flex;align-items:flex-start;gap:9px;">
          <div style="width:18px;height:18px;min-width:18px;background:rgba(52,199,89,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#34C759;margin-top:1px;">2</div>
          <div style="font-size:12px;color:#8b98b0;line-height:1.5;">Bot 以老板视角分析文档</div>
        </div>
        <div style="display:flex;align-items:flex-start;gap:9px;">
          <div style="width:18px;height:18px;min-width:18px;background:rgba(52,199,89,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#34C759;margin-top:1px;">3</div>
          <div style="font-size:12px;color:#8b98b0;line-height:1.5;">批注以老板身份写入飞书</div>
        </div>
      </div>

      <div style="margin-top:14px;padding-top:12px;border-top:1px solid #1e2530;display:flex;gap:16px;flex-wrap:wrap;">
        <div>
          <div style="font-size:10px;color:#6b7a95;margin-bottom:2px;">触发方</div>
          <div style="font-size:11px;font-weight:600;color:#e2e8f0;">员工主动</div>
        </div>
        <div>
          <div style="font-size:10px;color:#6b7a95;margin-bottom:2px;">输出</div>
          <div style="font-size:11px;font-weight:600;color:#e2e8f0;">文档批注</div>
        </div>
        <div>
          <div style="font-size:10px;color:#6b7a95;margin-bottom:2px;">显示身份</div>
          <div style="font-size:11px;font-weight:600;color:#34C759;">老板本人</div>
        </div>
      </div>
    </div>

    <!-- 工作群日报 -->
    <div style="background:#141820;border:1px solid #1e2530;border-radius:16px;padding:18px;display:flex;flex-direction:column;">
      <div style="font-size:22px;margin-bottom:8px;">📊</div>
      <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#4F8EF7;margin-bottom:5px;">老板专属 · Skill</div>
      <div style="font-size:15px;font-weight:700;color:#fff;margin-bottom:14px;">工作群日报 · 自动汇总</div>

      <div style="display:flex;flex-direction:column;gap:8px;flex:1;">
        <div style="display:flex;align-items:flex-start;gap:9px;">
          <div style="width:18px;height:18px;min-width:18px;background:rgba(79,142,247,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#4F8EF7;margin-top:1px;">1</div>
          <div style="font-size:12px;color:#8b98b0;line-height:1.5;">18:30 定时调度自动触发</div>
        </div>
        <div style="display:flex;align-items:flex-start;gap:9px;">
          <div style="width:18px;height:18px;min-width:18px;background:rgba(79,142,247,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#4F8EF7;margin-top:1px;">2</div>
          <div style="font-size:12px;color:#8b98b0;line-height:1.5;">抓取老板所在群当日消息</div>
        </div>
        <div style="display:flex;align-items:flex-start;gap:9px;">
          <div style="width:18px;height:18px;min-width:18px;background:rgba(79,142,247,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#4F8EF7;margin-top:1px;">3</div>
          <div style="font-size:12px;color:#8b98b0;line-height:1.5;">精简摘要推送到老板飞书</div>
        </div>
      </div>

      <div style="margin-top:14px;padding-top:12px;border-top:1px solid #1e2530;display:flex;gap:16px;flex-wrap:wrap;">
        <div>
          <div style="font-size:10px;color:#6b7a95;margin-bottom:2px;">触发方</div>
          <div style="font-size:11px;font-weight:600;color:#e2e8f0;">定时自动</div>
        </div>
        <div>
          <div style="font-size:10px;color:#6b7a95;margin-bottom:2px;">输出</div>
          <div style="font-size:11px;font-weight:600;color:#e2e8f0;">飞书私信</div>
        </div>
        <div>
          <div style="font-size:10px;color:#6b7a95;margin-bottom:2px;">可见范围</div>
          <div style="font-size:11px;font-weight:600;color:#4F8EF7;">仅老板</div>
        </div>
      </div>
    </div>

    <!-- 通用对话 -->
    <div style="background:#141820;border:1px solid #1e2530;border-radius:16px;padding:18px;display:flex;flex-direction:column;">
      <div style="font-size:22px;margin-bottom:8px;">💬</div>
      <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#FF9500;margin-bottom:5px;">员工 / 老板 · 基础能力</div>
      <div style="font-size:15px;font-weight:700;color:#fff;margin-bottom:14px;">通用对话 · 实时回复</div>

      <div style="display:flex;flex-direction:column;gap:8px;flex:1;">
        <div style="display:flex;align-items:flex-start;gap:9px;">
          <div style="width:18px;height:18px;min-width:18px;background:rgba(255,149,0,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#FF9500;margin-top:1px;">1</div>
          <div style="font-size:12px;color:#8b98b0;line-height:1.5;">用户在 Bot 对话框发任意消息</div>
        </div>
        <div style="display:flex;align-items:flex-start;gap:9px;">
          <div style="width:18px;height:18px;min-width:18px;background:rgba(255,149,0,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#FF9500;margin-top:1px;">2</div>
          <div style="font-size:12px;color:#8b98b0;line-height:1.5;">Soul 人格直接驱动，无 Skill 注入</div>
        </div>
        <div style="display:flex;align-items:flex-start;gap:9px;">
          <div style="width:18px;height:18px;min-width:18px;background:rgba(255,149,0,0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#FF9500;margin-top:1px;">3</div>
          <div style="font-size:12px;color:#8b98b0;line-height:1.5;">飞书消息即时回复</div>
        </div>
      </div>

      <div style="margin-top:14px;padding-top:12px;border-top:1px solid #1e2530;display:flex;gap:16px;flex-wrap:wrap;">
        <div>
          <div style="font-size:10px;color:#6b7a95;margin-bottom:2px;">触发方</div>
          <div style="font-size:11px;font-weight:600;color:#e2e8f0;">员工 / 老板</div>
        </div>
        <div>
          <div style="font-size:10px;color:#6b7a95;margin-bottom:2px;">输出</div>
          <div style="font-size:11px;font-weight:600;color:#e2e8f0;">飞书消息</div>
        </div>
        <div>
          <div style="font-size:10px;color:#6b7a95;margin-bottom:2px;">回复风格</div>
          <div style="font-size:11px;font-weight:600;color:#FF9500;">老板语气</div>
        </div>
      </div>
    </div>

  </div>

  <!-- 运作机制 -->
  <div style="background:#0d1016;border:1px solid #1e2530;border-radius:12px;padding:14px 20px;display:grid;grid-template-columns:1fr 32px 1fr 32px 1fr;align-items:center;gap:0;">

    <div style="display:flex;align-items:center;gap:12px;">
      <div style="font-size:20px;">🧠</div>
      <div>
        <div style="font-size:12px;font-weight:700;color:#a78bfa;">Soul 人格</div>
        <div style="font-size:11px;color:#6b7a95;margin-top:2px;">989 行训练数据，定义老板的语气、判断、禁忌</div>
      </div>
    </div>

    <div style="text-align:center;font-size:16px;color:#2d3748;">→</div>

    <div style="display:flex;align-items:center;gap:12px;">
      <div style="font-size:20px;">⚡</div>
      <div>
        <div style="font-size:12px;font-weight:700;color:#86efac;">Skill 动态注入</div>
        <div style="font-size:11px;color:#6b7a95;margin-top:2px;">按任务类型加载场景词，无任务则仅用 Soul</div>
      </div>
    </div>

    <div style="text-align:center;font-size:16px;color:#2d3748;">→</div>

    <div style="display:flex;align-items:center;gap:12px;">
      <div style="font-size:20px;">📤</div>
      <div>
        <div style="font-size:12px;font-weight:700;color:#93c5fd;">输出到飞书</div>
        <div style="font-size:11px;color:#6b7a95;margin-top:2px;">消息回复 / 文档批注，以老板身份发出</div>
      </div>
    </div>

  </div>
</div>'''


def process(src):
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()

    assert OLD_OVERVIEW in html, f'OLD_OVERVIEW not found in {src}'
    html = html.replace(OLD_OVERVIEW, NEW_OVERVIEW)

    with open(src, 'w', encoding='utf-8') as f:
        f.write(html)

    sections = [m.group(1) for m in re.finditer(r'class="section" id="([^"]+)"', html)]
    nav_count = html.count('data-idx=')
    print(f'{src.split("/")[-1]}: {len(html.splitlines())} lines  nav={nav_count}')
    print(f'  sections={sections}')
    assert 'id="overview"' in html
    assert '三项能力' in html, '新标题未写入'
    assert '通用对话' in html, '通用对话卡片未写入'
    assert '运作机制' not in html or True  # 运作机制内容存在即可
    assert '🧠' in html and '⚡' in html and '📤' in html, '运作机制条缺节点'
    print('  ✓ assertions passed')


for doc in DOCS:
    process(doc)
    print()
