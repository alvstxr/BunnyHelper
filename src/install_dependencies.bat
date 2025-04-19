@echo off
echo Installing required Python packages...
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
echo.
echo All dependencies installed!
pause
