import ffmpeg
import os
import subprocess
import json
import os.path
import datetime

offsetP = 0.00
offsetA = 0.00


# to access from dictionary dictname["key"]

def convertTime(t):
    return str(datetime.timedelta(seconds=t))


def convertBackTime(t):
    h, m, s = t.split(':')
    return float(h) * 3600 + float(m) * 60 + float(s)


def getVidLength(input_video):
    input_video = input_video.replace("'", '')
    result = subprocess.Popen('ffprobe -i '+ input_video +' -show_entries format=duration -v quiet -of csv="p=0"', stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = result.communicate()
    return float(output[0].decode().strip("\n"))

def video_crop(videoname, ts, end_ts, musicts, word):
    print("Cropping word ", word, " for " + musicts + " from ", videoname, ", time " + ts + " - " + end_ts)
    print('/'.join(videoname.split("/")[:-1]) + '/forStitching/' + os.path.splitext(os.path.basename(videoname))[0] + '_' + str(convertBackTime(ts)) + '_' + str(convertBackTime(end_ts)) + '_' + word + '.mp4')
    end_filename = '/'.join(videoname.split("/")[:-1]) + '/forStitching/' + os.path.splitext(os.path.basename(videoname))[0] + '_' + musicts + '_' + str(convertBackTime(ts)) + '_' + str(convertBackTime(end_ts)) + '_' + word + '.mp4'
    end_filename = end_filename.replace("'", '')
    if os.path.isfile(end_filename):
        return end_filename
    subprocess.run(
        'ffmpeg' + ' -i ' + videoname + ' -ss ' + convertTime(convertBackTime(ts) - offsetP) +
        ' -to ' + convertTime(convertBackTime(end_ts) + offsetA) + ' ' + end_filename + ' -y',
        shell=True)
    return end_filename


def video_crop2(videoname, ts, end_ts, musicts, word, end_filename):
    print('video_crop2', (videoname, ts, end_ts, musicts, word, end_filename))
    print("Cropping word ", word, " for " + musicts + " from ", videoname, ", time " + ts + " - " + end_ts)
    #######/ folder name / ##################  splittext(basename(videoname)) + _ + start + _ end _ word . mp4
#    end_filename = '/'.join(videoname.split("/")[:-1]) + os.path.splitext(os.path.basename(videoname))[0] + '_' + musicts + '_' + str(ts) + '_' + str(end_ts) + '_' + word + '.mp4'
    # end_filename = '/'.join(videoname.split("/")[:-1]) + os.path.splitext(os.path.basename(videoname))[0] + '_' + musicts + '_' + str(ts) + '_' + str(end_ts) + '_' + word + '.mp4'
    print(end_filename)
    end_filename = end_filename.replace("'", '')
    if os.path.isfile(end_filename):
        return end_filename
    subprocess.run(
        'ffmpeg' + ' -i ' + videoname + ' -ss ' + convertTime(float(ts) - offsetP) +
        ' -to ' + convertTime(float(end_ts) + offsetA) + ' ' + end_filename + ' -y',
        shell=True)
    return end_filename

if __name__ == "__main__":
    with open('obama.json') as f:
        data = json.load(f)

    path = './resources/speech_videos/obama/obama.mp4'
    path1 = '.resources/obama/'

    for keys in data:
        print(type(data[keys]))
        for segment_i in range(len(data[keys])):  # elements in array
            s = data[keys][segment_i]  #
            ss = s.split(" ~(**)~ ")
            if not (os.path.exists(path1 + keys)):
                os.mkdir(path1 + keys + '/')

            end_filename = path1 + keys + '/' + str(len(os.listdir(path1 + keys + '/')) + 1) + "_" + \
                           os.path.splitext(os.path.basename(ss[0]))[0].replace(" ", "_") + "_" + str(
                convertBackTime(ss[1])) + "_" + str(
                convertBackTime(ss[2])) + '.mp4'
            # end_filename = path1 + keys + '/' + 'as:2.mp4'

            # print('ffmpeg' + ' -ss ' + ss[1] + ' -i ' + path + '/' + ss[0] + ' -to ' + ss[
            #     2] + ' -c copy ' + end_filename)
            # subprocess.run('ffmpeg' + ' -i ' + path + '/' + ss[0] + ' -ss ' + convertTime(convertBackTime(ss[1])-offset) +
            #                ' -to ' + convertTime(convertBackTime(ss[2])+offset) + ' -async 1 -strict -2 ' + end_filename,
            #                shell=True)
            subprocess.run(
                'ffmpeg' + ' -i ' + path + '/' + ss[0] + ' -ss ' + convertTime(convertBackTime(ss[1]) - offsetP) +
                ' -to ' + convertTime(convertBackTime(ss[2]) + offsetA) + ' ' + end_filename,
                shell=True)
