module.exports = {
  apps: [{
    name: 'feishu-bot',
    script: 'server.js',
    cwd: '/Users/lth/vscode workspace/Projects/feishu-claude-bot',
    instances: 1,
    exec_mode: 'fork',
    autorestart: true,
    watch: false,
    // Wait 3s before restarting after crash — prevents rapid restart loops
    restart_delay: 3000,
    // Exponential backoff: 100ms → 200ms → 400ms → ... up to 16s
    exp_backoff_restart_delay: 100,
    max_memory_restart: '300M',
    // Daily restart at 4am to refresh WebSocket connection
    cron_restart: '0 4 * * *',
    env: {
      NODE_ENV: 'production',
      NO_PROXY: 'open.feishu.cn',
      no_proxy: 'open.feishu.cn',
    },
    // Log settings
    out_file: '/Users/lth/.pm2/logs/feishu-bot-out-0.log',
    error_file: '/Users/lth/.pm2/logs/feishu-bot-error-0.log',
    merge_logs: true,
    log_date_format: 'YYYY-MM-DD HH:mm:ss',
  }],
};
