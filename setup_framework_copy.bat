@echo off
setlocal EnableDelayedExpansion

echo 📦 Setting up the Selenium Automation Framework...
echo.

:: Step 1: Install Python dependencies
echo 🐍 Installing Python libraries from requirements.txt...
pip install -r requirements.txt
echo.

:: Step 2: Check if PowerShell is available
where powershell >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ PowerShell not found. Please install or enable PowerShell and re-run this script.
    pause
    exit /b 1
)

:: Step 3: Check if Scoop is installed
where scoop >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo 🥄 Scoop not found. Installing Scoop...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "iwr -useb get.scoop.sh | iex"

    echo 🔁 Adding Scoop to current PATH...
    set "PATH=%PATH%;%USERPROFILE%\scoop\shims"
) ELSE (
    echo ✅ Scoop is already installed.
)
echo.

:: Step 4: Check if Allure is installed
echo 🔍 Checking for Allure...
powershell -NoProfile -ExecutionPolicy Bypass -Command "if (-not (scoop list | Out-String).Contains('allure')) { scoop install allure; Write-Host '✨ Allure installed.' } else { Write-Host '✅ Allure already installed.' }"
echo.

:: Step 5: Ensure scoop\shims in User PATH permanently
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$shimPath = '$env:USERPROFILE\scoop\shims';" ^
  "$userPath = [Environment]::GetEnvironmentVariable('PATH', 'User');" ^
  "if (-not ($userPath -split ';' | Where-Object { $_ -eq $shimPath })) {" ^
  "  [Environment]::SetEnvironmentVariable('PATH', $userPath + ';' + $shimPath, 'User');" ^
  "  Write-Host '🔧 Added scoop shim path to User PATH.'" ^
  "} else { Write-Host '✅ Scoop shim path already present in PATH.' }"

echo.

:: Step 6: Check Allure availability
echo 🔍 Verifying Allure installation...
where allure >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Allure not found. Please restart your terminal and try again.
    pause
    exit /b 1
) ELSE (
    allure --version
)

echo.
echo ✅ Setup complete!
echo You can now run tests using: python runner.py
timeout /t 10 /nobreak >nul
