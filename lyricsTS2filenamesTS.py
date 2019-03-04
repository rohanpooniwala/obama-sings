import os
import random
from video_crop_cache import video_crop
import shutil

def lyricsTS2filenamesTS(person, lyrics_timestamps):
    filenamesTS = []
    for i in lyrics_timestamps:
        not_found = True
        ts = i[0]
        word = i[1]
        print("Finding ", ts, word)
        all_tsTxt = []
        for txts in os.listdir('resources/' + person + '/'):
            if txts.endswith('TimestampTxt.txt'):
                all_tsTxt.append('resources/' + person + '/' + txts)
        for Txt in all_tsTxt:
            if not not_found:
                break
            with open(Txt) as f:
                data_Txt = f.read().split("\n")[1:]
            for data_Txt_i in data_Txt:
                if word == data_Txt_i.split(",")[2]:
                    cropped_vid_ts = video_crop(Txt.replace('TimestampTxt.txt', '.mp4'), data_Txt_i.split(",")[0], data_Txt_i.split(",")[1], str(ts), word)
                    filenamesTS.append([ts, cropped_vid_ts])
                    not_found = False
                    print("Completed ", lyrics_timestamps.index(i), "/", len(lyrics_timestamps))
                    break
        if not_found:
            print("not found in txt, finding ", word, ' from cache')
            try:
                selected_vid = random.choice(os.listdir('resources/' + person + '/cache/' + word))
                temp = selected_vid.replace('.mp4', '').split('_')
                newfilename = 'resources/' + person + '/forStitching/{}_{}_{}_{}_{}.mp4'.format(temp[1], ts, temp[2], temp[3], word)
                shutil.copyfile('resources/' + person + '/cache/' + word + '/' + selected_vid, newfilename)
                filenamesTS.append([ts, newfilename])
                not_found = False
                print('found in cache')
            except Exception as e:
                print('Not found in cache\n', e)
                pass
        if not_found:
            print(word+" not found. Segmenting.")
            # cropped_vid_ts = segment_word()
            # filenamesTS.append([ts, cropped_vid_ts])

    with open("resources/"+person+'/musicTimeStamps.txt','w') as h:
        h.write("\n".join([','.join([str(__) for __ in _]) for _ in filenamesTS]))
    return filenamesTS


if __name__ == "__main__":
    a = [[35.61024864583333, "We're"], [36.14279364583333, 'talking'], [36.501521875, 'away'], [38.46158333333333, 'I'],
         [38.63540010416666, "don't"], [38.99043010416666, 'know'], [39.34915833333333, 'what'],
         [40.059218333333334, "I'm"], [40.4179465625, 'to'], [40.599159791666665, 'say'], [40.954189791666664, "I'll"],
         [41.30921979166666, 'say'], [41.84176479166666, 'it'], [42.02297802083333, 'anyway'], [44.15685625, "Today's"],
         [44.689401249999996, 'another'], [45.75818947916667, 'day'], [46.113219479166666, 'to'],
         [46.2981309375, 'find'], [46.6531609375, 'you'], [47.363220937499996, 'Shying'], [48.07697916666667, 'away'],
         [50.214555624999996, "I'll"], [50.38837239583333, 'be'], [50.569585624999995, 'coming'], [50.924615625, 'for'],
         [51.09843239583333, 'your'], [51.279645625, 'love'], [51.812190625, 'OK'], [52.70716208333333, 'Take'],
         [54.1309803125, 'on'], [55.55479854166666, 'me'], [56.978616770833334, 'Take'], [57.50746354166667, 'on'],
         [57.95494927083333, 'me'], [58.40613322916666, 'Take'], [59.82625322916667, 'me'], [61.25007145833333, 'on'],
         [62.67758791666667, 'Take'], [63.21383114583333, 'on'], [63.653920416666665, 'me'],
         [64.10140614583334, "I'll"], [65.525224375, 'be'], [66.94904260416666, 'gone'], [68.72789083333333, 'In'],
         [68.90910406249999, 'a'], [69.26783229166666, 'day'], [69.44164906249999, 'or'], [69.80407552083334, 'two'],
         [75.49565020833333, 'So'], [76.0318934375, 'needless'], [76.39062166666666, 'to'], [76.56813666666666, 'say'],
         [78.34698489583333, "I'm"], [78.52449989583333, 'odds'], [78.883228125, 'and'], [79.238258125, 'ends'],
         [79.95201635416666, 'But'], [80.30704635416666, "that's"], [80.48456135416666, 'me'],
         [80.83959135416666, 'that'], [81.19462135416666, 'stumbling'], [82.0895928125, 'away'],
         [84.04595604166666, 'Slowly'], [84.57850104166667, 'learning'], [85.29225927083333, 'that'],
         [85.64728927083333, 'life'], [86.0060175, 'is'], [86.1835325, 'OK'], [87.2486225, 'Say'],
         [87.78856395833333, 'after'], [88.13989572916667, 'me'], [90.0999571875, "It's"], [90.2774721875, 'no'],
         [90.4549871875, 'better'], [90.8100171875, 'to'], [90.99123041666667, 'be'], [91.1650471875, 'safe'],
         [91.34626041666667, 'than'], [91.70129041666667, 'sorry'], [92.59256364583332, 'Take'], [94.016381875, 'on'],
         [95.44020010416666, 'me'], [96.86401833333333, 'Take'], [97.40026156249999, 'on'], [97.84035083333333, 'me'],
         [98.29153479166666, 'Take'], [99.71535302083333, 'me'], [101.13547302083333, 'on'],
         [102.56298947916666, 'Take'], [103.09923270833333, 'on'], [103.53932197916666, 'me'],
         [103.98680770833333, "I'll"], [105.4106259375, 'be'], [106.83444416666666, 'gone'], [108.61329239583333, 'In'],
         [108.794505625, 'a'], [109.15323385416666, 'day'], [109.327050625, 'or'], [109.68947708333333, 'two'],
         [155.25535864583333, 'Oh'], [155.61038864583332, 'the'], [155.8026965625, 'things'],
         [156.16142479166666, 'you'], [156.33893979166666, 'say'], [158.11778802083333, 'Is'],
         [158.29530302083333, 'it'], [158.65403125, 'live'], [159.00906125, 'or'], [159.72281947916667, 'Just'],
         [160.07784947916667, 'to'], [160.25536447916667, 'play'], [160.61039447916667, 'my'],
         [160.96542447916667, 'worries'], [161.67918270833331, 'away'], [163.81675916666666, "You're"],
         [163.99427416666666, 'all'], [164.34930416666666, 'the'], [164.70803239583333, 'things'],
         [165.06306239583333, "I've"], [165.41809239583333, 'got'], [165.776820625, 'to'], [165.954335625, 'remember'],
         [167.019425625, 'Shying'], [167.73318385416667, 'away'], [169.87076031249998, "I'll"],
         [170.04827531249998, 'be'], [170.22579031249998, 'coming'], [170.58082031249998, 'for'],
         [170.76203354166665, 'you'], [170.93954854166665, 'anyway'], [172.36336677083332, 'Take'],
         [173.79088322916667, 'on'], [175.21470145833334, 'me'], [176.63851968749998, 'Take'],
         [177.17106468749998, 'on'], [177.6148521875, 'me'], [178.06603614583332, 'Take'], [179.489854375, 'me'],
         [180.91367260416666, 'on'], [182.33749083333333, 'Take'], [182.86633760416666, 'on'], [183.3175215625, 'me'],
         [183.76500729166665, "I'll"], [185.18512729166665, 'be'], [186.61264375, 'gone'], [188.39149197916666, 'In'],
         [188.56530874999999, 'a'], [188.92403697916666, 'day'], [189.10525020833333, 'or'],
         [189.10525020833333, 'two'], [189.4639784375, 'Take'], [190.8840984375, 'on'], [192.30791666666667, 'me'],
         [193.7317348958333, 'Take'], [194.2642798958333, 'on'], [194.80422135416666, 'me'],
         [195.15925135416666, 'Take'], [196.58306958333333, 'me'], [198.0068878125, 'on'], [199.4344042708333, 'Take'],
         [199.96325104166667, 'on'], [200.41073677083332, 'me'], [200.85822249999998, "I'll"],
         [202.28204072916665, 'be'], [203.70585895833332, 'gone'], [205.4847071875, 'In'], [205.65852395833332, 'a'],
         [206.0172521875, 'day'], [206.19846541666666, 'or'], [206.55719364583334, 'two']]
    print(lyricsTS2filenamesTS('obama', a))
