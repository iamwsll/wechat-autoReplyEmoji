#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成comtypes所需的UI Automation模块
"""

import comtypes.client

def generate_uiautomation_module():
    """生成UI Automation的comtypes模块"""
    try:
        print("正在生成UI Automation模块...")
        
        # 这将生成comtypes.gen.UIAutomationClient模块
        comtypes.client.GetModule("UIAutomationCore.dll")
        
        print("UI Automation模块生成完成！")
        return True
        
    except Exception as e:
        print(f"生成UI Automation模块时出错: {e}")
        return False

if __name__ == "__main__":
    generate_uiautomation_module()
