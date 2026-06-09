#!/usr/bin/env node
/**
 * Batch distillation: iterate over groups × soul files
 * Usage: node scripts/batch-distill.js
 */
require('dotenv').config();
const { distill, parseDistillCommand } = require('../src/soul/updater');
const { createAuditContext, generateReport } = require('../src/audit/runner');

// Already completed: GPTPro, AI-Agent Team, 33 direct team, WTCCN HO Data Lab & Product (all 4 files)
// WTCCN_Product identity done; resume from style
const GROUPS = [
  { id: 'oc_e36a9993ef6b10df9d425a692f712fd8', name: 'WTCCN HO Data Lab & Product_Product', skipFiles: ['identity'] },
  { id: 'oc_7de7e9b33dfcb06c3d7097a9ec81894e', name: '门店服务应用内部工作群' },
  { id: 'oc_96d19b40e4edf46961d267b067786d28', name: 'AI效率先锋大赛--内部群' },
  { id: 'oc_0e90958e82b4d0cc00a566e3ab538b25', name: '屈臣氏飞书Aily落地场景沟通' },
  { id: 'oc_0c3d0a34ef1e8527a1fde8c15cb1a04e', name: 'CB1.0 商品陈列属性需求沟通' },
  { id: 'oc_f7d79bda2c02c3b7799325ac9fa04ead', name: 'ChatStore未来云店（+供应商）' },
  { id: 'oc_85e15d4d13c4f8e18bfc058af0fce1a3', name: 'CB1.0项目跟进搬砖群' },
  { id: 'oc_c899cc64c9be8ae2e76ae07bc52007f3', name: 'People & Product 智能问答沟通群' },
  { id: 'oc_cd42097eca1fff20e8ed03d1ed2be2b1', name: '物料管理项目二期需求沟通' },
  { id: 'oc_ee2d4d81a9ea0f4bf252efb5338d3318', name: '物料下发场景迁移飞书工作小组' },
  { id: 'oc_30926cda9fab625269c5bee034594039', name: 'CB对接BPM沟通群' },
  { id: 'oc_19cef09f02bbd88d6c9c57b91d226d1a', name: '屈臣氏飞书专属运维中心' },
  { id: 'oc_8221448fd17cf01082e36516adbf9858', name: '01 x 九章 CDH沟通群' },
];

const SOUL_FILES = ['management', 'style', 'decision', 'communication'];
const DAYS = 90;

async function run() {
  const total = GROUPS.length * SOUL_FILES.length;
  let done = 0, skipped = 0, failed = 0;

  for (const group of GROUPS) {
    for (const file of SOUL_FILES) {
      if (group.skipFiles?.includes(file)) continue;
      done++;
      const reason = `批量蒸馏-${group.name}-${file}`;
      const opts = {
        targetFile: file,
        chatId: group.id,
        startMs: Date.now() - DAYS * 24 * 60 * 60 * 1000,
        endMs: Date.now(),
        reason,
      };
      process.stdout.write(`[${done}/${total}] ${group.name} → ${file} ... `);
      try {
        const auditContext = createAuditContext(opts, 'batch-distill', `batch_${Date.now()}`);
        await distill(opts, auditContext);
        console.log('✅');
      } catch (err) {
        console.log('❌', err.message.slice(0, 60));
        failed++;
      }
      // Avoid rate limiting
      await new Promise(r => setTimeout(r, 1500));
    }
  }

  console.log(`\n完成: ${done - failed} 成功, ${failed} 失败 / 共 ${total} 个任务`);
}

run().catch(console.error);
