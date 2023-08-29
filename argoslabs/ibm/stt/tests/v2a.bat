
REM ffmpeg.exe -i Rec.m4a -vn -f mp3 -ab 19200 Rec.mp3
REM ffmpeg.exe -i Rec2.m4a -vn -f mp3 -ab 19200 Rec2.mp3

ffmpeg.exe -i Rec.m4a -vn -acodec pcm_s16le -ac 1 -ar 22050 Rec.wav
ffmpeg.exe -i Rec2.m4a -vn -acodec pcm_s16le -ac 1 -ar 22050 Rec2.wav

