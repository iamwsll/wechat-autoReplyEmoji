#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试微信自动表情包程序的基本功能
"""

import sys
import os

def test_imports():
    """测试所有必要的模块导入"""
    print("测试模块导入...")
    
    try:
        import pyautogui
        print("✓ pyautogui 导入成功")
    except ImportError as e:
        print(f"✗ pyautogui 导入失败: {e}")
        return False
    
    try:
        import pygetwindow as gw
        print("✓ pygetwindow 导入成功")
    except ImportError as e:
        print(f"✗ pygetwindow 导入失败: {e}")
        return False
    
    try:
        import win32gui
        print("✓ win32gui 导入成功")
    except ImportError as e:
        print(f"✗ win32gui 导入失败: {e}")
        return False
    
    try:
        import comtypes.client
        print("✓ comtypes 导入成功")
    except ImportError as e:
        print(f"✗ comtypes 导入失败: {e}")
        return False
    
    try:
        import comtypes.gen.UIAutomationClient as UIAuto
        print("✓ UI Automation 模块导入成功")
    except ImportError as e:
        print(f"⚠ UI Automation 模块导入失败: {e}")
        print("  程序将使用备选监控方案")
    try:
        import keyboard
        print("✓ keyboard 导入成功")
    except ImportError:
        try:
            from pynput import keyboard as pynput_keyboard
            print("✓ pynput 导入成功（备选）")
        except ImportError:
            print("⚠ keyboard 和 pynput 都导入失败")
            print("  位置设置功能可能受限")
    
    return True

def test_wechat_detection():
    """测试微信窗口检测"""
    print("\n测试微信窗口检测...")
    
    try:
        import pygetwindow as gw
        wechat_windows = gw.getWindowsWithTitle("微信")
        
        if wechat_windows:
            print(f"✓ 找到 {len(wechat_windows)} 个微信窗口")
            for i, window in enumerate(wechat_windows):
                print(f"  窗口 {i+1}: {window.title}")
                print(f"    位置: ({window.left}, {window.top})")
                print(f"    大小: {window.width} x {window.height}")
        else:
            print("✗ 未找到微信窗口")
            print("  请确保微信PC版已经打开")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ 微信窗口检测失败: {e}")
        return False

def test_mouse_control():
    """测试鼠标控制功能"""
    print("\n测试鼠标控制...")
    
    try:
        import pyautogui
        
        # 获取当前鼠标位置
        current_pos = pyautogui.position()
        print(f"✓ 当前鼠标位置: {current_pos}")
        
        # 测试安全设置
        pyautogui.FAILSAFE = True
        print("✓ 鼠标安全停止功能已启用")
        
        return True
        
    except Exception as e:
        print(f"✗ 鼠标控制测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=== 微信自动表情包程序测试 ===\n")
    
    all_tests_passed = True
    
    # 测试模块导入
    if not test_imports():
        all_tests_passed = False
    
    # 测试微信检测
    if not test_wechat_detection():
        all_tests_passed = False
    
    # 测试鼠标控制
    if not test_mouse_control():
        all_tests_passed = False
    
    # 输出测试结果
    print("\n=== 测试结果 ===")
    if all_tests_passed:
        print("✓ 所有测试通过！程序可以正常运行")
        print("\n现在可以运行主程序: python wechat_auto_emoji.py")
    else:
        print("✗ 部分测试失败，请检查上述错误信息")
    
    input("\n按 Enter 键退出...")

if __name__ == "__main__":
    main()
