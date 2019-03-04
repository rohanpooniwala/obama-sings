import scrapers
import midi_to_audio
import midi_parser
import urllib 
from lyricsTS2filenamesTS import lyricsTS2filenamesTS
from videoStitcher import videoStitching, stitchFinal
from word_timestamps import extractWordTimestamps

if __name__ == "__main__":
    song = str(input("Enter Song to use:"))
    # song = "this is my life"

    file_name = scrapers.get_song_links(song)[:10]

    print("="*20)
    print("Select a song:")
    [print("{}. {}".format(file_name.index(_), urllib.parse.unquote(_[2].replace("+"," ")))) for _ in file_name]

    index = int(input("Index:"))
    # index = 0
    scrapers.download_kar(file_name[index])
    print("Downloaded:", file_name[index])
    print("="*20)

    midi_filename = "./temp/"+file_name[index][2]
    lyrics_filename = "./temp/"+file_name[index][2]+".txt"
    print("midi_filename", midi_filename)
    print("lyrics_filename", lyrics_filename)

    person = 'obama'

    # Load lyrics
    # start loop
    # while False:
    #     person = str(input("Enter person (query) to use:"))
    #     links = scrapers.google_scrap.search_link(person)[:10]
    # 
    #     print("="*20)
    #     print("Select a video:")
    #     [print("{}. {}".format(file_name.index(_), _[0])) for _ in links]
    #     
    #     index = int(input("Index:"))
    #     scrapers.download_video(links[index])
    #     print("Downloaded:", file_name[index])
    # extract words
    # crop?
    # repeat untill all the words are found
    # or crop here?


    # extractWordTimestamps("resources/"+person+"/"+links[index][0])

    # get timestamps from midi
    raw_timestamps = midi_parser.get_word_timestamp(midi_filename)
    # print(raw_timestamps)

    # match time stamps
    text_lyrics = midi_parser.load_lyrics(lyrics_filename)

    final_timestamps = midi_parser.complete_lyrics(raw_timestamps, text_lyrics)
    if len(final_timestamps) < len(text_lyrics):
        print("Couldn't extract lyrics!")
        exit()

    text_lyrics = [''.join(x for x in _ if x.isalpha() or x == "'") for _ in text_lyrics]
    print(text_lyrics)
    final_timestamps = [[_[0], ''.join(x for x in _[1] if x.isalpha() or x == "'")] for _ in final_timestamps]
    # print(final_timestamps)

    # Videos cropped !!
    filenamesTS = lyricsTS2filenamesTS(person, final_timestamps)
    videoStitching(filenamesTS, 'resources/' + person + "/")
    stitchFinal('resources/' + person + "/")

    # auto tune?
    # add bg
    midi_to_audio.midi_to_audio(midi_filename, './temp_mp3/'+file_name[index][2]+'.mp3')
    midi_to_audio.combine_audio("output.mp4", './temp_mp3/'+file_name[index][2] +'.mp3', 'ObamaSings_'+file_name[index][2]+'.mp4')




    # alignment_offset (use scraping youtube code to get instrumental)
