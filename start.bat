@echo off
REM ============================================================
REM  EDIT THE LINE BELOW FIRST: set NODE_DIR to the exact folder
REM  that contains node.exe (the one you copied from the address
REM  bar earlier). Example:
REM  set NODE_DIR=C:\Users\rhensh\OneDrive\Desktop\node-v24.21.0-win-x64\node-v24.21.0-win-x64
REM ============================================================
set NODE_DIR=PASTE_YOUR_NODE_FOLDER_PATH_HERE

set PATH=%NODE_DIR%;%PATH%

echo Using Node from: %NODE_DIR%
node -v
npm -v

if not exist node_modules (
  echo.
  echo Installing dependencies, this may take a minute...
  call npm install
)

echo.
echo Starting the app... a local address will appear below.
echo Open it in your browser. Press Ctrl+C here to stop the app.
echo.
call npm run dev

pause
