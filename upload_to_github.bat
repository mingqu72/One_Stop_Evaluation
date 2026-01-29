@echo off
setlocal

:: --- 1. 设置 Git 路径 ---
set "GIT_PATH=D:\Github\Git\cmd"
set "PATH=%GIT_PATH%;%PATH%"

:: --- 2. 界面初始化 ---
cls
echo ==========================================
echo      Auto-Eval Pro GitHub Uploader
echo      (Reset & Diagnostic Mode)
echo ==========================================
echo.

:: --- 3. 检查 Git 是否可用 ---
echo [1/6] Checking Git environment...
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Git command not found! 
    echo Please check if "D:\Github\Git\cmd" is correct.
    echo.
    pause
    exit /b
)
git --version
echo.

:: --- 4. 初始化与配置 ---
echo [2/6] Configuring repository...
if not exist ".git" git init
git config user.name "mingqu72"
git config user.email "2199853163@qq.com"

:: --- 5. 提交代码 ---
echo [3/6] Adding and committing files...
git add .
git commit -m "Release via diagnostic script" >nul 2>nul

:: --- 6. 设置远程 ---
echo [4/6] Setting remote origin...
git remote remove origin >nul 2>nul
git remote add origin https://github.com/mingqu72/Futao-Workshop.git
git branch -M main

:: --- 7. 推送 (核心步骤) ---
echo [5/6] Preparing to push...
echo.
echo ========================================================
echo [IMPORTANT INSTRUCTIONS]
echo 1. A login window SHOULD appear shortly.
echo 2. If it's a browser window and it's blank -> Close it.
echo 3. If it's a console prompt -> Type your Token.
echo ========================================================
echo.
echo Executing git push...
git push -u origin main

:: --- 8. 结果判定 ---
if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Upload successfully completed!
) else (
    echo.
    echo [FAILED] Git push failed. Please check the error message above.
)

echo.
echo Press any key to exit...
pause
