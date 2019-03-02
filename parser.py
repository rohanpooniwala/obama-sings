import midi


def get_word_timestamp(midifile):
    pattern = midi.read_midifile(midifile)
    pattern.make_ticks_abs()
    first_event = None
    for _ in pattern[0]:
        if type(_) == midi.SetTempoEvent:
            first_event = _
            break
    time_per_tick = first_event.mpqn / (10**6 * pattern.resolution)
    timestamps = ([[_.tick * time_per_tick, _.text.replace("/", "").replace("\\", "").strip()] for _ in pattern[2] if type(_) == midi.TextMetaEvent and _.text[0] != "@"])
    return timestamps

def complete_lyrics(input_stamps, lyrics_path):
    lyrics = open(lyrics_path).read().split("\n")
    temp = []
    for _ in lyrics:
        temp += _.split(" ")
    lyrics = temp
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