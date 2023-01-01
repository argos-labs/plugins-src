import os
def zenity(op):
   os.system(f'zenity --{op}')
#zenity('calendar') -1
#zenity('entry')
#zenity('zenity_info')
#zenity('file-selection') -1
#zenity('list') -1
#zenity('zenity_question --text="Are you sure you want to process?"   && echo YES || echo NO')
#zenity('warning && echo YES || echo NO')
#zenity('scale')
#zenity('text-zenity_info --editable ') -1
#zenity('color-selection --show-palette ') -2
#zenity('password')
#zenity('forms')- 1
#zenity('calendar --display=DISPLAY') -> xwindow server, skip