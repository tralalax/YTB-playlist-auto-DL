:: Check for Python Installation
python --version 3>NUL
if errorlevel 1 goto errorNoPython

pip install -r requirements.txt
python __main__.py

pause

:errorNoPython
echo.
echo Error^: Python not installed
echo You must have python to use this program
echo.
pause