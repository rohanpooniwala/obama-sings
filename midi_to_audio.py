import subprocess
# import librosa
import numpy as np

def midi_to_audio(midi_path, output_path):
    return subprocess.call(["timidity",midi_path,"-Ow","-o",output_path])

combine_command = '''ffmpeg -i {} -i {} -filter_complex [0:a][1:a]amerge=inputs=2[a] -map 0:v -map [a] -c:v copy -c:a libvorbis -ac 2 -shortest {} -y'''
combine_command_2 = '''ffmpeg -i {} -i {} -map 0:v -map 0:a -map 1:a -c:a aac {}'''
def combine_audio(video_path, audio_path, output_path):
#    return subprocess.call(["ffmpeg", "-i", video_path,"-i", audio_path, "-filter_complex", "[0:a][1:a]amerge=inputs=2[a]", '-map 0:v -map "[a]"', '-c:v', 'copy', '-c:a', 'libvorbis', '-ac', '2', '-shortest', output_path])
    return subprocess.call(combine_command.format(video_path, audio_path, output_path).split(' '))

def alignment_offset(midi_song, instrumental):
    y1 = librosa.load(midi_song)
    y2 = librosa.load(instrumental)
    beat_track_1 = librosa.frames_to_time(librosa.beat.beat_track(y1)[1])
    beat_track_2 = librosa.frames_to_time(librosa.beat.beat_track(y2)[1])
    i = min([len(beat_track_1), len(beat_track_1)])
    return np.average(beat_track_2[:i] - beat_track_1[:i])

