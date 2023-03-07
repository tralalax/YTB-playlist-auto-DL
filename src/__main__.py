from pytube import YouTube
from pytube import Playlist
import json
import io
import os
import logging
from configparser import ConfigParser


# load config
def loadConfig():
    try:
        config_object = ConfigParser()
        config_object.read("./config.ini")

        return config_object

    except Exception as err:
        logging.error('couldn\'t load config file file')
        return None

config_object = loadConfig()

if config_object is not None:
    playlistConfig = config_object['PLAYLIST']
    generalConfig = config_object['GENERAL']


def getVideoIDbyPlaylist():

    # get all playlist in a list
    for selectedPlaylist in playlistConfig:

        videoIdtoRewrite = []
        videoIdList = []
        videoIdToDl = []
        prevIdFileID = []

        # get playlist URl from the config file
        plUrl = playlistConfig[selectedPlaylist]
        # remove the " " 
        plUrl = plUrl[1:-1]
        # get playlist ID
        plId = plUrl.split('list=',1)[1]

        if os.path.isfile(os.path.join(os.getcwd(), 'old_id', plId+'.json')):
            print("FILE ALREADY EXIST FOR : "+plId)

            # load existing old_ID file
            with open(os.path.join(os.getcwd(), 'old_id', plId+'.json')) as prevIdjson:
                prevIdFile = json.load(prevIdjson)

                prevIdFileID = prevIdFile[plId]
                
                # create a playlist object
                pl = Playlist(plUrl)
                
                # get video ID in the request result
                for url in pl.video_urls:
                    url = str(url)

                    videoId = url.split('=',1)[1]

                    if videoId in prevIdFileID:
                        pass
                    else:
                        videoIdToDl.append(videoId)

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
            print("CREATING NEW FILE FOR : "+plId)

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

    print(plIdFromConfig)

    # check if the ID file is in the plIdFromConfig
    for extraFile in os.listdir(os.path.join(os.getcwd()+'/old_id')):
        
        # remove the .json to the file
        extraFile = extraFile[:-5]

        if extraFile not in plIdFromConfig:

            # del the none used file
            os.remove(os.path.join(os.getcwd()+'/old_id'+extraFile+'.json'))

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
            ytbVideo.download(output_path=os.getcwd())
        
        print(ytbVideo)


delOldIdFile()
#getVideoIDbyPlaylist()
#downloadList(["80MGUrKXr58"])

#https://www.youtube.com/watch?v=80MGUrKXr58


# TODO del json file if playlist is removed from config