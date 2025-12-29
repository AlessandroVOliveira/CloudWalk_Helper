@echo off
REM CloudWalk Helper - One-Command Start Script for Windows
REM This script sets up and runs the CloudWalk Helper chatbot

echo.
echo  ========================================
echo   CloudWalk Helper - Quick Start
echo  ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker is not installed or not in PATH.
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Check if Docker is running
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker is not running.
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

REM Check if .env file exists, if not create from example
if not exist .env (
    echo [INFO] Creating .env file from template...
    if exist .env.example (
        copy .env.example .env >nul
        echo.
        echo [IMPORTANT] Please edit .env file and add your OpenRouter API key!
        echo Get a free key at: https://openrouter.ai
        echo.
        notepad .env
        echo Press any key after saving your API key...
        pause >nul
    ) else (
        echo [ERROR] .env.example not found!
        pause
        exit /b 1
    )
)

echo [INFO] Building and starting CloudWalk Helper...
echo This may take a few minutes on first run...
echo.

REM Build and run with Docker Compose
docker-compose up --build -d

if %ERRORLEVEL% EQU 0 (
    echo.
    echo  ========================================
    echo   CloudWalk Helper is running!
    echo  ========================================
    echo.
    echo   Open your browser at:
    echo   http://localhost:8501
    echo.
    echo   To stop: docker-compose down
    echo  ========================================
    echo.
    
    REM Open browser automatically
    timeout /t 3 >nul
    start http://localhost:8501
) else (
    echo [ERROR] Failed to start. Check the logs above.
    pause
)
