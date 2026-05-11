@echo off
echo 📦 Setting up the Selenium Automation Framework...
echo.

:: Step 1: Install Python dependencies
echo 🐍 Installing Python libraries from requirements.txt...
pip install -r requirements.txt
echo.

:: Step 2: Check if Scoop is installed
where scoop >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo 🥄 Scoop not found. Installing Scoop...
    powershell -ExecutionPolicy RemoteSigned -Command "iwr -useb get.scoop.sh | iex"
) ELSE (
    echo ✅ Scoop is already installed.
)
echo.

:: Step 3: Check if Allure is installed
scoop list allure >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ✨ Installing Allure CLI via Scoop...
    scoop install allure
) ELSE (
    echo ✅ Allure is already installed.
)
echo.

:: Step 4: Confirm Allure installation
echo 🔍 Verifying Allure version...
allure --version
echo.

echo ✅ Setup complete!
echo You can now run tests using: python runner.py
echo.

:: Wait 3 seconds before auto-close
timeout /t 3 /nobreak >nul
