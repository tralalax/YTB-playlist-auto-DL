# YTB-playlist-auto-DL

YTB-playlist-auto-DL is a python script to automatically download the videos you add to a YouTube playlist.
It automatically checks if there are any new videos added to a playlist since the last time the script was run, if so, it downloads them.


### Current feature :
- Multiple playlists to check at once
- Choose between audio and video

### WIP feature :
- Logging system
- More choices for file extensions
- Sub-folder for each playlist

__Feel free to contribute or suggest features!__

## Installation :

### Run at computer startup
if you want to run this script automatically every time you start your computer. Download this [file.bat](https://github.com/tralalax/YTB-playlist-auto-DL/blob/main/installerRunAtStartup.bat) and run it, it will download the necessary file into the `startup` directory. Then you can delete the installer and check your file in `%appdata%\Microsoft\Windows\Startup Menu\Programs\Startup`.
Make sure to edit the configuration file once it is installed.

### Run manually
if you want to use this script manually, follow these steps :
1. download the [main.py](https://github.com/tralalax/YTB-playlist-auto-DL/blob/main/src/__main__.py) file and the [config.ini](https://github.com/tralalax/YTB-playlist-auto-DL/blob/main/config.ini) file in a folder
2. create a python venv with `python -m venv YTBplDLvenv` activate it with `YTBplDLvenv\Scripts\activate` then, install the requirements `pip install -r requirements.txt`
__OR__
you can simply install the requirements with `pip install -r requirements.txt`
3. run the `__main__.py`

### Configuration
After installing the script, you can edit the config.ini file. In the GENERAL section, you can change some options or leave the default value (each option has an explanation of what it does in the file).
Then add the URL of your playlist in the PLAYLIST section like this:

```ini
; the name of the Key dosen't matter, put whatever you want, the only important thing is the URL after the ' = ' sign
; make sure to insert the URL of the playlist between " and "
playlist1 = "https://www.youtube.com/playlist?list=PLHtyfDv32xnEBJiyxKaiDXGCaw974vJbu"
example2 = "https://www.youtube.com/watch?v=5W8vqbZhxSo&list=PLHtyfDv35xnEP5uM4N6Jy9sBtAKyPpUp7&index=3"
blablablabla = "https://www.youtube.com/watch?v=5W8vqbZhxSo&list=PsdGFEgsfDv35xnEP5uM4N6Jy9setAKyP58p7"
```

