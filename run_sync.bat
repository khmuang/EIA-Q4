@echo off
setlocal
cd /d "%~dp0"

echo ===========================================
echo       EIA Q4 SYNC TOOL (ONEDRIVE 2026)
echo ===========================================

:: [1/3] Run Data Extraction & Sync from OneDrive
echo [1/3] Extracting Data from OneDrive Q4...
python update_dashboard.py

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Data Extraction Failed.
    pause
    exit /b 1
)

:: [2/3] Generate Static Tables
echo [2/3] Generating Detailed Static Tables...
python gen_tables.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Table Generation Failed.
    pause
    exit /b 1
)

:: [3/3] Push Updates to GitHub Repository (EIA-Q4)
echo [3/3] Syncing to GitHub (EIA-Q4)...
git add index.html data.js update_dashboard.py gen_tables.py run_sync.bat README.md .gitignore changelogs/
git commit -m "Auto Sync: EIA Q4 Dashboard Update (%date% %time%)"
git push origin main
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Git Push encountered an issue. Please check network/remote status.
)

echo ===========================================
echo       EIA Q4 DASHBOARD SYNC COMPLETE!
echo       URL: https://khmuang.github.io/EIA-Q4/
echo ===========================================
pause
