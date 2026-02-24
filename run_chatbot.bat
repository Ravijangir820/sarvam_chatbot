@echo off
REM Sarvam Chatbot Startup Script for Windows

echo.
echo ====================================
echo   Sarvam AI Chatbot
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version

REM Check if venv exists, if not create it
if not exist "venv\" (
    echo [2/4] Creating virtual environment...
    python -m venv venv
) else (
    echo [2/4] Virtual environment already exists
)

REM Activate virtual environment
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo [4/4] Installing dependencies...
pip install -q -r requirements.txt

echo.
echo ====================================
echo   Starting Sarvam AI Chatbot
echo ====================================
echo.
echo The chatbot will start on: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
