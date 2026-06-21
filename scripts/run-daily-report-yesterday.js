#!/usr/bin/env node
// One-shot script: generate daily report for yesterday

require('dotenv').config();

const { runDailyReport } = require('../src/tasks/daily-report');

const yesterday = new Date();
yesterday.setDate(yesterday.getDate() - 1);
yesterday.setHours(0, 0, 0, 0);
const startMs = yesterday.getTime();
const endMs = yesterday.getTime() + 24 * 60 * 60 * 1000;

console.log(`[run-yesterday] ${yesterday.toLocaleDateString('zh-CN', { month: 'long', day: 'numeric', weekday: 'short' })}`);

runDailyReport(
  report => { console.log('\n' + '='.repeat(60) + '\n' + report + '\n' + '='.repeat(60) + `\n[${report.length} chars]`); },
  { startMs, endMs }
).catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
