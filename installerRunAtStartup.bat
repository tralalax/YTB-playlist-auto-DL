:: Check for Python Installation
python --version 3>NUL
if errorlevel 1 goto errorNoPython

:: python is installed.
:: downloading file from github
cd %appdata%\Microsoft\Windows\Start Menu\Programs\Startup
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/tralalax/YTB-playlist-auto-DL/main/YTBplaylist-autoDL.bat', 'YTBplaylist-autoDL.bat')"

mkdir "YTB-playlist-Auto-DL"
cd %appdata%\Microsoft\Windows\Start Menu\Programs\Startup\YTB-playlist-Auto-DL

powershell -Command "(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/tralalax/YTB-playlist-auto-DL/main/requirements.txt', 'requirements.txt')"
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/tralalax/YTB-playlist-auto-DL/main/src/__main__.py', '__main__.py')"
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/tralalax/YTB-playlist-auto-DL/main/config.ini', 'config.ini')"

:: creating python venv
python -m venv YTBplDLvenv
YTBplDLvenv\Scripts\activate.bat

:: install dependencies
YTBplDLvenv install -r requirements.txt

:: exit the installer
::exit /b
pause

:errorNoPython
echo.
echo Error^: Python not installed
echo You must have python to use this program
echo.
pause