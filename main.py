import scrapers
import midi_to_audio
import midi_parser
import urllib 

if __name__ == "__main__":
    song = str(input("Enter Song to use:"))

    file_name = scrapers.get_song_links(song)[:10]

    print("="*20)
    print("Select a song:")
    [print("{}. {}".format(file_name.index(_), urllib.parse.unquote(_[2].replace("+"," ")))) for _ in file_name]

    index = int(input("Index:"))
    scrapers.download_kar(file_name[index])
    print("Downloaded:", file_name[index])
    print("="*20)

    midi_filename = "./temp/"+file_name[index][2]
    lyrics_filename = "./temp/"+file_name[index][2]+".txt"
    print("midi_filename", midi_filename)
    print("lyrics_filename", lyrics_filename)

    # exit()

    # Load lyrics
    # start loop
    while False:
        person = str(input("Enter person (query) to use:"))
        links = scrapers.google_scrap.search_link(person)[:10]

        print("="*20)
        print("Select a video:")
        [print("{}. {}".format(file_name.index(_), _[0])) for _ in links]
        
        index = int(input("Index:"))
        scrapers.download_video(links[index])
        print("Downloaded:", file_name[index])
    # extract words
    # crop?
    # repeat untill all the words are found
    # or crop here?

    # Videos cropped !!
    

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

    print(final_timestamps)

    stitch_videos(final_timestamps, file_name)
    
    # stitch videos according to timestamps
    # auto tune?
    # add bg
