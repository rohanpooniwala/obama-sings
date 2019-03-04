import subprocess
import os
from revAiS2T import S2T
import time


def extractWordTimestamps(videoName):
    extractedAudioName = os.path.splitext(videoName)[0]+".wav"
    print("Creating .wav from video ", extractedAudioName)
    # command = "ffmpeg -i "+videoName+" -ab 160k -ac 2 -ar 44100 -vn "+extractedAudioName+" -y"
    command = "ffmpeg -i "+videoName+" -vn "+extractedAudioName+" -y"
    # check arguments and what they do

    subprocess.call(command, shell=False)
    # should check if filename not there yet, subprocess takes time

    time.sleep(2)

    S2T(extractedAudioName)


if __name__ == "__main__":
    person = "obama"
    speech_video = "obama.mp4"
    videoName = "resources/"+person+"/"+speech_video
    print("Reading video from ", videoName)
    extractWordTimestamps(videoName)
