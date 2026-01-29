@echo off
set PATH=D:\Github\Git\cmd;%PATH%
echo ==========================================
echo      Auto-Eval Pro GitHub Uploader
echo ==========================================
echo.

echo [1/7] Initializing Git repository...
git init
if %errorlevel% neq 0 goto Error

echo [2/7] Configuring user info...
git config user.name "mingqu72"
git config user.email "2199853163@qq.com"

echo [3/7] Adding files...
git add .

echo [4/7] Committing files...
git commit -m "Initial release of One-Stop Eval Tool"

echo [5/7] Renaming branch to main...
git branch -M main

echo [6/7] Adding remote origin...
git remote remove origin 2>nul
git remote add origin https://github.com/mingqu72/Futao-Workshop.git

echo [7/7] Pushing to GitHub...
echo.
echo ========================================================
echo NOTE: A popup window will likely appear.
echo Please select "Sign in with your browser" or "Token".
echo If you choose Browser, you can use your normal password!
echo ========================================================
echo.
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo      SUCCESS! Upload Completed.
    echo ==========================================
) else (
    :Error
    echo.
    echo ==========================================
    echo      ERROR: Upload Failed.
    echo      Please try running this script again.
    echo ==========================================
)
pause
