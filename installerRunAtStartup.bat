:: Check for Python Installation
python --version 3>NUL
if errorlevel 1 goto errorNoPython

:: python is installed.
:: downloading file from github
cd %appdata%\Microsoft\Windows\Start Menu\Programs\Startup
mkdir "YTB-playlist-Auto-DL"
cd %appdata%\Microsoft\Windows\Start Menu\Programs\Startup\YTB-playlist-Auto-DL

python -m venv YTBplDLvenv
nomdelenvironement\Scripts\activate.bat

powershell -Command "(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/tralalax/YTB-playlist-auto-DL/main/src/__main__.py', '__main__.py')"
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/tralalax/YTB-playlist-auto-DL/main/src/__main__.py', '__main__.py')"
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/tralalax/YTB-playlist-auto-DL/main/config.ini', 'config.ini')"

:: exit the installer
::exit /b
pause

:errorNoPython
echo.
echo Error^: Python not installed
echo You must have python to use this program
echo.
pause