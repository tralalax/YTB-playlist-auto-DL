import json
import io
import os
import logging
from configparser import ConfigParser

# import pytube
try:
    from pytube import YouTube
    from pytube import Playlist
except ImportError as err:
    logging.error("couldn't import module 'pytube' : "+err)
    exit(1)


def getVideoIDbyPlaylist():

    videoIdToDl = []
    videoIdtoRewrite = []
    videoIdList = []
    prevIdFileID = []

    # get all playlist in a list
    for selectedPlaylist in playlistConfig:

        # get playlist URl from the config file
        plUrl = playlistConfig[selectedPlaylist]
        # remove the " " 
        plUrl = plUrl[1:-1]
        # get playlist ID
        plId = plUrl.split('list=',1)[1]

        if os.path.isfile(os.path.join(os.getcwd(), 'old_id', plId+'.json')):
            logging.info("file : "+plId+" already exist, loading it")

            # load existing old_ID file
            with open(os.path.join(os.getcwd(), 'old_id', plId+'.json')) as prevIdjson:
                prevIdFile = json.load(prevIdjson)

                prevIdFileID = prevIdFile[plId]
                
                # create a playlist object
                pl = Playlist(plUrl)
                
                # get video ID in the request result
                for url, index in pl.video_urls:
                    url = str(url)

                    # get video ID from video URL
                    videoId = url.split('=',1)[1]

                    # compare videoId with the videoId in json file
                    if not videoId in prevIdFileID:
                        videoIdToDl.append(videoId)

                    # limit
                    if index == generalConfig['max_video_per_playlist']:
                        break
                    

                for i in prevIdFileID:
                    videoIdList.append(i)

                videoIdtoRewrite = videoIdToDl + videoIdList

                videoIdList.clear


            with open(os.path.join(os.getcwd(), 'old_id', plId+'.json'), mode='w') as curentJsonFile:
                
                # rewrite all the new ID
                videoIdJson = {
                    plId: videoIdtoRewrite
                }
                json.dump(videoIdJson, fp=curentJsonFile, indent=4)

            del videoIdtoRewrite
            del videoIdJson
            del prevIdFileID


        else:
            logging.info("file : "+plId+" dosen't exist, creating it")

            # no file found, create new one and write request result
            with open(os.path.join(os.getcwd(), 'old_id', plId+'.json'), mode='x') as curentJsonFile:
                
                # create a playlist object
                pl = Playlist(plUrl)

                print("plUrl : "+plUrl)
                print(pl)

                # get ID of every video
                for url in pl.video_urls:
                    url = str(url)

                    videoId = url.split('=',1)[1]

                    print(videoId)

                    videoIdList.append(videoId)
                    videoIdToDl.append(videoId)

                videoIdJson = {
                    plId: videoIdList
                }
                json.dump(videoIdJson, fp=curentJsonFile, indent=4)

                videoIdList.clear

    return videoIdToDl



plIdFromConfig = []

# del ID file that has been removed from config file
def delOldIdFile():

    # get playlist URl from the config file   
    for selectedPlaylist in playlistConfig:

        plUrl = playlistConfig[selectedPlaylist]
        # remove the " " 
        plUrl = plUrl[1:-1]
        # get playlist ID and store it in a list
        plIdFromConfig.append(plUrl.split('list=',1)[1])

    # check if the ID file is in the plIdFromConfig
    for extraFile in os.listdir(os.path.join(os.getcwd(),'old_id')):
        
        # remove the .json to the file
        extraFile = extraFile[:-5]

        if extraFile not in plIdFromConfig:

            # del the none used file
            try:
                os.remove(os.path.join(os.getcwd(),'old_id',extraFile+'.json'))
            except Exception as err:
                logging.error("something went wrong during the suppression of an old id file, feel free to report this issue on github" + err)

    plIdFromConfig.clear



# download a list of video ID
def downloadList(IdList):

    baseVideoUrl = "https://www.youtube.com/watch?v="

    # select one video ID from the list
    for video in IdList:

        print(baseVideoUrl+video)

        # create a YouTube object
        ytb = YouTube(baseVideoUrl+video)

        # create a stream with filter
        if generalConfig['file_format'] == 'audio':
            ytbVideo = ytb.streams.filter(only_audio=True).order_by('abr').desc().first()
            
        elif generalConfig['file_format'] == 'video':
            ytbVideo = ytb.streams.filter(only_video=True).order_by('resolution').desc().first()

        else:
            logging.error("file format incorect, please check config file")
            return

        # download the stream video
        if ytbVideo is not None:

            try:
                ytbVideo.download(output_path=downloadPath)
            except PermissionError as err:
                logging.error("raised permission error : " + err)
            except Exception as err:
                logging.fatal("something went wrong during the download, feel free to report this issue on github : " + err)



# MAIN
if __name__ == '__main__':

    # check config file
    try:
        config_object = ConfigParser(allow_no_value=True)
        config_object.read("./config.ini")

        playlistConfig = config_object['PLAYLIST']
        generalConfig = config_object['GENERAL']

    except Exception as err:
        logging.error('couldn\'t load config file')
        exit(1)


    # check old_id directory
    if os.path.isdir(os.path.join(os.getcwd(),'old_id')):
        pass

    else:
        logging.info('couldn\'t load old_id folder, creating a new one')
        try:
            os.makedirs(os.path.join(os.getcwd(),'old_id'))
            logging.info('successfully created old_id directory')
        except Exception as err:
            logging.error('couldn\'t create old_id directory')
            exit(1)


    # delete non used id file, if it's enable in the config
    if config_object.getboolean(section='GENERAL', option='del_non_used_id_file'):
        delOldIdFile()
        logging.info("cleared non used json file")


    # get downlaod path or create a folder Download
    if generalConfig['download_path'] == "" or generalConfig['download_path'] == " ":
        logging.info("no download path selected in cofig file, defaulting download location to the Download folder")
        
        if os.path.isdir(os.path.join(os.getcwd(),'Download')):
            downloadPath = os.path.join(os.getcwd(),'Download')

        else:
            logging.info('couldn\'t load Download folder, creating a new one')

            try:
                os.makedirs(os.path.join(os.getcwd(),'Download'))
                downloadPath = os.path.join(os.getcwd(),'Download')

                logging.info('successfully created Download directory')

            except Exception as err:
                logging.error('couldn\'t create Download directory')
                exit(1)

    else:
        # get the path set in config file
        downloadPath = os.path.abspath(os.path.join(os.getcwd(), generalConfig['download_path']))
        # prevent incorrectly decoded utf-8 tring (shit like Ã©)
        downloadPath = downloadPath.encode('iso-8859-1').decode('utf-8')


    # check for new video to download
    logging.info("checking for new video to download...")

    # check if there is playlist in PLAYSLIST section in config file
    playlistInConfig = False
    for i in playlistConfig:
        if not playlistInConfig:
            playlistInConfig = True

    if not playlistInConfig:
        logging.error("no playlist found in config file section PLAYLIST")
        exit(1)
    else:  
        videoIdToDl = getVideoIDbyPlaylist()


    # download video
    if videoIdToDl:
        logging.info("downloading new videos...")
        downloadList(IdList=videoIdToDl)

    else:
        logging.info("no new video was found, nothing was downloaded")

    # exit the script
    logging.info("exiting the script")
    del videoIdToDl
    exit(0)


# TODO logging in file / logging in console
# TODO sub-folder by playlist
