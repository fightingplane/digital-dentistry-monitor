#!/usr/bin/env python3
"""
处理 RSS 监控任务的简化版本
"""

import subprocess
import sys
import os

def main():
    """运行 RSS 监控"""
    script_path = "/home/admin/.openclaw/workspace/dental-digital-monitor/simple_monitor.py"
    
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print("✅ RSS 监控执行成功")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ RSS 监控执行失败: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("⏰ RSS 监控执行超时")
    except Exception as e:
        print(f"💥 RSS 监控执行异常: {e}")

if __name__ == "__main__":
    main()