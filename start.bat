@echo off
REM Quick start script for AI Translation Assistant (Windows)

echo ========================================
echo AI Translation Assistant - Quick Start
echo ========================================
echo.

REM Check if .env exists in backend
if not exist backend\.env (
    echo [WARNING] backend\.env not found!
    echo Please copy backend\.env.example to backend\.env and configure your API keys.
    echo.
    pause
    exit /b 1
)

echo [1/3] Starting backend server...
echo.

set "PYTHON_EXE=%~dp0myenv\Scripts\python.exe"
if not exist "%PYTHON_EXE%" (
    echo [WARNING] myenv not found. Falling back to system Python.
    echo           Consider running: myenv\\Scripts\\activate
    echo.
    set "PYTHON_EXE=python"
)

cd backend
start cmd /k "%PYTHON_EXE% app.py"
cd ..

echo [2/3] Backend started at http://localhost:8000
echo.

timeout /t 3 /nobreak > nul

echo [3/3] You can now start the Flutter app:
echo    cd flutter_app
echo    flutter run
echo.

echo ========================================
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo ========================================
echo.

pause
