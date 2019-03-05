import midi
# import midi_to_audio

def load_lyrics(lyrics_path):
    lyrics = open(lyrics_path).read().split("\n")
    temp = []
    for _ in lyrics:
        temp += _.split(" ")
    return temp



    # timestamps = ([[_.tick * time_per_tick, _.text.replace("/", "").replace("\\", "").strip()] for _ in pattern[2] if type(_) == midi.TextMetaEvent and _.text[0] != "@"])
    return timestamps

def complete_lyrics(input_stamps, lyrics):
    #print(lyrics)
    temp_word = []
    words_list = []
    index = 0
    while len(input_stamps) != 0:
        if len(temp_word) == 0:
            temp_word = input_stamps.pop(0)
        else:
            temp_word[1] += input_stamps.pop(0)[1]
        
        if temp_word[1] == lyrics[index]:
            words_list.append(temp_word)
            temp_word = []
            index += 1
    #words_list.append(temp_word)
    return words_list

def get_vocals(midifile):
    pattern = midi.read_midifile(midifile)
    temp = [_ for _ in pattern if midi.TrackNameEvent in [type(i) for i in _]]
    temp1 = []
    for _ in temp:
        for __ in _:
            if type(__)==midi.TrackNameEvent:
                temp1.append(__)
    pattern.make_ticks_rel()

    new_pattern = midi.Pattern(resolution=pattern.resolution)
    new_pattern.append(pattern[0])
    new_pattern.append(pattern[1])
    new_pattern.append(pattern[2])
    new_pattern.append(pattern[3])
    fname = midifile.split("/")[-1]
    midi.write_midifile("./temp_midi/" + fname, new_pattern)
    
    midi_to_audio.midi_to_audio("./temp_midi/" + fname, "./temp_mp3/" + fname + ".mp3")
    return fname


if __name__== "__main__":
    from pprint import pprint
    midifile = "./temp/Nirvana+-+Smells+Like+Teen+Spirit.kar"
    print(get_vocals(midifile))
    exit()

    pattern = midi.read_midifile(midifile)
    temp = [_ for _ in pattern if midi.TrackNameEvent in [type(i) for i in _]]
    temp1 = []
    for _ in temp:
        for __ in _:
            if type(__)==midi.TrackNameEvent:
                temp1.append(__)
    pattern.make_ticks_rel()

    new_pattern = midi.Pattern(resolution=pattern.resolution)
    new_pattern.append(pattern[0])
    new_pattern.append(pattern[1])
    new_pattern.append(pattern[2])
    new_pattern.append(pattern[3])
    midi.write_midifile("example.kar", new_pattern)
    # pprint(pattern[0])
    # print(len(pattern), len(temp))
    
    # [print("b", _[0]) for _ in pattern]    
    # [print("a", _[0]) for _ in temp]    
    
    # pprint(temp1)

    # new_pattern.append()
    # new_pattern.append(pattern[2])
    # new_pattern.append(pattern[4])

    # pattern = midi.read_midifile("./example.kar")
    # print(pattern)
    # [print("b", _[0]) for _ in pattern[1]]    
    # pprint(pattern)


    # D:\Anaconda\lib\site-packages\midi-0.2.3-py3.6.egg\midi\
    
