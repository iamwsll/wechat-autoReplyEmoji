#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试热键功能
"""

import time
import pyautogui

# 导入键盘监听库
try:
    import keyboard
    HAS_KEYBOARD = True
    print("✓ keyboard库可用")
except ImportError:
    HAS_KEYBOARD = False
    try:
        from pynput import keyboard as pynput_keyboard
        HAS_PYNPUT = True
        print("✓ pynput库可用")
    except ImportError:
        HAS_PYNPUT = False
        print("✗ 没有可用的键盘监听库")

def test_hotkey_detection():
    """测试热键检测功能"""
    print("\n=== 热键检测测试 ===")
    
    position_confirmed = False
    
    def confirm_position():
        nonlocal position_confirmed
        position_confirmed = True
        pos = pyautogui.position()
        print(f"位置已确认！当前鼠标位置: {pos}")
    
    if HAS_KEYBOARD:
        print("使用keyboard库进行热键检测")
        print("请按 F1 键确认当前鼠标位置...")
        
        keyboard.add_hotkey('f1', confirm_position)
        
        start_time = time.time()
        while not position_confirmed and (time.time() - start_time) < 10:
            time.sleep(0.1)
        
        keyboard.clear_all_hotkeys()
        
    elif HAS_PYNPUT:
        print("使用pynput库进行热键检测")
        print("请按 F1 键确认当前鼠标位置...")
        
        def on_key_press(key):
            try:
                if key == pynput_keyboard.Key.f1:
                    confirm_position()
                    return False  # 停止监听
            except AttributeError:
                pass
        
        listener = pynput_keyboard.Listener(on_press=on_key_press)
        listener.start()
        
        start_time = time.time()
        while not position_confirmed and (time.time() - start_time) < 10:
            time.sleep(0.1)
        
        listener.stop()
    
    else:
        print("没有可用的键盘监听库，跳过测试")
        return False
    
    if position_confirmed:
        print("✓ 热键检测测试成功")
        return True
    else:
        print("✗ 热键检测测试失败（超时）")
        return False

def main():
    print("微信表情包程序 - 热键功能测试")
    print("=" * 40)
    
    success = test_hotkey_detection()
    
    if success:
        print("\n✓ 热键功能正常，可以解决微信窗口焦点问题")
    else:
        print("\n✗ 热键功能异常，请检查键盘监听库安装")
    
    input("\n按 Enter 键退出...")

if __name__ == "__main__":
    main()
