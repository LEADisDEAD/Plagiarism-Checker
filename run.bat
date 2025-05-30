@echo off
REM Start Flask backend silently (no window)
start /B python nlpmain.py

REM Wait for backend to initialize
timeout /t 3 >nul

REM Start React frontend (auto-opens browser)
cd plagiarism-frontend
start "" /B npm start

REM Keep this window open
pause