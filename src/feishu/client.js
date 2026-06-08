require('dotenv').config();
const { Client, LoggerLevel } = require('@larksuiteoapi/node-sdk');

let _client = null;

function getFeishuClient() {
  if (!_client) {
    if (!process.env.FEISHU_APP_ID || !process.env.FEISHU_APP_SECRET) {
      throw new Error('FEISHU_APP_ID and FEISHU_APP_SECRET must be set');
    }
    _client = new Client({
      appId: process.env.FEISHU_APP_ID,
      appSecret: process.env.FEISHU_APP_SECRET,
      loggerLevel: LoggerLevel.error,
    });
  }
  return _client;
}

module.exports = { getFeishuClient };
