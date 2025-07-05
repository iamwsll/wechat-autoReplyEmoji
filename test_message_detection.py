#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信消息检测测试脚本
专门用于测试新的消息检测机制
"""

import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from wechat_auto_emoji import WeChatAutoEmoji

def main():
    print("=== 微信消息检测测试工具 ===")
    print("此工具用于测试改进后的消息检测机制")
    print("使用前请确保：")
    print("1. 微信PC版已打开并登录")
    print("2. 已打开一个聊天窗口")
    print("3. 准备接收或发送一些测试消息")
    print("-" * 50)
    
    bot = WeChatAutoEmoji()
    
    try:
        # 直接运行测试
        bot.test_message_detection()
    except KeyboardInterrupt:
        print("\n测试已结束")
    except Exception as e:
        print(f"测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
