import moviepy.editor as mp


clip = mp.VideoFileClip("Recording.m4a").subclip(0,20)
clip.audio.write_audiofile("rec.mp3")
