#!/bin/bash
pkill -f "node server.js" 2>/dev/null
sleep 1
cd "$(dirname "$0")"
echo "🚀 Starting Feishu-Claude bridge..."
NO_PROXY="*" no_proxy="*" node server.js
