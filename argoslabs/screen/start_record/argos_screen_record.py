"""
====================================
 :mod:`argoslabs.screen.start_record.argos_screen_capture`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for running python script with requirements.txt
"""
#
# Authors
# ===========
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/05/13]
#     - starting

################################################################################
import os
import cv2
import time
import pystray
import warnings
import datetime
import argparse
import pyautogui
import numpy as np
from PIL import Image
from pystray import Menu, MenuItem
from multiprocessing import Process, Value


################################################################################
warnings.filterwarnings('ignore', category=RuntimeWarning, module='runpy')


################################################################################
def exit_action(icon):
    icon.is_stop_recording.value = True
    icon.visible = False
    icon.stop()


################################################################################
def setup(icon):
    icon.visible = True
    while True:
        if icon.is_stop_recording.value:
            icon.stop()
            break
        time.sleep(1)


################################################################################
def init_icon(is_stop_recording, icon_file):
    icon = pystray.Icon('Argos Labs Screen Recording')
    icon.menu = Menu(
        MenuItem('Stop Recording', lambda: exit_action(icon)),
    )
    icon.icon = Image.open(icon_file)
    icon.title = 'Argos Labs Screen Recording'
    setattr(icon, 'is_stop_recording', is_stop_recording)
    icon.run(setup)


################################################################################
class ArgosScreenCapture(object):
    # ==========================================================================
    SUPPORTED_CODECS = [
        '.mp4',
        '.avi',
    ]

    # ==========================================================================
    def __init__(self, filename, break_file=None,
                 size_percent=80, fps=10,
                 timeout=600, is_stop_recording=None):
        _, codec = os.path.splitext(filename.lower())

        if codec not in self.SUPPORTED_CODECS:
            raise ValueError(f'CODEC must be one of {self.SUPPORTED_CODECS} but "{codec}"')
        if fps < 1:
            raise ValueError(f'FPS must higher than or equal to 1 but "{fps}"')
        if fps > 20:
            raise ValueError(f'FPS must lower than or equal to 20 but "{fps}"')
        if size_percent < 10:
            raise ValueError(f'Size Percent must higher than or equal to 10 but "{size_percent}"')
        if size_percent > 100:
            raise ValueError(f'Size Percent must lower than or equal to 100 but "{size_percent}"')
        self.fps = fps
        self.resolution = pyautogui.size()
        self.size = self.resolution[0] * size_percent // 100, \
                    self.resolution[1] * size_percent // 100
        if codec == '.mp4':
            self.codec = 0x7634706d
        elif codec == '.avi':
            self.codec = cv2.VideoWriter_fourcc(*"XVID")
        self.timeout = timeout
        self.is_stop_recording = is_stop_recording
        # for internal
        self.filename = filename
        if break_file is None:
            break_file = filename + '.brk'
        self.break_file = break_file
        self.start_ts = None
        self.end_ts = None
        self.fps_start_ts = None
        self.shot_cnt = 0
        self.delay = (1.0 - fps * 0.04) / fps

    # ==========================================================================
    def __enter__(self):
        self.open()
        return self

    # ==========================================================================
    def __exit__(self, *args):
        self.close()

    # ==========================================================================
    def open(self):
        self.out = cv2.VideoWriter(self.filename, self.codec, self.fps, self.size)
        self.start_ts = self.fps_start_ts = datetime.datetime.now()
        self.shot_cnt = 0

    # ==========================================================================
    def close(self):
        if self.out is None:
            return
        self.out.release()
        self.end_ts = datetime.datetime.now()

    # ==========================================================================
    def shot(self):
        if self.is_stop_recording is not None and self.is_stop_recording.value:
            return False
        if self.out is None:
            return False
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        b = cv2.resize(frame, self.size, fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
        self.out.write(b)

        self.shot_cnt += 1
        if self.shot_cnt % self.fps == 0:
            c_ts = datetime.datetime.now()
            if (c_ts - self.start_ts).total_seconds() >= self.timeout:
                return False
            # 딜레이 없이 초당 20번 정도 shot을 하면 거의 1초가 맞는다고 가정하면 0.05초 걸림
            # 따라서 (1.0 - fps * 0.04) / fps 만큼 deley 필요: 0.05 => 0.04
            fps_diff = c_ts - self.fps_start_ts
            if fps_diff.seconds < 1:
                time.sleep((1000000 - fps_diff.microseconds) / 1000000.0)
            self.fps_start_ts = c_ts
        if os.path.exists(self.break_file):
            os.remove(self.break_file)
            return False
        time.sleep(self.delay)
        return True


################################################################################
def start_recording(args):
    is_stop_recording = Value('i', False)
    icon_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'icon-my.png')
    p = Process(target=init_icon, args=(is_stop_recording, icon_file))
    p.start()
    with ArgosScreenCapture(
            filename=args.filename,
            break_file=args.break_file,
            size_percent=args.size_percent,
            fps=args.fps,
            timeout=args.timeout,
            is_stop_recording=is_stop_recording) as asc:
        while True:
            if not asc.shot():
                break
    is_stop_recording.value = True
    p.join()


################################################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser('Argos Labs Screen Recording')
    parser.add_argument('filename',
                        help='Filename for saving screen recording. Extension must one of {".mp4", "avi"}')
    parser.add_argument('break_file',
                        help='If this file exists then stop this recording')
    parser.add_argument('--size-percent', type=int,
                        default=80,
                        help='Percent of actual screen size, value must between 10 and 100, default is 80')
    parser.add_argument('--fps', type=int,
                        default=20,
                        help='Frames per second, value must between 5 and 30, default is 20')
    parser.add_argument('--timeout', type=int,
                        default=600,
                        help='If this timeout seconds elapsed then stop the recording')
    # cmd = [
    #     'screen-rec.mp4',
    #     'C:\\Users\\toor\\AppData\\Local\\Temp\\ARGOS_SCREEN_RECORDING.brk',
    #     '--size-percent', '80',
    #     '--fps', '20', '--timeout', '600'
    # ]
    #_args = parser.parse_args(cmd)

    _args = parser.parse_args()
    start_recording(_args)
