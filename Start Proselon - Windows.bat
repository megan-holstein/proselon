@echo off
setlocal
cd /d "%~dp0"

rem Detect which engines are installed.
set "HAVE_CLAUDE="
set "CLAUDE_CMD=claude"
where claude >nul 2>nul && set "HAVE_CLAUDE=1"
if not defined HAVE_CLAUDE if exist "%USERPROFILE%\.local\bin\claude.exe" (
    set "HAVE_CLAUDE=1"
    set "CLAUDE_CMD=%USERPROFILE%\.local\bin\claude.exe"
)
set "HAVE_CODEX="
where codex >nul 2>nul && set "HAVE_CODEX=1"

rem Pick the engine from what's installed. Only ask when it's ambiguous:
rem both installed (which one this time?) or neither (which subscription to set up?).
set "ENGINE="
if defined HAVE_CLAUDE if defined HAVE_CODEX goto askboth
if defined HAVE_CLAUDE ( set "ENGINE=claude" & goto gitcheck )
if defined HAVE_CODEX ( set "ENGINE=chatgpt" & goto gitcheck )
goto askinstall

:askboth
echo Welcome to Proselon.
echo.
echo You have both Claude and ChatGPT set up. Which should I write with today?
echo.
echo   1. Claude
echo   2. ChatGPT
echo.
set "CHOICE="
set /p CHOICE=Type 1 or 2 and press Enter:
if "%CHOICE%"=="2" (set "ENGINE=chatgpt") else (set "ENGINE=claude")
goto gitcheck

:askinstall
echo Welcome to Proselon.
echo.
echo Proselon writes using an AI subscription you already have. Which one do you use?
echo.
echo   1. Claude    ^(any paid plan^)
echo   2. ChatGPT   ^(Plus or Pro^)
echo.
set "CHOICE="
set /p CHOICE=Type 1 or 2 and press Enter:
if "%CHOICE%"=="1" set "ENGINE=claude"
if "%CHOICE%"=="2" set "ENGINE=chatgpt"
if "%ENGINE%"=="" (
    echo.
    echo Proselon currently works with a Claude or a ChatGPT subscription. Once you
    echo have one, double-click this launcher again.
    echo.
    pause
    exit /b 0
)

:gitcheck
where git >nul 2>nul
if errorlevel 1 (
    echo Your project is always saved right here on your computer, exactly where
    echo you left it.
    echo.
    echo One optional extra: Proselon can also keep a history of past versions, so
    echo you can go back in time to earlier drafts. To add that anytime, install the
    echo free Git tool from https://git-scm.com/download/win ^(the standard options
    echo are fine^) and relaunch.
    echo.
    echo Press any key to continue without it for now...
    pause >nul
    echo.
)

rem Obsidian is the optional window for reading and editing your book. If it's
rem installed, open this folder in it; otherwise stay quiet (see README.md).
set "OBSIDIAN_EXE="
if exist "%LOCALAPPDATA%\Obsidian\Obsidian.exe" set "OBSIDIAN_EXE=%LOCALAPPDATA%\Obsidian\Obsidian.exe"
if exist "%LOCALAPPDATA%\Programs\Obsidian\Obsidian.exe" set "OBSIDIAN_EXE=%LOCALAPPDATA%\Programs\Obsidian\Obsidian.exe"
if not "%OBSIDIAN_EXE%"=="" powershell -NoProfile -Command "Start-Process ('obsidian://open?path=' + [uri]::EscapeDataString((Get-Location).Path))"

if "%ENGINE%"=="chatgpt" goto chatgpt

rem ----- Claude -----
where claude >nul 2>nul
if errorlevel 1 (
    if exist "%USERPROFILE%\.local\bin\claude.exe" (
        set "CLAUDE_CMD=%USERPROFILE%\.local\bin\claude.exe"
    ) else (
        echo Proselon writes with Claude Code, which isn't installed yet.
        echo It's free to install and uses the Claude subscription you already have.
        echo.
        echo Press any key to install Claude Code now, or close this window to cancel.
        pause >nul
        powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://claude.ai/install.ps1 | iex"
        if exist "%USERPROFILE%\.local\bin\claude.exe" set "CLAUDE_CMD=%USERPROFILE%\.local\bin\claude.exe"
    )
)

if not "%CLAUDE_CMD%"=="claude" goto launchclaude
where claude >nul 2>nul
if errorlevel 1 (
    echo.
    echo The install didn't finish. See "README.md" in this folder for help.
    pause
    exit /b 1
)

:launchclaude
echo.
echo Starting Proselon...
echo If you're asked to log in, choose "Claude account" and use your normal Claude login.
echo.
"%CLAUDE_CMD%"
pause
exit /b 0

:chatgpt
where codex >nul 2>nul
if errorlevel 1 (
    where npm >nul 2>nul
    if errorlevel 1 (
        echo Proselon writes with Codex -- the part of ChatGPT that can work with the
        echo files on your computer. It isn't installed yet.
        echo.
        echo First install Node.js from https://nodejs.org ^(choose the LTS version^),
        echo then double-click this launcher again.
        echo.
        pause
        exit /b 1
    )
    echo Proselon writes with Codex -- the part of ChatGPT that can work with the
    echo files on your computer. It isn't installed yet. It's free, and it runs on
    echo the ChatGPT subscription you already have.
    echo.
    echo Press any key to install it now, or close this window to cancel.
    pause >nul
    call npm install -g @openai/codex
    where codex >nul 2>nul
    if errorlevel 1 (
        echo.
        echo The install didn't finish. See "README.md" in this folder for help.
        pause
        exit /b 1
    )
)

echo.
echo Starting Proselon...
echo If you're asked to log in, choose "Sign in with ChatGPT" and use your normal ChatGPT login.
echo.
codex
pause
exit /b 0
