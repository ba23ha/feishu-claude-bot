const PATTERNS = [
  { type: 'distill', patterns: [/^\/distill/i, /蒸馏/, /读取.*群.*消息/, /提炼.*风格.*soul/i] },
  { type: 'reply', patterns: [/帮.*回复/, /代写.*回复/, /写.*回复/, /回一下/, /怎么回/, /reply/i] },
  { type: 'polish', patterns: [/润色/, /优化.*表达/, /改写/, /polish/i, /优化一下这/, /帮.*改一下/] },
  { type: 'review', patterns: [/点评/, /评价/, /看.*方案/, /看.*汇报/, /看.*计划/, /review/i, /分析.*方案/] },
  { type: 'meeting', patterns: [/会议纪要/, /提炼.*会议/, /总结.*会议/, /妙记/, /meeting/i, /纪要/] },
];

/**
 * Detect task type from user message text.
 * @param {string} text
 * @returns {'reply'|'polish'|'review'|'meeting'|'distill'|'general'}
 */
function detectTaskType(text) {
  for (const { type, patterns } of PATTERNS) {
    if (patterns.some(p => p.test(text))) return type;
  }
  return 'general';
}

module.exports = { detectTaskType };
