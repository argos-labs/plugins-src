"""
====================================
 :mod:`argoslabs.data.word2txt`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Docx Conversion(docs -> txt) plugin
"""
# Authors
# ===========
#
# * Kyobong An
#
# --------
#
#  * [2021/11/17]
#     - 플러그인 이름 변경 Doc2TXT -> Word2TXT
#  * [2021/11/16]
#     - stu에서 "pypandoc" 모듈을 설치하라고 나오면서 작동하지않음. docx2txt와 win32com 사용해서 리빌드함.
#  * [2021/06/22]
#     - starting

################################################################################
import re
import os
import sys
import docx2txt
import win32com.client
# from alabs.common.util.vvencoding import get_file_encoding
from alabs.common.util.vvargs import func_log, get_icon_path, ModuleContext, \
    ArgsError, ArgsExit


class Word2Txt(object):
    def __init__(self, argspec):
        self.filename = argspec.filename
        self.output = argspec.output
        self.text = None

        if os.path.splitext(self.filename)[1] == '.doc':
            self.text = self.doc2txt()
        elif os.path.splitext(self.filename)[1] == '.docx':
            self.text = self.do_docx2txt()
            self.remove_spaces()    # 줄과줄사이에 줄바꿈이 한번들어가는 것을 제거하기위한 함수

        if argspec.output:
            with open(self.output, 'w', encoding=argspec.encoding) as file:
                file.write(self.text)
                file.close()
            print(self.output)
        else:
            print(self.text)

    def remove_spaces(self):
        temp = self.text.split('\n\n')
        self.text = "\n".join(temp)

    def get_output_file_path(self):
        return os.path.splitext(self.filename)[0] + '.txt'

    def doc2txt(self):
        app = win32com.client.Dispatch('Word.Application')
        doc = app.Documents.Open(self.filename)
        text = doc.Content.Text
        app.Quit()
        return text

    def do_docx2txt(self):    # 파일을 변환 하는데 단락 사이에 \n 공백이 생김
        text = docx2txt.process(self.filename)
        return text


################################################################################
@func_log
def do_word2txt(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        Word2Txt(argspec)
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 99
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
            owner='ARGOS-LABS',
            group='2',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='Word2TXT',
            icon_path=get_icon_path(__file__),
            description='Converting from word file to text file',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('filename', display_name='Doc/Docx File',
                          input_method='fileread', help='Select a word file')
        mcxt.add_argument('--output', display_name='Output Filepath',
                          input_method='filewrite',
                          help='Specify an absolute file path to save the output')
        mcxt.add_argument('--encoding', display_name='Encoding', default='utf-8',
                          help='Encoding for .txt file')
        argspec = mcxt.parse_args(args)
        return do_word2txt(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
