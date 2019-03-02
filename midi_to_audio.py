import subprocess

def midi_to_audio(midi_path, output_path):
    return subprocess.call(["timidity",midi_path,"-Ow","-o",output_path])

def combine_audio(video_path, audio_path, output_path):
    return subprocess.call(["ffmpeg", "-i", video_path,"-i", audio_path, "-filter_complex", "[0:a][1:a]amerge=inputs=2[a]", '-map 0:v -map "[a]"', '-c:v', 'copy', '-c:a', 'libvorbis', '-ac', '2', '-shortest', output_path])
