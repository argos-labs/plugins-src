"""
====================================
 :mod:`argoslabs.google.youtube`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module ai translate
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2022/03/05] Kyobong
#     - get_info에 self.yt.description 값이 None 타입일 경우가 존재 수정
#     - TODO: caption은 라이브러리 에러가 있음 https://github.com/pytube/pytube/issues/1674
#  * [2022/03/05]
#     - Youtube => YouTube
#  * [2022/03/03]
#     - TODO: --caption-srt not working currently XML save only
#  * [2022/02/28]
#     - "Stream Info", "Download"
#  * [2022/02/03]
#     - starting

################################################################################
import os
import sys
import csv
# import shutil
from bs4 import BeautifulSoup
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
# noinspection PyPackageRequirements
from pytube import YouTube


################################################################################
class MyTube(object):
    # ==========================================================================
    OP = (
        'Get Info',
        'Stream Info',
        "Download",
        "Caption Info",
        "Caption Get",
    )
    URL = 'https://www.youtube.com/watch?v='
    INFO_HAEDER = (
        'video_id',
        'title',
        'author',
        'publish_date',
        'rating',
        'views',
        'description',
        'keywords',
        'thumbnail_url',
        'len_seconds',
        'num_streams',
        'num_captions',
    )
    STREAM_HAEDER = (
        'index',
        'itag',
        'mime_type',
        'resolution',
        'fps',
        'video_codec',
        'audio_codec',
        'is_progressive',
        'type',
        'abr',
        'bitrate',
        'expiration',
        'filesize',
    )
    CAPTION_HAEDER = (
        'index',
        'code',
        'name',
        'url',
    )

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.video_id = argspec.video_id
        self.yt = YouTube(self.URL + self.video_id)

    # ==========================================================================
    def get_info(self):
        cw = csv.writer(sys.stdout, lineterminator='\n')
        cw.writerow(self.INFO_HAEDER)
        title = self.yt.title
        title = title.replace('\r', '')
        title = title.replace('\n', ' ')
        desc = self.yt.description
        if desc:
            desc = desc.replace('\r', '')
            desc = desc.replace('\n', ' ')
        keywords = list()
        for k in self.yt.keywords:
            k = k.replace('\r', '')
            k = k.replace('\n', ' ')
            k = k.replace(':', ' ')
            keywords.append(k)
        row = [
            self.video_id,
            self.yt.title,
            self.yt.author,
            self.yt.publish_date.strftime('%Y%m%d-%H%M%S'),
            self.yt.rating,
            self.yt.views,
            desc,
            ':'.join(keywords),
            self.yt.thumbnail_url,
            self.yt.length,
            len(self.yt.streams),
            len(self.yt.captions),
        ]
        cw.writerow(row)

    # ==========================================================================
    def stream_info(self):
        cw = csv.writer(sys.stdout, lineterminator='\n')
        cw.writerow(self.STREAM_HAEDER)
        # sts = [s for s in self.yt.streams]
        for i, st in enumerate(self.yt.streams):
            row = [
                str(i + 1),
                st.itag,
                st.mime_type,
                st.resolution,
                st.fps if hasattr(st, 'fps') else 'None',
                st.video_codec,
                st.audio_codec,
                st.is_progressive,
                st.type,
                st.abr,
                st.bitrate,
                st.expiration.strftime('%Y%m%d-%H%M%S'),
                st.filesize,
            ]
            cw.writerow(map(str, row))

    # ==========================================================================
    def download(self):
        if not self.argspec.save_file:
            raise IOError('Inalid "Save File"')
        try:
            st = self.yt.streams[self.argspec.stream_index - 1]
        except Exception as err:
            raise IndexError(f'Cannot get index {self.argspec.stream_index} stream, first get the result of "Stream Info"')
        sf = os.path.abspath(self.argspec.save_file)
        sf_dir = os.path.dirname(sf)
        sf_bn = os.path.basename(sf)
        rf = st.download(
            output_path=sf_dir,
            filename=sf_bn,
            skip_existing=False,
            timeout=self.argspec.timeout,
        )
        print(rf, end='')

    # ==========================================================================
    def caption_info(self):
        cw = csv.writer(sys.stdout, lineterminator='\n')
        cw.writerow(self.CAPTION_HAEDER)
        # sts = [s for s in self.yt.streams]
        for i, cp in enumerate(self.yt.captions):
            row = [
                str(i + 1),
                cp.code,
                cp.name,
                cp.url,
            ]
            cw.writerow(map(str, row))

    # ==========================================================================
    @staticmethod
    def xml2text(xmlstr):
        ts = list()
        soup = BeautifulSoup(xmlstr, 'html.parser')
        for p in soup.find_all('p'):
            ts.append(p.text.strip())
        return '\n'.join(ts)

    # ==========================================================================
    def caption_get(self):
        if not self.argspec.caption_file:
            raise IOError('Inalid "Caption File"')
        try:
            caps = [cp for cp in self.yt.captions]
            cp = caps[self.argspec.caption_index - 1]
        except Exception as err:
            raise IndexError(f'Cannot get index {self.argspec.stream_index} caption, first get the result of "Caption Info"')
        cf = os.path.abspath(self.argspec.caption_file)
        cp_str = cp.xml_captions
        # if self.argspec.caption_srt:
        #     cp_str = cp.xml_caption_to_srt(cp_str)
        if self.argspec.caption_text:
            cp_str = self.xml2text(cp_str)
        with open(cf, 'w', encoding='utf-8') as ofp:
            ofp.write(cp_str)
        print(cf, end='')


################################################################################
@func_log
def do_youtube(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        mt = MyTube(argspec)
        if argspec.op == MyTube.OP[0]:  # Get Info
            mt.get_info()
        elif argspec.op == MyTube.OP[1]:  # Stream Info
            mt.stream_info()
        elif argspec.op == MyTube.OP[2]:  # Download
            mt.download()
        elif argspec.op == MyTube.OP[3]:  # Caption Info
            mt.caption_info()
        elif argspec.op == MyTube.OP[4]:  # Caption Get
            mt.caption_get()
        return 0
    except Exception as e:
        msg = 'Youtube error: %s' % str(e)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        mcxt.logger.error(msg)
        return 99
    finally:
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    try:
        with ModuleContext(
            owner='ARGOS-LABS',
            group='10',   # Web Scraping
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='YouTube Operation',
            icon_path=get_icon_path(__file__),
            description='Youtube Video Operation',
        ) as mcxt:
            ##################################### for app dependent parameters
            mcxt.add_argument('op',
                              default=MyTube.OP[0],
                              choices=MyTube.OP,
                              display_name='Operation',
                              help='Operations for Youtube video')
            mcxt.add_argument('video_id',
                              display_name='Video ID',
                              help='Youtube video id')
            ##################################### for app dependent options
            mcxt.add_argument('--save-file',
                              input_group='Download;groupbox',
                              display_name='Save file',
                              input_method='filewrite',
                              help='File path to download of video/audio')
            mcxt.add_argument('--stream-index',
                              input_group='Download;groupbox',
                              display_name='Stream Index',
                              type=int, default=1,
                              help='Stream index from "Stream Info", default is the first [[1]]]')
            mcxt.add_argument('--timeout',
                              input_group='Download;groupbox',
                              display_name='Timeout', type=int, default=20,
                              help='Download timeout, default is [[20]]')
            ##################################### for app dependent options
            mcxt.add_argument('--caption-file',
                              input_group='Caption Get;groupbox',
                              display_name='Save Cap file',
                              input_method='filewrite',
                              help='File path to download of caption')
            mcxt.add_argument('--caption-index',
                              input_group='Caption Get;groupbox',
                              display_name='Caption Index',
                              type=int, default=1,
                              help='Caption index from "Caption Info", default is the first [[1]]]')
            mcxt.add_argument('--caption-text',
                              action='store_true',
                              input_group='Caption Get;groupbox',
                              display_name='Extract Text',
                              help='If this flag is set extracting text only')
            # mcxt.add_argument('--caption-srt',
            #                   action='store_true',
            #                   input_group='Caption Get;groupbox',
            #                   display_name='SRT Format',
            #                   help='If this flag is set SRT format will be saved otherwise XML format')

            argspec = mcxt.parse_args(args)
            return do_youtube(mcxt, argspec)
    except Exception as e:
        msg = 'Youtube error: %s' % str(e)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        mcxt.logger.error(msg)
        return 98


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
