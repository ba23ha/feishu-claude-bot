#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const file = path.join(__dirname, '..', 'docs', 'boss-copilot.html');
const html = fs.readFileSync(file, 'utf8');

const checks = [
  ['日报 Demo 页面', 'id="demo-daily-report"'],
  ['批注 Demo 页面', 'id="demo-inline-review"'],
  ['真实 Demo 导航', '</span>真实 Demo</button>'],
  ['双页共用导航映射', 'data-nav-group="real-demo"'],
  ['真实日报截图', 'assets/demo/daily-report-2026-06-26.png'],
  ['真实批注预览截图', 'assets/demo/inline-review-preview-2026-06-29.jpg'],
  ['真实批注结果截图', 'assets/demo/inline-review-comments-2026-06-29.jpg'],
  ['截图上半部分', 'data-demo-crop="daily-top"'],
  ['截图下半部分', 'data-demo-crop="daily-bottom"'],
  ['批注预览截图', 'data-demo-crop="inline-review-preview"'],
  ['预览识别框选', 'data-inline-annotation="preview"'],
  ['确认按钮框选', 'data-inline-annotation="confirm"'],
  ['文档正文锚点框选', 'data-inline-annotation="doc-anchor"'],
  ['评论栏结果框选', 'data-inline-annotation="comment-panel"'],
  ['文档批注摘要', '识别 5 个值得批注的问题'],
  ['风险分级批注', '① 先看风险 · 2红 / 2黄 / 1绿'],
  ['决策收敛批注', '>② 再做收敛</span>'],
  ['行动转化批注', '>③ 落到行动</span>'],
  ['风险图片框选', 'data-image-annotation="risk"'],
  ['收敛图片框选', 'data-image-annotation="focus"'],
  ['行动图片框选', 'data-image-annotation="action"'],
  ['风险图片胶囊', 'data-annotation-pill="risk"'],
  ['收敛图片胶囊', 'data-annotation-pill="focus"'],
  ['行动图片胶囊', 'data-annotation-pill="action"'],
];

const failures = checks.filter(([, token]) => !html.includes(token));

const reviewIndex = html.indexOf('id="demo-inline-review"');
const architectureIndex = html.indexOf('id="arch"');
if (reviewIndex === -1 || architectureIndex === -1 || reviewIndex > architectureIndex) {
  failures.push(['Demo 页面位于架构页之前', 'expected ordering']);
}

if (failures.length) {
  for (const [label] of failures) console.error(`FAIL: ${label}`);
  process.exit(1);
}

if (html.includes('先看风险</div><div style=')) {
  console.error('FAIL: 三段说明仍使用独立卡片');
  process.exit(1);
}

if (html.includes('data-annotation-label=')) {
  console.error('FAIL: 胶囊仍被移到图片外');
  process.exit(1);
}

if (html.includes('示例占位')) {
  console.error('FAIL: 第二个 Demo 仍包含示例占位');
  process.exit(1);
}

console.log('PASS: real Demo pages are present and correctly ordered');
