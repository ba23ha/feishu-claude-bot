const PATTERNS = [
  { type: 'distill', patterns: [/^\/distill/i, /蒸馏/, /读取.*群.*消息/, /提炼.*风格.*soul/i] },
  { type: 'reply', patterns: [/帮.*回复/, /代写.*回复/, /写.*回复/, /回一下/, /怎么回/, /reply/i, /润色/, /优化.*表达/, /改写/, /polish/i, /优化一下这/, /帮.*改一下/] },
  // review_inline must come before review to avoid false matches on doc URLs
  { type: 'review_inline', patterns: [
    /自动批注/, /文档批注/, /帮.*文档.*评论/, /在.*文档.*批注/, /看.*文档.*批注/,
    /feishu\.cn\/(docx|wiki)\/[A-Za-z0-9]+/,
  ]},
  { type: 'review', patterns: [/点评/, /评价/, /看.*方案/, /看.*汇报/, /看.*计划/, /review/i, /分析.*方案/] },
  { type: 'meeting', patterns: [/会议纪要/, /提炼.*会议/, /总结.*会议/, /妙记/, /meeting/i, /纪要/] },
  { type: 'delegation', patterns: [/帮.*安排/, /委派/, /写.*任务/, /派给/, /delegation/i] },
  { type: 'followup', patterns: [/催一下/, /追.*进度/, /问.*进展/, /跟进/, /followup/i, /follow.?up/i] },
];

/**
 * Detect task type from user message text.
 * @param {string} text
 * @returns {'reply'|'review'|'review_inline'|'meeting'|'delegation'|'followup'|'distill'|'general'}
 */
function detectTaskType(text) {
  for (const { type, patterns } of PATTERNS) {
    if (patterns.some(p => p.test(text))) return type;
  }
  return 'general';
}

/**
 * Extract Feishu document token and URL type from a message.
 * @param {string} text
 * @returns {{ token: string, urlType: 'docx'|'wiki' } | null}
 */
function extractDocToken(text) {
  const m = text.match(/feishu\.cn\/(docx|wiki)\/([A-Za-z0-9]+)/);
  if (!m) return null;
  return { token: m[2], urlType: m[1] };
}

module.exports = { detectTaskType, extractDocToken };
