#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信表情包发送冷却机制演示
展示如何防止发送表情包后的无限循环问题
"""

import time
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demo_cooldown_mechanism():
    """演示冷却机制的工作原理"""
    print("=== 表情包发送冷却机制演示 ===")
    print()
    print("问题场景：")
    print("1. 程序检测到新消息")
    print("2. 发送表情包回复")
    print("3. 表情包出现在聊天区域")
    print("4. 被误判为'新消息'")
    print("5. 触发新一轮发送 → 无限循环")
    print()
    print("解决方案（v1.2）：")
    print("1. 发送冷却机制 - 发送后进入冷却期")
    print("2. 消息来源识别 - 区分自己和他人的消息")
    print("3. 智能基线更新 - 冷却期后重新设定检测基准")
    print()
    
    # 模拟冷却机制
    emoji_cooldown = 3.0
    just_sent_emoji = False
    emoji_send_time = 0
    
    print("=== 模拟运行过程 ===")
    
    # 模拟检测到新消息
    print("✓ 检测到他人发送的新消息")
    print("→ 准备发送表情包...")
    
    # 模拟发送表情包
    print("✓ 表情包发送成功")
    just_sent_emoji = True
    emoji_send_time = time.time()
    print(f"→ 进入 {emoji_cooldown} 秒冷却期...")
    print()
    
    # 模拟冷却期内的检测
    for i in range(int(emoji_cooldown) + 1):
        current_time = time.time()
        remaining = max(0, emoji_cooldown - (current_time - emoji_send_time))
        
        if remaining > 0:
            print(f"[冷却中] 剩余 {remaining:.1f} 秒 - 暂停消息检测")
        else:
            just_sent_emoji = False
            print("[冷却结束] 恢复消息检测，更新检测基线")
            print("→ 准备检测新的消息...")
            break
        
        time.sleep(1)
    
    print()
    print("=== 机制特点 ===")
    print("• 防止无限循环：冷却期内不响应任何消息")
    print("• 智能识别：区分自己和他人发送的消息")
    print("• 可配置性：用户可自定义冷却时间")
    print("• 状态监控：实时查看冷却状态")
    print()
    print("=== 使用建议 ===")
    print("• 默认冷却时间：3秒（推荐）")
    print("• 活跃群聊：可适当延长至5-10秒")
    print("• 私人聊天：可缩短至1-2秒")
    print("• 使用 'cooldown' 命令调整冷却时间")
    print("• 使用 'status' 命令查看当前状态")

def main():
    try:
        demo_cooldown_mechanism()
    except KeyboardInterrupt:
        print("\n演示结束")

if __name__ == "__main__":
    main()
