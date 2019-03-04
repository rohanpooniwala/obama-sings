from lyricsTS2filenamesTS import lyricsTS2filenamesTS
import datetime
from video_crop_cache import video_crop2
import subprocess
import os
import random
import shutil


def convertTime(t):
    t = float(t)
    return str(datetime.timedelta(seconds=t))


def convertBackTime(t):
    h, m, s = t.split(':')
    return float(h) * 3600 + float(m) * 60 + float(s)


def videoStitching(filenamesTS, folderPath):
    print('videoStitching', filenamesTS, folderPath)

    random_1st_idle = random.choice(os.listdir(folderPath + '/cache/IdleClips/'))
    print('Random Selected for first idle:', random_1st_idle)
    len_r = float(random_1st_idle.split('_')[3].replace(".mp4", "")) - float(random_1st_idle.split('_')[2])
    r = filenamesTS[0][0] / len_r
    # shutil.copyfile(folderPath+'/cache/IdleClips/'+random_1st_idle, folderPath+"forStitching/"+folderPath.split('/')[-2]+"_0.00_0_0_Idle.mp4")
    r1st_idle = folderPath + 'forStitching/first.mp4'
    print('Running',
          '\n\tffmpeg' + ' -i ' + folderPath + "cache/IdleClips/" + random_1st_idle + ' -vf ' + ' setpts=' + str(
              r) + '*PTS ' + r1st_idle)
    subprocess.run(
        'ffmpeg' + ' -i ' + folderPath + "cache/IdleClips/" + random_1st_idle + ' -vf ' + ' setpts=' + str(
            r) + '*PTS ' + r1st_idle + ' -y',
        shell=True)

    f = open(folderPath + "stitchVideo.txt", "w")
    print('Stitch video file path:', folderPath + "stitchVideo.txt")
    f.write('file ' + r1st_idle + "\n")

    #    def video_crop2(videoname, ts, end_ts, musicts, word, end_filename):
    video_crop2(folderPath + filenamesTS[0][1].split("/")[-1].split("_")[0] + '.mp4',
                filenamesTS[0][1].split("_")[2],
                filenamesTS[0][1].split("_")[3],
                filenamesTS[0][1].split("_")[1],
                filenamesTS[0][1].split("_")[4].replace(".mp4", ""),
                filenamesTS[0][1])

    f.write("file '" + filenamesTS[0][1].replace("'", "") + "'\n")
    prevts = filenamesTS[0][0]
    prevf = filenamesTS[0][1]

    for i in filenamesTS[1:]:
        ts_diff = i[0] - prevts

        #    def video_crop2(videoname, ts, end_ts, musicts, word, end_filename):
        video_crop2(folderPath + i[1].split("/")[-1].split("_")[0] + '.mp4',
                    i[1].split("_")[2],
                    i[1].split("_")[3],
                    i[1].split("_")[1],
                    i[1].split("_")[4].replace(".mp4", ""),
                    i[1])

        idle_filen = chooseIdleClip(ts_diff, prevf, folderPath)

        f.write("file '" + i[1].replace("'", "") + "'\n")
        f.write("file '" + idle_filen + "'\n")
        prevts = i[0]
        prevf = i[1]
    print(f)
    f.close()

def stitchFinal(folderPath):
    shutil.copyfile(folderPath+"stitchVideo.txt","./stitchVideo.txt")
    subprocess.run('ffmpeg -f concat -i stitchVideo.txt -c copy ./output.mp4 -y', shell=True)


def chooseIdleClip(ts_diff, prevf, folderPath):
    print("chooseIdleClip", ts_diff, prevf, folderPath)

    # resources/obama/forStitching/obama_35.61024864583333_293.73_293.93_We're.mp4
    fn = prevf.split('_')[0]  # resources/obama/forStitching/obama
    ts = prevf.split('_')[2]  # ts
    end_ts = prevf.split('_')[3]  # end_ts
    word = prevf.split('_')[4].split(".")[0]  # We're

    fni = folderPath + fn.split("/")[-1] + "TimestampTxt.txt"  # resources/obama/ + obama + TimestampTxt.txt
    with open(fni, "r") as g:
        idle_data = g.read().split("\n")

    # ts,end_ts,we're
    find_i = convertTime(ts) + "," + convertTime(end_ts) + ',' + word
    print("findi", find_i)

    try:
        j_index = idle_data.index(find_i)
    except:
        print("warning!", find_i)
        #### Shouldnt occur!!
        j_index = random.randint(1, len(idle_data))  # change this

    # Get next idle
    idleClip = []
    for _i in idle_data[j_index + 1:]:
        if _i.split(',')[-1] == 'IdleClips':
            idleClip = _i.split(",")
            break

    if len(idleClip) == 0:
        # Should'nt happen, handle properly
        return

    ts, end_ts = str(convertBackTime(idleClip[0])), str(convertBackTime(idleClip[1]))

    # folderPath + fn.split("/")[-1] + '.mp4'
    # resources/obama/forStitching/obama_35.61024864583333_293.73_293.93_We're.mp4
    idle_file_name = fn + '__' + ts + '_' + end_ts + '_Idle'
    temp_idle_file_name = idle_file_name + '_.mp4'

    #   def video_crop2(videoname, ts, end_ts, musicts, word, end_filename):
    video_crop2(folderPath + fn.split("/")[-1] + '.mp4',
                ts,
                end_ts,
                '',
                'Idle',
                temp_idle_file_name)
    r = ts_diff / (float(end_ts) - float(ts))

    subprocess.run(
        'ffmpeg' + ' -i ' + temp_idle_file_name + ' -vf ' + ' setpts=' + str(
            r) + '*PTS ' + idle_file_name + '__.mp4 -y',
        shell=True)

    null_command = '''ffmpeg -f lavfi -i anullsrc -i {} -shortest -c:v copy -c:a aac -map 0:a -map 1:v {} -y'''
    subprocess.run(
        null_command.format(idle_file_name+ '__.mp4', idle_file_name + '.mp4').split(' '),
        shell=True)
    return idle_file_name + '.mp4'


if __name__ == "__main__":
    # a = [[35.61024864583333, "We're"], [36.14279364583333, 'talking'], [36.501521875, 'away'], [38.46158333333333, 'I'],
    #      [38.63540010416666, "don't"], [38.99043010416666, 'know'], [39.34915833333333, 'what']]
    # filenamesTS = lyricsTS2filenamesTS('obama', a)
    person = "obama"
    folderPath = 'resources/' + person + "/"
    filenamesTS = [[35.61024864583333, "resources/obama/forStitching/obama_35.61024864583333_293.73_293.93_We're.mp4"],
                   [36.14279364583333,
                    'resources/obama/forStitching/obama_36.14279364583333_830.07_830.46_talking.mp4'],
                   [36.501521875, 'resources/obama/forStitching/obama_36.501521875_144.7_144.91_away.mp4'],
                   [38.46158333333333, 'resources/obama/forStitching/obama_38.46158333333333_147.18_147.27_I.mp4'],
                   [38.63540010416666,
                    "resources/obama/forStitching/obama_38.63540010416666_137.74_137.92000000000002_don't.mp4"],
                   [38.99043010416666, 'resources/obama/forStitching/obama_38.99043010416666_147.27_147.87_know.mp4'],
                   [39.34915833333333, 'resources/obama/forStitching/obama_39.34915833333333_238.27_238.45_what.mp4']]
    videoStitching(filenamesTS, folderPath)
    stitchFinal(folderPath)
