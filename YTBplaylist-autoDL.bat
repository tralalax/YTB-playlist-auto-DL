:: Check for Python Installation
python --version 3>NUL
if errorlevel 1 goto errorNoPython

:: start the script (main.py)
cd YTB-playlist-Auto-DL

YTB-playlist-Auto-DL\YTBplDLvenv\Scripts\activate.bat && python __main__.py && deactivate

:: exit the script
exit /b

:: message for error if no python
:errorNoPython
echo.
echo Error^: Python not installed
echo You must have python to use this program
echo.
pause