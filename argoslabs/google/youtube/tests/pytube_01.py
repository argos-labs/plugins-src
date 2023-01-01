import sys
from pytube import YouTube, Channel

# https://stackoverflow.com/questions/68680322/pytube-urllib-error-httperror-http-error-410-gone




# url = "https://www.youtube.com/watch?v=IZhXZRpZWOc"
# yt = YouTube(url)
# captions = yt.captions.all()
# caption = captions[0]
# xml = caption.xml_captions
# print(caption.xml_captions)
# a = caption.float_to_srt_time_format
# print(caption.float_to_srt_time_format)

vids = (
    '61LwFaWJ5jI',
    '8MDXAPL0Um0',
    'AhWZbrNhoIc',
    'fhi-ETomA74',
    'jwRDEt51mBI',
    'O9F6EC-HS0E',
    'ji_wxLA-8X8',
    'u5B4XMzyi98',
    # '6NqICdhKSk4',
    # 'kB-dJaCXAxA',
    # '1sISguPDlhY',
    # 'IxndOd3kmSs',
    # 'JwhouCNq-Fc',
)

for vid in vids:
    url = f"https://www.youtube.com/watch?v={vid}"
    yt = YouTube(url)
    title = yt.title
    print(title)
    title = title.replace('’', "'")
    title = title.replace('“', '"')
    title = title.replace('”', '"')
    print(title)


sys.exit(0)


# c_url = 'https://www.youtube.com/channel/UCcdwLMPsaU2ezNSJU1nFoBQ'
# c = Channel(c_url)
# print(c.channel_name)
