#!/bin/bash
# Memory Manager - Bash 包装脚本
# 方便 OpenClaw 和其他脚本调用记忆管理系统

MEMORY_MANAGER="/home/devbox/.openclaw/workspace/tools/memory_manager.py"

# 确保脚本可执行
chmod +x "$MEMORY_MANAGER"

# 命令分发
case "$1" in
    startup)
        python3 "$MEMORY_MANAGER" startup
        ;;
    add)
        if [ $# -lt 4 ]; then
            echo "用法: memory.sh add <type> <source> <description> [data.json]"
            exit 1
        fi
        python3 "$MEMORY_MANAGER" add "$2" "$3" "$4" "$5"
        ;;
    cleanup)
        HOURS="${2:-24}"
        python3 "$MEMORY_MANAGER" cleanup "$HOURS"
        ;;
    summary)
        python3 "$MEMORY_MANAGER" summary
        ;;
    auto)
        python3 "$MEMORY_MANAGER" auto
        ;;
    *)
        echo "用法: $0 {startup|add|cleanup|summary|auto}"
        echo ""
        echo "命令:"
        echo "  startup      - 启动时加载记忆"
        echo "  add         - 添加事件 (需要 3 个参数)"
        echo "  cleanup     - 清理过期事件 (可选小时数，默认 24)"
        echo "  summary     - 显示记忆摘要"
        echo "  auto        - 自动化模式 (清理 + 摘要)"
        exit 1
        ;;
esac
