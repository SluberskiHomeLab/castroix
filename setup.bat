@echo off
REM Castroix Setup Script for Windows
REM Automatically detects Node.js and NPM, and sets up the application

setlocal enabledelayedexpansion

echo ========================================
echo       Castroix Setup Script
echo ========================================
echo.

REM Detect Windows
echo [INFO] Detected: Windows
echo.

REM Check if Node.js is installed
echo [INFO] Checking for Node.js installation...
where node >nul 2>nul
if %errorlevel% equ 0 (
    for /f "delims=" %%i in ('node --version') do set NODE_VERSION=%%i
    echo [SUCCESS] Node.js is installed: !NODE_VERSION!
    set NODE_INSTALLED=1
) else (
    echo [WARNING] Node.js is not installed.
    set NODE_INSTALLED=0
)
echo.

REM Check if npm is installed
echo [INFO] Checking for npm installation...
where npm >nul 2>nul
if %errorlevel% equ 0 (
    for /f "delims=" %%i in ('npm --version') do set NPM_VERSION=%%i
    echo [SUCCESS] npm is installed: !NPM_VERSION!
    set NPM_INSTALLED=1
) else (
    echo [WARNING] npm is not installed.
    set NPM_INSTALLED=0
)
echo.

REM Install Node.js if not installed
if !NODE_INSTALLED! equ 0 (
    echo [WARNING] Node.js is required to run Castroix.
    echo.
    echo Please download and install Node.js from: https://nodejs.org/
    echo.
    echo After installation:
    echo   1. Restart your computer or open a new command prompt
    echo   2. Run this setup script again
    echo.
    set /p OPEN_BROWSER="Would you like to open the Node.js download page now? (Y/N): "
    if /i "!OPEN_BROWSER!"=="Y" (
        start https://nodejs.org/
    )
    echo.
    echo [INFO] Exiting setup. Please install Node.js and run this script again.
    pause
    exit /b 1
)

if !NPM_INSTALLED! equ 0 (
    echo [ERROR] npm should be installed with Node.js but was not found.
    echo Please reinstall Node.js from: https://nodejs.org/
    pause
    exit /b 1
)

REM Install dependencies
echo [INFO] Installing npm dependencies...
if exist package.json (
    npm install
    if %errorlevel% equ 0 (
        echo [SUCCESS] Dependencies installed successfully!
    ) else (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
) else (
    echo [ERROR] package.json not found. Are you in the correct directory?
    pause
    exit /b 1
)
echo.

REM Setup configuration
if not exist config.json (
    if exist config.json.sample (
        echo [INFO] Creating config.json from config.json.sample...
        copy config.json.sample config.json >nul
        echo [SUCCESS] config.json created successfully!
    ) else (
        echo [WARNING] config.json.sample not found. You may need to create config.json manually.
    )
) else (
    echo [INFO] config.json already exists, skipping creation.
)
echo.

echo [SUCCESS] Setup completed successfully!
echo.

REM Ask to launch
set /p LAUNCH="Would you like to launch Castroix now? (Y/N): "
if /i "!LAUNCH!"=="Y" (
    echo [INFO] Launching Castroix...
    npm start
) else (
    echo [INFO] You can launch Castroix later by running: npm start
)

echo.
pause
