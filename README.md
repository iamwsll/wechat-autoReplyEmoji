# 微信自动表情包回复器 使用说明

## 功能介绍

这个程序可以监控微信PC版的聊天窗口，当检测到新消息时自动发送随机表情包。程序使用了Windows UI Automation技术来监控窗口变化，确保准确检测新消息的到来。

## 系统要求

- Windows 操作系统
- Python 3.7 或更高版本
- 微信PC版

## 安装依赖

运行以下命令安装所需的Python包：

```bash
pip install pyautogui pywin32 comtypes psutil keyboard pynput
```

或者使用requirements.txt：

```bash
pip install -r requirements.txt
```

**重要**：新增了键盘监听库来解决微信窗口焦点问题：
- `keyboard` - 主要的热键监听库
- `pynput` - 备选的键盘监听库

## 使用步骤

### 1. 准备工作

1. **打开微信PC版**并登录
2. **打开要自动回复的聊天窗口**（个人聊天或群聊）
3. 确保聊天窗口是当前活跃窗口

### 2. 运行程序

```bash
python wechat_auto_emoji.py
```

### 3. 程序设置

程序启动后会显示命令菜单：

```
可用命令：
1. start - 开始监控
2. stop - 停止监控
3. test - 测试发送表情包
4. setup - 重新设置表情包位置
5. debug - 测试消息检测功能
6. cooldown - 设置发送冷却时间
7. status - 查看当前状态
8. quit - 退出程序
```

### 4. 首次设置（输入 `start`）

当你输入 `start` 命令时，程序会引导你完成以下设置：

#### 步骤1：设置表情包按钮位置
- 切换到微信窗口
- 将鼠标移动到聊天输入框右侧的**表情包图标**上
- 使用以下任一热键确认位置：
  - **F1** 键
  - **Ctrl+空格**
  - **Ctrl+Shift+C**

#### 步骤2：设置表情包面板区域
- 先手动点击表情包按钮，打开表情包面板
- 将鼠标移动到表情包面板的**左上角**，使用热键确认
- 将鼠标移动到表情包面板的**右下角**，使用热键确认

#### 步骤3：关闭表情包面板
- 手动关闭表情包面板（点击其他地方或按ESC）
- 使用热键确认完成

**重要提示**：使用热键确认位置可以解决微信窗口焦点切换的问题，确保程序能正确接收到确认信号。

### 5. 开始监控

设置完成后，程序会自动开始监控：
- 程序会检测聊天窗口的变化
- 当收到新消息时，会自动点击表情包按钮
- 随机选择一个表情包发送

## 程序特点

### 智能消息检测

程序使用多种方法检测新消息：

1. **UI Automation**：监控聊天区域的元素变化
2. **窗口标题监控**：检测窗口标题中的未读消息提示
3. **备选方案**：确保在不同环境下都能正常工作

### 改进的消息检测机制

**v1.2 重要更新**：解决了发送表情包后被误判为新消息的无限循环bug。

#### 问题背景
1. **v1.0问题**：仅依靠聊天区域中UI元素数量的变化来检测新消息，微信在收到新消息时可能会同时移除旧消息元素，导致总数量不变，从而无法检测到新消息。

2. **v1.1问题**：虽然解决了检测问题，但程序发送表情包后，表情包会出现在聊天区域中，被检测为"新消息"，从而触发新一轮的表情包发送，造成无限循环。

#### 解决方案（v1.2）
新版本使用智能防循环机制：

1. **发送冷却机制**：
   - 发送表情包后进入3秒冷却期
   - 冷却期内不检测新消息，避免误判自己发送的内容
   - 可通过 `cooldown` 命令自定义冷却时间

2. **消息来源识别**：
   - 分析消息元素的位置和属性
   - 识别自己发送的消息（通常在右侧）
   - 对自己发送的消息返回特殊标记，不触发回复

3. **智能基线更新**：
   - 冷却期结束后自动更新消息检测基线
   - 避免把冷却期内的消息当作新消息
   - 确保检测机制的持续准确性

4. **状态监控**：
   - 新增 `status` 命令查看程序运行状态
   - 实时显示冷却状态和剩余时间
   - 提供详细的调试信息

#### 使用建议
- 如果遇到消息检测问题，可以使用 `debug` 命令进行实时测试
- 观察控制台输出，了解检测机制的工作状态
- 在不同聊天场景下测试，确保检测的可靠性

### 安全功能

- **鼠标安全停止**：将鼠标移动到屏幕左上角可紧急停止程序
- **窗口检测**：自动检测微信窗口是否关闭
- **错误处理**：完善的异常处理机制

### 自适应性

- **动态位置获取**：每次启动都会重新获取微信窗口位置
- **用户自定义**：表情包按钮和面板位置由用户手动确认
- **随机选择**：随机选择表情包，避免重复

## 常用命令

- `start` - 开始监控（首次运行需要设置位置）
- `stop` - 停止监控
- `test` - 测试发送表情包功能
- `setup` - 重新设置表情包位置
- `debug` - 测试消息检测功能
- `cooldown` - 设置发送冷却时间（新增）
- `status` - 查看当前程序状态（新增）
- `quit` - 退出程序

## 注意事项

### 使用前准备

1. **确保微信已登录**并处于正常状态
2. **打开目标聊天窗口**，确保是你想要自动回复的对话
3. **不要在程序运行时移动微信窗口**，可能影响点击位置
4. **建议在测试环境中先试用**，避免误发消息

### 位置设置技巧

1. **表情包按钮**：通常在聊天输入框的右侧，是一个笑脸图标
2. **表情包面板**：设置区域时要包含所有可见的表情包
3. **避免边缘**：设置面板区域时留出一定边距，避免点击到边框

### 故障排除

1. **程序无法检测新消息**：
   - 使用 `debug` 命令测试检测机制是否正常工作
   - 检查微信窗口是否是当前活跃窗口
   - 尝试重新运行程序
   - 确保聊天窗口有实际的消息交互
   - 运行 `python test_message_detection.py` 进行专门测试

2. **表情包发送失败**：
   - 重新设置表情包按钮和面板位置
   - 确保表情包面板能正常打开
   - 检查微信是否有网络连接

3. **热键无法响应**：
   - 确保已安装 `keyboard` 或 `pynput` 库
   - 尝试以管理员权限运行程序
   - 检查其他程序是否占用了相同热键

4. **位置设置困难**：
   - 使用 `python test_hotkey.py` 测试热键功能
   - 尝试不同的热键组合（F1、Ctrl+空格等）
   - 确保在30秒内完成位置确认

5. **程序崩溃或异常**：
   - 查看终端输出的错误信息
   - 重启微信和程序
   - 确保所有依赖包已正确安装

6. **消息检测不准确或遗漏**：
   - 这是v1.1版本重点解决的问题
   - 使用 `debug` 命令观察检测过程
   - 查看控制台输出的消息签名变化
   - 如果仍有问题，可能需要调整检测间隔或算法参数
   - 在不同类型的聊天（个人/群聊）中测试检测效果

## 技术说明

### 核心技术

- **Windows UI Automation**：用于监控微信窗口的元素变化
- **PyAutoGUI**：用于模拟鼠标点击操作
- **Win32 API**：用于窗口管理和系统交互
- **多线程监控**：后台持续监控，不阻塞用户界面

### 监控原理

程序通过以下方式检测新消息：

1. **元素变化检测**：监控聊天区域的子元素数量变化
2. **窗口标题变化**：检测标题栏中的未读消息数量标识
3. **组合判断**：多种方法结合，提高检测准确性

## 免责声明

本程序仅供学习和研究使用。使用本程序时请遵守相关法律法规和平台规定。由于自动化操作可能违反某些服务条款，用户需自行承担使用风险。

## 版本信息

- 版本：1.2
- 开发日期：2025年7月5日
- 开发者：wsll

## 项目文件说明

### 主要文件

- **`wechat_auto_emoji.py`** - 主程序文件，包含所有核心功能
- **`requirements.txt`** - Python依赖包列表
- **`README.md`** - 详细使用说明文档
- **`start.bat`** - Windows批处理启动脚本

### 辅助文件

- **`test_setup.py`** - 程序测试脚本，检查依赖和功能
- **`test_message_detection.py`** - 消息检测机制测试脚本（新增）
- **`demo.py`** - 演示脚本，展示基本功能
- **`generate_uia_module.py`** - UI Automation模块生成脚本
- **`prompt.md`** - 项目需求文档

### 快速开始

1. **方法一**：双击 `start.bat`（Windows用户推荐）
2. **方法二**：运行 `python wechat_auto_emoji.py`
3. **测试模式**：运行 `python test_setup.py` 检查环境
4. **消息检测测试**：运行 `python test_message_detection.py` 测试新的检测机制
5. **演示模式**：运行 `python demo.py` 查看功能演示

## 故障排除指南

### 常见问题

**Q: 程序提示"未找到微信窗口"**
A: 确保微信PC版已打开并完全加载完成

**Q: UI Automation模块导入失败**
A: 运行 `python generate_uia_module.py` 生成必要模块

**Q: 表情包发送位置不准确**
A: 使用 `setup` 命令重新设置表情包按钮和面板位置

**Q: 程序无法检测新消息**
A: 尝试重启微信，确保聊天窗口是当前活跃窗口

### 调试模式

如果遇到问题，可以：

1. 运行 `python test_setup.py` 检查环境
2. 运行 `python demo.py` 测试基本功能
3. 查看终端输出的详细错误信息
4. 确保所有依赖包版本兼容

## 更新日志

### v1.2 (2025-07-05)
- **重要修复**：解决了发送表情包后被误判为新消息的无限循环bug
- **新增**：发送冷却机制，可自定义冷却时间
- **新增**：消息来源识别，区分自己和他人发送的消息
- **新增**：`cooldown` 命令，设置发送冷却时间
- **新增**：`status` 命令，查看程序运行状态
- **改进**：智能基线更新机制
- **改进**：更robust的防循环检测算法

### v1.1 (2025-07-05)
- **重要修复**：解决了仅依赖widget数量检测新消息的bug
- **新增**：基于消息内容签名的检测机制
- **新增**：消息历史追踪功能
- **新增**：多重验证机制，提高检测准确性
- **新增**：`debug` 命令，用于测试消息检测功能
- **改进**：更robust的新消息检测算法
- **改进**：详细的调试输出和状态监控

### v1.0 (2025-07-05)
- 初始版本发布
- 支持Windows UI Automation监控
- 实现随机表情包发送
- 添加多种消息检测方法
- 完善的错误处理和安全机制
