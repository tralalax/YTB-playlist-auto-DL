:: Check for Python Installation
python --version 3>NUL
if errorlevel 1 goto errorNoPython


cd YTB-playlist-Auto-DL

YTB-playlist-Auto-DL\YTBplDLvenv\Scripts\activate.bat && pip install --upgrade pip && pip install -r requirements.txt && python __main__.py && deactivate


pause

:errorNoPython
echo.
echo Error^: Python not installed
echo You must have python to use this program
echo.
pause