#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信聊天自动回复表情包生成器
功能：监控微信PC版聊天窗口，检测新消息并自动发送随机表情包
作者：GitHub Copilot
日期：2025年7月5日
"""

import time
import random
import threading
import sys
import ctypes
from ctypes import wintypes
import comtypes.client
from comtypes import CoCreateInstance, CLSCTX_INPROC_SERVER, GUID
import pyautogui
import pygetwindow as gw
import win32gui
import win32api
import win32con
from typing import Optional, Tuple, List

# 导入键盘监听库
try:
    import keyboard
    HAS_KEYBOARD = True
except ImportError:
    try:
        from pynput import keyboard as pynput_keyboard
        HAS_PYNPUT = True
        HAS_KEYBOARD = False
    except ImportError:
        HAS_KEYBOARD = False
        HAS_PYNPUT = False
        print("警告：无法导入键盘监听库，将使用备选方案")

# 尝试导入UI Automation，如果失败则使用备选方案
try:
    import comtypes.gen.UIAutomationClient as UIAuto
    HAS_UIA = True
except ImportError:
    print("UI Automation模块未找到，将使用备选监控方案")
    HAS_UIA = False
    UIAuto = None

class WeChatAutoEmoji:
    def __init__(self):
        # 微信相关变量
        self.wechat_window = None
        self.wechat_hwnd = None
        self.chat_area_element = None
        self.emoji_button_pos = None
        self.emoji_panel_area = None
        
        # 初始化UI Automation（如果可用）
        self.uia = None
        if HAS_UIA:
            try:
                self.uia = CoCreateInstance(UIAuto.CUIAutomation._reg_clsid_, 
                                           interface=UIAuto.IUIAutomation, 
                                           clsctx=CLSCTX_INPROC_SERVER)
                print("UI Automation已初始化")
            except Exception as e:
                print(f"UI Automation初始化失败: {e}")
                self.uia = None
        
        # 监控状态
        self.is_monitoring = False
        self.last_message_count = 0
        self.last_window_title = ""
        self.monitoring_thread = None
        
        # 位置设置相关
        self.position_confirmed = False
        self.hotkey_listener = None
        
        # 配置
        self.check_interval = 0.5  # 检查间隔（秒）
        self.click_delay = 0.2     # 点击延迟（秒）
        
        print("微信自动表情包回复器已初始化")
        print("请确保微信PC版已经打开并登录")
    
    def find_wechat_window(self) -> bool:
        """查找微信窗口"""
        try:
            # 查找微信窗口
            wechat_windows = gw.getWindowsWithTitle("微信")
            if not wechat_windows:
                print("未找到微信窗口，请确保微信已经打开.你可能需要尝试:将wechat最小化后,再执行start命令.")
                return False
            
            self.wechat_window = wechat_windows[0]
            self.wechat_hwnd = self.wechat_window._hWnd
            
            # 激活微信窗口
            if self.wechat_window.isMinimized:
                self.wechat_window.restore()
            self.wechat_window.activate()
            
            print(f"找到微信窗口: {self.wechat_window.title}")
            print(f"窗口位置: ({self.wechat_window.left}, {self.wechat_window.top})")
            print(f"窗口大小: {self.wechat_window.width} x {self.wechat_window.height}")
            
            return True
            
        except Exception as e:
            print(f"查找微信窗口时出错: {e}")
            return False
    
    def get_wechat_automation_element(self):
        """获取微信窗口的UI Automation元素"""
        try:
            if not self.uia or not HAS_UIA:
                return None
                
            # 通过窗口句柄获取元素
            element = self.uia.ElementFromHandle(self.wechat_hwnd)
            if element:
                print("成功获取微信窗口的UI Automation元素")
                return element
            else:
                print("无法获取微信窗口的UI Automation元素")
                return None
                
        except Exception as e:
            print(f"获取UI Automation元素时出错: {e}")
            return None
    
    def find_chat_area(self, root_element):
        """查找聊天区域元素"""
        try:
            if not self.uia or not HAS_UIA or not root_element:
                return False
                
            # 尝试查找聊天消息列表
            # 微信的聊天区域通常是一个列表控件
            condition = self.uia.CreatePropertyCondition(
                UIAuto.UIA_ControlTypePropertyId, 
                UIAuto.UIA_ListControlTypeId
            )
            
            chat_lists = root_element.FindAll(UIAuto.TreeScope_Descendants, condition)
            
            if chat_lists.Length > 0:
                # 通常聊天区域是最大的列表控件
                largest_list = None
                max_size = 0
                
                for i in range(chat_lists.Length):
                    list_element = chat_lists.GetElement(i)
                    rect = list_element.CurrentBoundingRectangle
                    size = rect.right * rect.bottom
                    
                    if size > max_size:
                        max_size = size
                        largest_list = list_element
                
                if largest_list:
                    self.chat_area_element = largest_list
                    print("找到聊天区域")
                    return True
            
            print("未找到聊天区域，将使用备选方案")
            return False
            
        except Exception as e:
            print(f"查找聊天区域时出错: {e}")
            return False
    
    def wait_for_hotkey(self, timeout=30) -> bool:
        """等待热键确认，支持多种方式"""
        self.position_confirmed = False
        
        print("等待确认位置...")
        print("请选择以下任一方式确认当前鼠标位置：(推荐使用2)")
        print("1. 按 F1 键确认")
        print("2. 按 Ctrl+空格 确认")
        print("3. 按 Ctrl+Shift+C 确认")
        print("4. 同时按住 Ctrl+Alt 然后点击鼠标左键")
        print("(超时时间: 30秒)")
        
        start_time = time.time()
        
        if HAS_KEYBOARD:
            # 使用keyboard库监听热键
            def on_hotkey():
                self.position_confirmed = True
                print("位置已确认！")
            
            # 注册多个热键
            keyboard.add_hotkey('f1', on_hotkey)
            keyboard.add_hotkey('ctrl+space', on_hotkey)
            keyboard.add_hotkey('ctrl+shift+c', on_hotkey)
            
            # 等待确认或超时
            while not self.position_confirmed and (time.time() - start_time) < timeout:
                time.sleep(0.1)
            
            # 清除热键
            keyboard.clear_all_hotkeys()
            
        elif HAS_PYNPUT:
            # 使用pynput库监听
            def on_key_press(key):
                try:
                    if key == pynput_keyboard.Key.f1:
                        self.position_confirmed = True
                        print("位置已确认！")
                        return False  # 停止监听
                except AttributeError:
                    pass
            
            listener = pynput_keyboard.Listener(on_press=on_key_press)
            listener.start()
            
            # 等待确认或超时
            while not self.position_confirmed and (time.time() - start_time) < timeout:
                time.sleep(0.1)
            
            listener.stop()
            
        else:
            # 备选方案：使用简单的时间延迟
            print("键盘监听不可用，将使用备选方案")
            print("请在3秒内将鼠标移动到目标位置...")
            for i in range(3, 0, -1):
                print(f"倒计时: {i}")
                time.sleep(1)
            self.position_confirmed = True
        
        if not self.position_confirmed:
            print("确认超时！")
            return False
        
        return True
    
    def setup_emoji_positions(self) -> bool:
        """设置表情包按钮和面板位置"""
        print("\n=== 表情包位置设置 ===")
        print("注意：由于需要在微信窗口中操作，我们将使用热键来确认位置")
        print()
        
        # 设置表情包按钮位置
        print("步骤 1: 设置表情包按钮位置")
        print("-" * 40)
        print("1. 请切换到微信窗口")
        print("2. 将鼠标移动到表情包按钮上（聊天输入框右侧的表情图标）")
        print("3. 使用热键确认位置")
        
        if not self.wait_for_hotkey():
            print("表情包按钮位置设置失败")
            return False
        
        self.emoji_button_pos = pyautogui.position()
        print(f"✓ 表情包按钮位置已设置: {self.emoji_button_pos}")
        
        # 设置表情包面板区域
        print("\n步骤 2: 设置表情包面板区域")
        print("-" * 40)
        print("1. 请先点击表情包按钮打开表情包面板")
        print("2. 将鼠标移动到表情包面板的左上角")
        print("3. 使用热键确认左上角位置")
        
        if not self.wait_for_hotkey():
            print("表情包面板左上角位置设置失败")
            return False
        
        panel_top_left = pyautogui.position()
        print(f"✓ 表情包面板左上角: {panel_top_left}")
        
        print("\n步骤 3: 设置表情包面板右下角")
        print("-" * 40)
        print("1. 将鼠标移动到表情包面板的右下角")
        print("2. 使用热键确认右下角位置")
        
        if not self.wait_for_hotkey():
            print("表情包面板右下角位置设置失败")
            return False
        
        panel_bottom_right = pyautogui.position()
        print(f"✓ 表情包面板右下角: {panel_bottom_right}")
        
        # 保存面板区域信息
        self.emoji_panel_area = {
            'left': panel_top_left.x,
            'top': panel_top_left.y,
            'right': panel_bottom_right.x,
            'bottom': panel_bottom_right.y,
            'width': panel_bottom_right.x - panel_top_left.x,
            'height': panel_bottom_right.y - panel_top_left.y
        }
        
        print(f"✓ 表情包面板区域已设置: {self.emoji_panel_area}")
        
        # 关闭表情包面板
        print("\n步骤 4: 关闭表情包面板")
        print("-" * 40)
        print("请手动关闭表情包面板（点击其他地方或按ESC）")
        print("然后使用热键确认...")
        
        if not self.wait_for_hotkey():
            print("警告：未确认表情包面板关闭，但设置已完成")
        
        print("\n✓ 位置设置完成！")
        print("现在可以开始监控了")
        return True
    
    def get_message_count(self) -> int:
        """获取当前聊天区域的消息数量"""
        try:
            if self.chat_area_element and self.uia and HAS_UIA:
                # 尝试获取子元素数量
                condition = self.uia.CreateTrueCondition()
                children = self.chat_area_element.FindAll(UIAuto.TreeScope_Children, condition)
                return children.Length
            else:
                # 备选方案：监控窗口标题变化
                # 当有新消息时，微信窗口标题通常会显示未读消息数量
                if self.wechat_window:
                    current_title = self.wechat_window.title
                    if current_title != self.last_window_title:
                        self.last_window_title = current_title
                        # 如果标题包含数字（可能是未读消息数量），认为有新消息
                        import re
                        if re.search(r'\(\d+\)', current_title) or re.search(r'\[\d+\]', current_title):
                            return 1  # 返回一个非零值表示有新消息
                return 0
                
        except Exception as e:
            print(f"获取消息数量时出错: {e}")
            return 0
    
    def detect_new_message(self) -> bool:
        """检测是否有新消息 - 使用多种方法"""
        try:
            # 方法1：如果有UI Automation支持，使用元素变化检测
            if self.chat_area_element and self.uia and HAS_UIA:
                current_count = self.get_message_count()
                if current_count > self.last_message_count:
                    print(f"检测到新消息！消息数量从 {self.last_message_count} 增加到 {current_count}")
                    self.last_message_count = current_count
                    return True
                self.last_message_count = current_count
            
            # 方法2：监控窗口标题变化（未读消息通知）
            if self.wechat_window:
                current_title = self.wechat_window.title
                if current_title != self.last_window_title:
                    self.last_window_title = current_title
                    # 检查标题是否包含未读消息标识
                    import re
                    if re.search(r'\(\d+\)', current_title) or re.search(r'\[\d+\]', current_title):
                        print(f"通过窗口标题检测到新消息: {current_title}")
                        return True
            
            # 方法3：监控系统通知（Windows Toast通知）
            # 这个方法比较复杂，暂时不实现
            
            return False
            
        except Exception as e:
            print(f"检测新消息时出错: {e}")
            return False
    
    def click_emoji_button(self) -> bool:
        """点击表情包按钮"""
        try:
            if not self.emoji_button_pos:
                print("表情包按钮位置未设置")
                return False
            
            # 确保微信窗口是活动的
            if self.wechat_window:
                self.wechat_window.activate()
                time.sleep(0.1)
            
            # 点击表情包按钮
            pyautogui.click(self.emoji_button_pos.x, self.emoji_button_pos.y)
            time.sleep(self.click_delay)
            
            print("已点击表情包按钮")
            return True
            
        except Exception as e:
            print(f"点击表情包按钮时出错: {e}")
            return False
    
    def select_random_emoji(self) -> bool:
        """随机选择并点击一个表情包"""
        try:
            if not self.emoji_panel_area:
                print("表情包面板区域未设置")
                return False
            
            # 等待表情包面板打开
            time.sleep(0.3)
            
            # 在表情包面板区域内随机选择一个位置点击
            panel = self.emoji_panel_area
            
            # 避免点击到边缘，留出一定边距
            margin = 20
            random_x = random.randint(panel['left'] + margin, panel['right'] - margin)
            random_y = random.randint(panel['top'] + margin, panel['bottom'] - margin)
            
            # 点击随机位置
            pyautogui.click(random_x, random_y)
            time.sleep(self.click_delay)
            
            print(f"已点击表情包位置: ({random_x}, {random_y})")
            
            # 等待表情包发送
            time.sleep(0.2)
            
            return True
            
        except Exception as e:
            print(f"选择表情包时出错: {e}")
            return False
    
    def send_random_emoji(self) -> bool:
        """发送随机表情包的完整流程"""
        try:
            print("开始发送随机表情包...")
            
            # 1. 点击表情包按钮
            if not self.click_emoji_button():
                return False
            
            # 2. 选择随机表情包
            if not self.select_random_emoji():
                return False
            
            print("随机表情包发送完成！")
            return True
            
        except Exception as e:
            print(f"发送表情包时出错: {e}")
            return False
    
    def monitoring_loop(self):
        """消息监控循环"""
        print("开始监控微信消息...")
        
        while self.is_monitoring:
            try:
                # 检查微信窗口是否还存在
                if not self.wechat_window or not win32gui.IsWindow(self.wechat_hwnd):
                    print("微信窗口已关闭，停止监控")
                    self.stop_monitoring()
                    break
                
                # 检测新消息
                if self.detect_new_message():
                    print("检测到新消息，准备发送表情包...")
                    
                    # 发送随机表情包
                    if self.send_random_emoji():
                        print("表情包发送成功！")
                    else:
                        print("表情包发送失败")
                
                # 等待一段时间再检查
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"监控循环中发生错误: {e}")
                time.sleep(1)
    
    def start_monitoring(self):
        """开始监控"""
        if self.is_monitoring:
            print("已经在监控中...")
            return
        
        # 查找微信窗口
        if not self.find_wechat_window():
            return
        
        # 获取UI Automation元素
        root_element = self.get_wechat_automation_element()
        if not root_element:
            print("无法获取微信窗口的UI元素，将使用备选监控方案")
        else:
            # 查找聊天区域
            self.find_chat_area(root_element)
        
        # 设置表情包位置
        if not self.setup_emoji_positions():
            print("表情包位置设置失败")
            return
        
        # 初始化消息计数
        self.last_message_count = self.get_message_count()
        print(f"初始消息数量: {self.last_message_count}")
        
        # 启动监控
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        print("监控已启动！")
    
    def stop_monitoring(self):
        """停止监控"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2)
        print("监控已停止")
    
    def run(self):
        """运行主程序"""
        print("=== 微信自动表情包回复器 ===")
        print("注意事项：")
        print("1. 请确保微信PC版已经打开并登录")
        print("2. 请打开您想要自动回复的聊天窗口")
        print("3. 程序将监控当前活跃的聊天窗口")
        print("4. 检测到新消息时会自动发送随机表情包")
        print()
        
        while True:
            try:
                print("\n可用命令：")
                print("1. start - 开始监控")
                print("2. stop - 停止监控")
                print("3. test - 测试发送表情包")
                print("4. setup - 重新设置表情包位置")
                print("5. quit - 退出程序")
                
                command = input("\n请输入命令: ").strip().lower()
                
                if command == "start":
                    self.start_monitoring()
                    
                elif command == "stop":
                    self.stop_monitoring()
                    
                elif command == "test":
                    if self.emoji_button_pos and self.emoji_panel_area:
                        print("测试发送表情包...")
                        self.send_random_emoji()
                    else:
                        print("请先运行 start 命令设置位置")
                        
                elif command == "setup":
                    self.setup_emoji_positions()
                    
                elif command == "quit":
                    self.stop_monitoring()
                    print("程序已退出")
                    break
                    
                else:
                    print("无效命令，请重新输入")
                    
            except KeyboardInterrupt:
                self.stop_monitoring()
                print("\n程序已退出")
                break
            except Exception as e:
                print(f"程序运行时出错: {e}")

def main():
    """主函数"""
    try:
        # 设置pyautogui的安全设置
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        # 创建并运行程序
        app = WeChatAutoEmoji()
        app.run()
        
    except Exception as e:
        print(f"程序启动失败: {e}")
        input("按 Enter 键退出...")

if __name__ == "__main__":
    main()
