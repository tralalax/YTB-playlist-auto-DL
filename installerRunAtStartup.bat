:: Check for Python Installation
python --version 3>NUL
if errorlevel 1 goto errorNoPython

:: downloading file from github in Start directory
cd %appdata%\Microsoft\Windows\Start Menu\Programs\Startup
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/tralalax/YTB-playlist-auto-DL/main/YTBplaylist-autoDL.bat', 'YTBplaylist-autoDL.bat')"

mkdir "YTB-playlist-Auto-DL"
cd %appdata%\Microsoft\Windows\Start Menu\Programs\Startup\YTB-playlist-Auto-DL

powershell -Command "(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/tralalax/YTB-playlist-auto-DL/main/requirements.txt', 'requirements.txt')"
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/tralalax/YTB-playlist-auto-DL/main/src/__main__.py', '__main__.py')"
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/tralalax/YTB-playlist-auto-DL/main/config.ini', 'config.ini')"

:: creating python venv
python -m venv YTBplDLvenv

cd YTB-playlist-Auto-DL

:: install dependencies
YTB-playlist-Auto-DL\YTBplDLvenv\Scripts\activate.bat && pip install --upgrade pip && pip install -r requirements.txt && deactivate

echo Installation finished
echo config file is in %appdata%\Microsoft\Windows\Start Menu\Programs\Startup\YTB-playlist-Auto-DL
echo check github for more info : https://github.com/tralalax/YTB-playlist-auto-DL

:: exit the installer
exit /b

:: message for error if no python
:errorNoPython
echo.
echo Error^: Python not installed
echo You must have python to use this program
echo.
pause