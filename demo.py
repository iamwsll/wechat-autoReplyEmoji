#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信自动表情包程序演示脚本
用于快速展示程序功能，无需完整设置
"""

import pyautogui
import pygetwindow as gw
import time

def demo_wechat_detection():
    """演示微信窗口检测功能"""
    print("=== 微信窗口检测演示 ===")
    
    try:
        # 查找微信窗口
        wechat_windows = gw.getWindowsWithTitle("微信")
        
        if wechat_windows:
            window = wechat_windows[0]
            print(f"找到微信窗口: {window.title}")
            print(f"位置: ({window.left}, {window.top})")
            print(f"大小: {window.width} x {window.height}")
            
            # 激活窗口
            if window.isMinimized:
                window.restore()
            window.activate()
            print("微信窗口已激活")
            
            return True
        else:
            print("未找到微信窗口")
            return False
            
    except Exception as e:
        print(f"检测失败: {e}")
        return False

def demo_mouse_position():
    """演示鼠标位置获取"""
    print("\n=== 鼠标位置演示 ===")
    print("请移动鼠标到不同位置，程序将显示实时坐标")
    print("按 Ctrl+C 结束演示")
    
    try:
        for i in range(20):  # 显示20次坐标
            pos = pyautogui.position()
            print(f"鼠标位置: ({pos.x}, {pos.y})", end='\r')
            time.sleep(0.5)
        print()  # 换行
        
    except KeyboardInterrupt:
        print("\n演示结束")

def demo_click_simulation():
    """演示点击模拟（仅获取位置，不实际点击）"""
    print("\n=== 点击模拟演示 ===")
    print("程序将获取当前鼠标位置作为点击目标")
    
    target_pos = pyautogui.position()
    print(f"目标位置: ({target_pos.x}, {target_pos.y})")
    
    print("如果这是表情包按钮位置，程序将在此处点击")
    print("（演示模式，不会实际点击）")

def main():
    """主演示函数"""
    print("微信自动表情包程序 - 演示模式")
    print("=" * 40)
    
    # 设置安全模式
    pyautogui.FAILSAFE = True
    
    # 演示窗口检测
    if not demo_wechat_detection():
        print("请先打开微信PC版")
        input("按 Enter 键退出...")
        return
    
    # 演示鼠标位置获取
    try:
        demo_mouse_position()
    except KeyboardInterrupt:
        pass
    
    # 演示点击模拟
    demo_click_simulation()
    
    print("\n=== 演示完成 ===")
    print("现在可以运行完整程序: python wechat_auto_emoji.py")
    input("按 Enter 键退出...")

if __name__ == "__main__":
    main()
