@echo off
setlocal

:: --- 设置 Git 路径 (和之前一样) ---
set "GIT_PATH=D:\Github\Git\cmd"
set "PATH=%GIT_PATH%;%PATH%"

echo ==========================================
echo      Auto-Eval Pro - Update Sync
echo ==========================================
echo.

:: --- 1. 添加变动 ---
echo [1/3] Scanning for changes...
git add .

:: --- 2. 提交变动 ---
echo [2/3] Committing changes...
set /p msg="Please enter commit message (Press Enter for 'Update'): "
if "%msg%"=="" set msg=Update
git commit -m "%msg%"

:: --- 3. 推送到 GitHub ---
echo [3/3] Pushing to GitHub...
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Your changes are now on GitHub!
) else (
    echo.
    echo [INFO] Nothing to push or an error occurred.
)

echo.
pause
