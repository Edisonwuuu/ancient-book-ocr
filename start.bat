@echo off
chcp 65001 >nul
echo =========================================
echo 古籍OCR识别系统 - 启动脚本
echo =========================================

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo ✓ 检测到Python

REM 虚拟环境目录
set VENV_DIR=venv

REM 检查虚拟环境是否存在
if not exist "%VENV_DIR%" (
    echo.
    echo 未找到虚拟环境，正在创建...
    python -m venv %VENV_DIR%
    
    if errorlevel 1 (
        echo ✗ 虚拟环境创建失败
        pause
        exit /b 1
    )
    echo ✓ 虚拟环境创建成功
) else (
    echo ✓ 虚拟环境已存在
)

REM 激活虚拟环境
echo.
echo 正在激活虚拟环境...
call %VENV_DIR%\Scripts\activate.bat

if errorlevel 1 (
    echo ✗ 虚拟环境激活失败
    pause
    exit /b 1
)
echo ✓ 虚拟环境已激活

REM 检查是否需要安装依赖
echo.
if not exist "%VENV_DIR%\.dependencies_installed" (
    echo 正在安装项目依赖...
    echo 这可能需要几分钟时间，请耐心等待...
    
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
    if errorlevel 1 (
        echo ✗ 依赖安装失败
        echo 提示: 如果安装缓慢，可以使用国内镜像源：
        echo pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
        pause
        exit /b 1
    )
    echo ✓ 依赖安装成功
    type nul > %VENV_DIR%\.dependencies_installed
) else (
    echo ✓ 依赖已安装
)

REM 创建必要的目录
if not exist "uploads" mkdir uploads

REM 启动应用
echo.
echo =========================================
echo 正在启动应用...
echo 请访问: http://localhost:5000
echo 按 Ctrl+C 停止服务
echo =========================================
echo.

python app.py

pause