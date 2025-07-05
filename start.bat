@echo off
echo ================================
echo 微信自动表情包回复器
echo ================================
echo.

echo 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python
    pause
    exit /b 1
)

echo 检查依赖包...
python -c "import pyautogui, pygetwindow, win32gui, comtypes, keyboard" >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    pip install pyautogui pywin32 comtypes psutil keyboard pynput
    echo.
)

echo 启动程序...
echo.
python wechat_auto_emoji.py

pause
