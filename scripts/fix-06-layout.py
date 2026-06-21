#!/usr/bin/env python3
"""
Page 06 (agent-arch) two fixes:
1. Soul tags: gap 4→3, padding 7→5 so 'taboos' fits on first row
2. Flow: replace vertical branches with horizontal row layout,
   restore flow-desc and legend, compact overall height
"""
import shutil, re

NEW_FLOW_WRAP = '''\
<div class="flow-wrap" style="padding:10px 16px;">

    <!-- 主流程 ①②③④ -->
    <div class="flow-row" style="margin-bottom:8px;">
      <div class="flow-col">
        <div class="flow-node highlight" style="font-size:12px;padding:6px 12px;">① 接收 WebSocket 事件</div>
        <div class="flow-desc">飞书 SDK 长连接监听</div>
      </div>
      <div class="flow-arrow-h">→</div>
      <div class="flow-col">
        <div class="flow-node" style="font-size:12px;padding:6px 12px;">② 消息去重</div>
        <div class="flow-desc">同一消息 ID 只处理一次</div>
      </div>
      <div class="flow-arrow-h">→</div>
      <div class="flow-col">
        <div class="flow-node" style="font-size:12px;padding:6px 12px;">③ 权限校验</div>
        <div class="flow-desc">白名单检查，非授权丢弃</div>
      </div>
      <div class="flow-arrow-h">→</div>
      <div class="flow-col">
        <div class="flow-node" style="font-size:12px;padding:6px 12px;">④ 任务类型识别</div>
        <div class="flow-desc">正则匹配意图</div>
      </div>
    </div>

    <div style="text-align:center;color:#2d3748;font-size:13px;line-height:1;margin-bottom:6px;">↓</div>

    <!-- 三条分支 · 横向排布 -->
    <div style="display:flex;flex-direction:column;gap:6px;margin-bottom:6px;">

      <!-- 文档预审 -->
      <div style="display:flex;align-items:center;gap:8px;padding:7px 12px;background:rgba(79,142,247,0.04);border:1px solid rgba(79,142,247,0.18);border-radius:8px;">
        <span style="font-size:9px;font-weight:700;color:#4F8EF7;white-space:nowrap;min-width:44px;letter-spacing:0.3px;text-transform:uppercase;">文档预审</span>
        <div class="flow-col">
          <div class="flow-node highlight" style="font-size:11px;padding:5px 10px;min-width:0;">⑤ 读取飞书文档</div>
          <div class="flow-desc">老板 OAuth token</div>
        </div>
        <div class="flow-arrow-h" style="font-size:13px;">→</div>
        <div class="flow-col">
          <div class="flow-node highlight" style="font-size:11px;padding:5px 10px;min-width:0;">⑥ 调用 Claude AI</div>
          <div class="flow-desc">注入 Soul + Skill，重试3次</div>
        </div>
        <div class="flow-arrow-h" style="font-size:13px;">→</div>
        <div class="flow-col">
          <div class="flow-node highlight" style="font-size:11px;padding:5px 10px;min-width:0;">⑦ 写入飞书批注</div>
          <div class="flow-desc">以老板身份逐条写入</div>
        </div>
      </div>

      <!-- 通用对话 -->
      <div style="display:flex;align-items:center;gap:8px;padding:7px 12px;background:rgba(52,199,89,0.03);border:1px solid rgba(52,199,89,0.15);border-radius:8px;">
        <span style="font-size:9px;font-weight:700;color:#34C759;white-space:nowrap;min-width:44px;letter-spacing:0.3px;text-transform:uppercase;">通用对话</span>
        <div class="flow-col">
          <div class="flow-node green" style="font-size:11px;padding:5px 10px;min-width:0;">⑧ Soul + Memory 注入</div>
          <div class="flow-desc">989行人格 + 467行记忆</div>
        </div>
        <div class="flow-arrow-h" style="font-size:13px;">→</div>
        <div class="flow-col">
          <div class="flow-node green" style="font-size:11px;padding:5px 10px;min-width:0;">⑨ 调用 Claude AI</div>
          <div class="flow-desc">基于老板语境生成回复</div>
        </div>
      </div>

      <!-- 日报 -->
      <div style="display:flex;align-items:center;gap:8px;padding:7px 12px;background:rgba(255,149,0,0.03);border:1px solid rgba(255,149,0,0.15);border-radius:8px;">
        <span style="font-size:9px;font-weight:700;color:#FF9500;white-space:nowrap;min-width:44px;letter-spacing:0.3px;text-transform:uppercase;">日报定时</span>
        <div class="flow-col">
          <div class="flow-node orange" style="font-size:11px;padding:5px 10px;min-width:0;">⑩ 拉取全部群消息</div>
          <div class="flow-desc">老板所在所有工作群</div>
        </div>
        <div class="flow-arrow-h" style="font-size:13px;">→</div>
        <div class="flow-col">
          <div class="flow-node orange" style="font-size:11px;padding:5px 10px;min-width:0;">⑪ AI 筛选 + 生成日报</div>
          <div class="flow-desc">过滤闲聊，保留进展/风险</div>
        </div>
      </div>

    </div>

    <div style="text-align:center;color:#2d3748;font-size:13px;line-height:1;margin-bottom:6px;">↓</div>

    <!-- 结果 -->
    <div style="display:flex;justify-content:center;margin-bottom:8px;">
      <div class="flow-col">
        <div class="flow-node" style="background:#1a2a1a;border-color:#34C759;color:#34C759;min-width:140px;text-align:center;font-size:12px;padding:6px 12px;">⑫ 分片发送结果</div>
        <div class="flow-desc">超3800字自动分段推送</div>
      </div>
    </div>

    <!-- 常驻 + 图例 合并一行 -->
    <div style="display:flex;align-items:center;gap:16px;border-top:1px dashed #1e2530;padding-top:8px;flex-wrap:wrap;">
      <span style="font-size:10px;font-weight:700;color:#4a5568;text-transform:uppercase;white-space:nowrap;">常驻</span>
      <span style="font-size:11px;color:#6b7a95;">⚡ 异常兜底（报错发提示）</span>
      <span style="font-size:11px;color:#6b7a95;">🛡 崩溃自动恢复（3秒内重启）</span>
      <div style="flex:1;"></div>
      <div style="display:flex;gap:12px;align-items:center;">
        <div style="display:flex;align-items:center;gap:4px;font-size:10px;color:#6b7a95;"><div style="width:8px;height:8px;border-radius:2px;background:rgba(79,142,247,0.4);border:1px solid #4F8EF7;flex-shrink:0;"></div>文档预审</div>
        <div style="display:flex;align-items:center;gap:4px;font-size:10px;color:#6b7a95;"><div style="width:8px;height:8px;border-radius:2px;background:rgba(52,199,89,0.3);border:1px solid #34C759;flex-shrink:0;"></div>通用对话</div>
        <div style="display:flex;align-items:center;gap:4px;font-size:10px;color:#6b7a95;"><div style="width:8px;height:8px;border-radius:2px;background:rgba(255,149,0,0.3);border:1px solid #FF9500;flex-shrink:0;"></div>日报调度</div>
      </div>
    </div>

  </div>'''

def process(src):
    shutil.copy(src, src.replace('.html', '-pre-fix06.html'))
    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()

    # ── Fix 1: Soul tags gap + padding ───────────────────────────────────────
    # Container: gap:4px → gap:3px (only in the Soul flex-wrap div)
    html = html.replace(
        '<div style="display:flex;flex-wrap:wrap;gap:4px;">\n          <span style="font-size:10px;background:rgba(139,92,246',
        '<div style="display:flex;flex-wrap:wrap;gap:3px;">\n          <span style="font-size:10px;background:rgba(139,92,246'
    )
    # Soul tag padding: 2px 7px → 2px 5px (only purple soul tags)
    html = html.replace(
        'background:rgba(139,92,246,0.1);border:1px solid rgba(139,92,246,0.3);border-radius:4px;padding:2px 7px;color:#c4b5fd;',
        'background:rgba(139,92,246,0.1);border:1px solid rgba(139,92,246,0.3);border-radius:4px;padding:2px 5px;color:#c4b5fd;'
    )

    # ── Fix 2: Replace flow-wrap with new horizontal layout ──────────────────
    # Find the flow-wrap div inside agent-arch
    fw_start = html.index('<div class="flow-wrap">')
    fw_depth = 0
    fi = fw_start
    while fi < len(html):
        if html[fi:fi+4] == '<div':
            fw_depth += 1; fi += 4
        elif html[fi:fi+6] == '</div>':
            fw_depth -= 1; fi += 6
            if fw_depth == 0:
                break
        else:
            fi += 1
    html = html[:fw_start] + NEW_FLOW_WRAP + html[fi:]

    with open(src, 'w', encoding='utf-8') as f:
        f.write(html)

    count_fw = html.count('<div class="flow-wrap"')
    print(f"{src.split('/')[-1]}: done, flow-wrap count={count_fw}")

process('/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/index.html')
process('/Users/lth/vscode workspace/Projects/feishu-claude-bot/docs/architecture-report.html')
