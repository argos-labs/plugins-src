"""
====================================
 :mod:`argoslabs.ocr.tesseract`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module sample
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2022/09/20]
#     - req_gw_get() 를 추가하여 NC2 인 경우 GW를 통하도록 함
#     - .argos-rpa.venv 대신 .argos-rpa.cache 에 저장
#  * [2021/04/09]
#     - 그룹에 "1-AI Solutions" 넣음
#  * [2020/03/21]
#     - install_tesseract.html 디자인 적용
#  * [2020/03/19]
#     - 최초 install_tesseract.html 설치 가이드 보여주기
#  * [2020/03/17]
#     - image, lang 을 옵션에서 제외하고 항상 넣도록, 아이콘 색상 조정
#  * [2020/03/10]
#     - download traineddata
#  * [2020/03/05]
#     - do main
#  * [2020/01/23]
#     - change call parameters
#  * [2019/08/11]
#     - finish
#  * [2019/08/10]
#     - starting

################################################################################
import os
import sys
# noinspection PyPackageRequirements
import cv2
import glob
import time
import shutil
import pathlib
import requests
import subprocess
# noinspection PyPackageRequirements
import pytesseract
# from tempfile import gettempdir
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import webbrowser


################################################################################
class Tesseract(object):
    # ==========================================================================
    VERSION = '4'
    TDIR = os.path.join(f'{os.environ["ProgramFiles"]}', 'Tesseract-OCR')
    DATADIRS = (
        os.path.join(TDIR, 'tessdata'),
        os.path.join(str(pathlib.Path.home()), '.argos-rpa.cache', 'tessdata')
    )
    # ==========================================================================
    OP_LIST = [
        'OCR',
        'List Languages',
        'Get Version',
    ]
    PSM_LIST = [
        'Orientation and script detection (OSD) only',
        'Automatic page segmentation with OSD',
        'Automatic page segmentation, but no OSD, or OCR',
        'Fully automatic page segmentation, but no OSD',   # Default
        'Assume a single column of text of variable sizes',
        'Assume a single uniform block of vertically aligned text',
        'Assume a single uniform block of text',
        'Treat the image as a single text line',
        'Treat the image as a single word',
        'Treat the image as a single word in a circle',
        'Treat the image as a single character',
        'Sparse text. Find as much text as possible in no particular order',
        'Sparse text with OSD',
        'Raw line. Treat the image as a single text line',
    ]
    OEM_LIST = [
        'Original Tesseract only',
        'Neural nets LSTM only',
        'Tesseract + LSTM',
        'Based on what is available',   # Default
    ]

    # ==========================================================================
    LANG_DICT = {  # Tesseract4 data
        'Afrikaans': 'afr',
        'Amharic': 'amh',
        'Arabic': 'ara',
        'Assamese': 'asm',
        'Azerbaijani': 'aze',
        'Azerbaijani, Cyrillic': 'aze_cyrl',
        'Belarusian': 'bel',
        'Bengali': 'ben',
        'Tibetan': 'bod',
        'Bosnian': 'bos',
        'Breton': 'bre',
        'Bulgarian': 'bul',
        'Valencian': 'cat',
        'Cebuano': 'ceb',
        'Czech': 'ces',
        'Chinese, Simplified': 'chi_sim',
        'Chinese, Simplified, Vertical': 'chi_sim_vert',
        'Chinese, Traditional': 'chi_tra',
        'Chinese, Traditional, Vertical': 'chi_tra_vert',
        'Cherokee': 'chr',
        'Corsican': 'cos',
        'Welsh': 'cym',
        'Danish': 'dan',
        'Danish Fraktur': 'dan_frak',
        'German': 'deu',
        'German Fraktur': 'deu_frak',
        'Divehi': 'div',
        'Dzongkha': 'dzo',
        'Greek': 'ell',
        'English': 'eng',
        'English, Middle': 'enm',
        'Esperanto': 'epo',
        # '': 'equ',
        'Estonian': 'est',
        'Basque': 'eus',
        'Faroese': 'fao',
        'Persian': 'fas',
        'Pilipino': 'fil',
        'Finnish': 'fin',
        'French': 'fra',
        # '': 'frk',
        'French, Middle': 'frm',
        'Western Frisian	': 'fry',
        'Gaelic': 'gla',
        'Irish': 'gle',
        'Galician': 'glg',
        'Greek, Ancient': 'grc',
        'Gujarati': 'guj',
        'Haitian': 'hat',
        'Hebrew': 'heb',
        'Hindi': 'hin',
        'Croatian': 'hrv',
        'Hungarian': 'hun',
        'Armenian': 'hye',
        'Inuktitut': 'iku',
        'Indonesian': 'ind',
        'Icelandic': 'isl',
        'Italian': 'ita',
        'Javanese': 'jav',
        'Japanese': 'jpn',
        'Japanese, Vertical': 'jpn_vert',
        'Kannada': 'kan',
        'Georgian': 'kat',
        'Kazakh': 'kaz',
        'Central Khmer': 'khm',
        'Kirghiz': 'kir',
        # '': 'kmr',
        'Korean': 'kor',
        'Korean, Vertical': 'kor_vert',
        'Lao': 'lao',
        'Latin': 'lat',
        'Latvian': 'lav',
        'Lithuanian': 'lit',
        'Luxembourgish': 'ltz',
        'Malayalam': 'mal',
        'Marathi	': 'mar',
        'Macedonian': 'mkd',
        'Maltese': 'mlt',
        'Mongolian': 'mon',
        'Maori': 'mri',
        'Malay': 'msa',
        'Burmese': 'mya',
        'Nepali': 'nep',
        'Dutch': 'nld',
        'Norwegian': 'nor',
        'Occitan': 'oci',
        'Oriya': 'ori',
        'Orientation Script Detection': 'osd',
        'Panjabi': 'pan',
        'Polish': 'pol',
        'Portuguese': 'por',
        'Pushto': 'pus',
        'Quechua': 'que',
        'Romanian': 'ron',
        'Russian': 'rus',
        'Sanskrit': 'san',
        'Sinhala': 'sin',
        'Slovak': 'slk',
        'Slovak Fraktur': 'slk_frak',
        'Slovenian': 'slv',
        'Sindhi': 'snd',
        'Spanish': 'spa',
        'Spanish, Old': 'spa_old',
        'Albanian': 'sqi',
        'Serbian': 'srp',
        'Serbian Latin': 'srp_latn',
        'Sundanese': 'sun',
        'Swahili': 'swa',
        'Swedish': 'swe',
        'Syriac': 'syr',
        'Tamil': 'tam',
        'Tatar': 'tat',
        'Telugu': 'tel',
        'Tajik': 'tgk',
        'Tagalog': 'tgl',
        'Thai': 'tha',
        'Tigrinya': 'tir',
        'Tonga ': 'ton',
        'Turkish': 'tur',
        'Uighur': 'uig',
        'Ukrainian': 'ukr',
        'Urdu': 'urd',
        'Uzbek': 'uzb',
        'Uzbek, Cyrillic': 'uzb_cyrl',
        'Vietnamese': 'vie',
        'Yiddish': 'yid',
        'Yoruba': 'yor',
    }

    # ==========================================================================
    @staticmethod
    def req_gw_get_url():
        urls = [
            'https://pypi-official.argos-labs.com/gw-files/tesseract-ocr-w32-setup-v4.1.0.20190314.exe',
            'https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-v4.1.0.20190314.exe',
        ]
        for url in urls:
            try:
                r = requests.get(url)
                if r.status_code // 10 == 20:
                    return url
            except:
                continue
        raise ReferenceError(f'Cannot download "tesseract-ocr-w32-setup-v4.1.0.20190314.exe" from urls={urls}')

    # ==========================================================================
    def _check_bin_win32(self):
        bin_file = os.path.join(self.TDIR, 'tesseract.exe')
        if not os.path.exists(bin_file):
            # dw = 'http://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-setup-4.00.00dev.exe'
            # dw = 'https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-v4.1.0.20190314.exe'
            dw_url = self.req_gw_get_url()
            if dw_url.startswith('https://pypi-official.argos-labs.com/gw-files/'):
                dw = os.path.join(os.path.dirname(__file__), 'install_tesseract.gw.html')
            else:
                dw = os.path.join(os.path.dirname(__file__), 'install_tesseract.html')
            url = 'file:///' + dw.replace('\\', '/')
            cmd = [
                sys.executable,
                '-m',
                'webbrowser',
                '-n',
                url
            ]
            po = subprocess.Popen(cmd)
            po.wait()
            raise RuntimeError(f'[Checkout your Browser] Cannot find "{bin_file}" for Windows tesseract\n')
        return bin_file

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _check_bin_nix(self):
        bin_file = shutil.which('tesseract')
        if bin_file:
            return bin_file
        if sys.platform == 'darwin':  # Mac
            raise RuntimeError('Please install tesseract. '
                               'Cannot find tesseract in your Mac.')
        else:
            raise RuntimeError('Please install tesseract. '
                               'Cannot find tesseract in your Linux.')

    # ==========================================================================
    def _check_bin(self):
        if sys.platform == 'win32':
            return self._check_bin_win32()
        elif sys.platform in ('darwin', 'linux'):
            return self._check_bin_nix()
        raise RuntimeError(f'Not supported platform "{sys.platform}"')

    # ==========================================================================
    def _get_lang_rd(self):
        for k, v in self.LANG_DICT.items():
            self.lang_rd[v] = k

    # ==========================================================================
    def _prepare_data(self):
        if not os.path.exists(self.DATADIRS[1]):
            os.makedirs(self.DATADIRS[1])
        for f in glob.glob(os.path.join(self.DATADIRS[0], '*.traineddata')):
            bn = os.path.basename(f)
            if not os.path.exists(os.path.join(self.DATADIRS[1], bn)):
                shutil.copy(f, os.path.join(self.DATADIRS[1], bn))

    # ==========================================================================
    def __init__(self):
        self.bin_file = self._check_bin()
        pytesseract.pytesseract.tesseract_cmd = self.bin_file
        # for internal
        self.lang_rd = {}
        self._prepare_data()

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def version(self):
        return pytesseract.get_tesseract_version()

    # ==========================================================================
    def list_langs(self):
        print('\n'.join(self.LANG_DICT.keys()))

    # ==========================================================================
    def get_lang_from_code(self, lc):
        if not self.lang_rd:
            self._get_lang_rd()
        if lc in self.lang_rd:
            return self.lang_rd[lc]
        raise ReferenceError(f'Cannot get langulage code "{lc}"')

    # ==========================================================================
    @staticmethod
    def req_gw_get(lang):
        urls = [
            f'https://pypi-official.argos-labs.com/gw-files/{lang}.traineddata',
            f'https://github.com/tesseract-ocr/tessdata/raw/master/{lang}.traineddata',
        ]
        for url in urls:
            try:
                r = requests.get(url)
                if r.status_code // 10 == 20:
                    return r
            except:
                continue
        raise ReferenceError(f'Cannot download "tesseract-ocr-w32-setup-v4.1.0.20190314.exe" from urls={urls}')

    # ==========================================================================
    def get_langs(self):
        tdlist = []
        for DATADIR in self.DATADIRS[1:]:
            for f in glob.glob(os.path.join(DATADIR, '*.traineddata')):
                bn = os.path.basename(f)
                lc, _ = os.path.splitext(bn)
                tdlist.append(self.get_lang_from_code(lc))
        return tdlist

    # ==========================================================================
    def check_lang(self, lang):
        if lang not in self.get_langs():
            # download
            url = 'https://github.com/tesseract-ocr/tessdata/raw/master/%s.traineddata'
            # rp = requests.get(url % self.LANG_DICT[lang])
            rp = self.req_gw_get(self.LANG_DICT[lang])
            with open(os.path.join(self.DATADIRS[1], '%s.traineddata'
                                                     % self.LANG_DICT[lang]),
                      'wb') as ofp:
                ofp.write(rp.content)
        return self.LANG_DICT[lang]


################################################################################
@func_log
def do_ts(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        ts = Tesseract()
        if ts.OP_LIST.index(argspec.op) == 0:       # OCR
            if not (argspec.image and os.path.exists(argspec.image)):
                raise ValueError(f'Invalid image file {argspec.image}')
            lang = ts.check_lang(argspec.lang)
            if argspec.lang2:
                lang += '+' + ts.check_lang(argspec.lang2)
            config = f'--tessdata-dir "{ts.DATADIRS[1]}"'
            psm = ts.PSM_LIST.index(argspec.psm)
            config += f' --psm {psm}'
            oem = ts.OEM_LIST.index(argspec.oem)
            config += f' --oem {oem}'
            img = cv2.imread(argspec.image)
            # we need to convert from BGR to RGB format/mode:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            rs = pytesseract.image_to_string(img_rgb, lang=lang, config=config)
            print(rs, end='')
        elif ts.OP_LIST.index(argspec.op) == 1:     # List Languages
            if argspec.trained_lang:
                tdlist = ts.get_langs()
                print('\n'.join(tdlist), end='')
            else:
                print('\n'.join(ts.LANG_DICT.keys()), end='')
        elif ts.OP_LIST.index(argspec.op) == 2:     # Get Version
            print(ts.version(), end='')
        else:
            raise ValueError(f'Invalid operation "{argspec.op}"')
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
        owner='ARGOS-LABS',
        group='1',  # AI Solutions
        version='4',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Tesseract',
        icon_path=get_icon_path(__file__),
        description='Tesseract OCR Engine',
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--lang2',
                          display_name='2nd Lang',
                          choices=list(Tesseract.LANG_DICT.keys()),
                          help='Second Language to OCR')
        mcxt.add_argument('--psm',
                          display_name='Page segmentation',
                          default='Fully automatic page segmentation, but no OSD',
                          choices=list(Tesseract.PSM_LIST),
                          help='Page segmentation modes')
        mcxt.add_argument('--oem',
                          display_name='OCR Engine',
                          default='Based on what is available',
                          choices=list(Tesseract.OEM_LIST),
                          help='OCR Engine modes')
        mcxt.add_argument('--trained-lang', action='store_true',
                          display_name='Trained Lang',
                          help='Get list of languages only have the trained data '
                               'for the "List Languages" operation')
        # ##################################### for app dependent parameters
        mcxt.add_argument('op',
                          display_name='Operation', choices=Tesseract.OP_LIST,
                          default='OCR',
                          help='Tesseract operations')
        mcxt.add_argument('image', show_default=True,
                          display_name='Image file', input_method='fileread',
                          help='Image file to recognize')
        mcxt.add_argument('lang', show_default=True,
                          display_name='Language',
                          default='English',
                          choices=list(Tesseract.LANG_DICT.keys()),
                          help='Language to OCR')
        argspec = mcxt.parse_args(args)
        return do_ts(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
