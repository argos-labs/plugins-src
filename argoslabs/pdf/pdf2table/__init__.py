#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.pdf.pdf2table`
====================================
.. moduleauthor:: Kyobong An <akb0930e@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS PDF Conversion(pdf -> txt) plugin
"""
# Authors
# ===========
#
# * Kyobong An
#
# --------
#
#  * [2021/08/11]
#   기능 대량 추가 {explicit_vertical_lines, explicit_horizontal_lines, snap_tolerance, join_tolerance, edge_min_length
#                 min_words_vertical, min_words_horizontal, keep_blank_chars, text_tolerance, text_x_tolerance,
#                 text_y_tolerance, intersection_tolerance, intersection_x_tolerance, intersection_y_tolerance}
#  * [2021/08/11]
#   TEXT를 사용할때 None타입 에러가 발생해서 try Except 사용해서 에러해결
#  * [2021/07/28]
#   기능추가 separator, code 수정
#  * [2021/07/28]
#     - starting

################################################################################
import os
import sys
import csv
import pdfplumber

from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class TableError(Exception):
    pass


class Pdf2table(object):
    def __init__(self, argspec, pdffile):
        self.argspec = argspec
        self.pdffile = pdffile
        self.pdf = pdfplumber.open(self.pdffile)
        self.page = argspec.page
        self.t_index = argspec.table_index
        self.vertical = argspec.vertical
        self.horizontal = argspec.horizontal
        self.encoding = argspec.encoding
        self.outfile = self.outfile(argspec.output, self.encoding)
        self.out_extension = os.path.splitext(argspec.output)[1]
        if self.out_extension == '.csv':
            self.output = csv.writer(self.outfile)  # csv형태로 내보낼때 사용
        else:
            self.output = str()     # Txet open 할때
        if self.page:
            self.pages = self.pdf.pages[self.page - 1]
        else:
            self.pages = self.pdf.pages
        self.tables = None
        self.sep = argspec.separator
        self.count = 0  # 페이지의 테이블이 있는지 없는지 체크하는 함수

    @staticmethod
    def outfile(outfile, encoding):
        out = open(outfile, 'w', encoding=encoding, newline="")
        return out

    def get_text(self):
        if self.page:  # page 선택할 수 있는 기능 추가
            self.output = self.pages.extract_text()
        else:
            for page in self.pages:
                # self.output += page.extract_text()
                try:
                    self.output += page.extract_text()
                except:
                    ...
        self.outfile.write(self.output)
        self.count = 1

    @staticmethod
    def explicit(page, explicit):
        if explicit == "curves":
            a = page.curves
        elif explicit == "lines":
            a = page.lines
        elif explicit == "rects":
            a = page.rects
        else:  # default 값
            a = []
        return a

    def get_table(self, page=None):
        if self.page:
            exp_v = self.explicit(self.pages, self.argspec.explicit_v)
            exp_h = self.explicit(self.pages, self.argspec.explicit_h)
            self.tables = self.pages.extract_tables(
                                table_settings={
                                 "vertical_strategy": self.vertical,
                                 "horizontal_strategy": self.horizontal,
                                 "explicit_vertical_lines": exp_v,
                                 # used for extract table from page[0]
                                 "explicit_horizontal_lines": exp_h,
                                 # used for extract table from page[0]
                                 "snap_tolerance": self.argspec.snap_tolerance,
                                 "join_tolerance": self.argspec.join_tolerance,
                                 "edge_min_length": self.argspec.edge_min_length,
                                 "min_words_vertical": self.argspec.min_words_vertical,
                                 "min_words_horizontal": self.argspec.min_words_horizontal,
                                 "keep_blank_chars": self.argspec.keep_blank_chars,
                                 "text_tolerance": self.argspec.text_tolerance,
                                 "text_x_tolerance": self.argspec.text_x_tolerance,
                                 "text_y_tolerance": self.argspec.text_y_tolerance,
                                 "intersection_tolerance": self.argspec.intersection_tolerance,
                                 "intersection_x_tolerance": self.argspec.intersection_x_tolerance,
                                 "intersection_y_tolerance": self.argspec.intersection_y_tolerance,
                                 })
            if self.tables:
                self.count += 1
            self.get_outfile()
        else:   # 페이지가 없는 경우 각각의 페이지에서 테이블을 가져오기위해서 page를 매개변수로 가져와 사용함
            for page in self.pages:
                exp_v = self.explicit(page, self.argspec.explicit_v)
                exp_h = self.explicit(page, self.argspec.explicit_h)
                self.tables = page.extract_tables(
                                table_settings={
                                 "vertical_strategy": self.vertical,
                                 "horizontal_strategy": self.horizontal,
                                 "explicit_vertical_lines": exp_v,
                                 # used for extract table from page[0]
                                 "explicit_horizontal_lines": exp_h,
                                 # used for extract table from page[0]
                                 "snap_tolerance": self.argspec.snap_tolerance,
                                 "join_tolerance": self.argspec.join_tolerance,
                                 "edge_min_length": self.argspec.edge_min_length,
                                 "min_words_vertical": self.argspec.min_words_vertical,
                                 "min_words_horizontal": self.argspec.min_words_horizontal,
                                 "keep_blank_chars": self.argspec.keep_blank_chars,
                                 "text_tolerance": self.argspec.text_tolerance,
                                 "text_x_tolerance": self.argspec.text_x_tolerance,
                                 "text_y_tolerance": self.argspec.text_y_tolerance,
                                 "intersection_tolerance": self.argspec.intersection_tolerance,
                                 "intersection_x_tolerance": self.argspec.intersection_x_tolerance,
                                 "intersection_y_tolerance": self.argspec.intersection_y_tolerance,
                                 })
                self.get_outfile()

                if self.tables:
                    self.count += 1

    def get_outfile(self):
        if self.out_extension == '.csv':
            if self.t_index == 0:
                for table in self.tables:
                    self.output.writerows(table)
            else:
                self.output.writerows(self.tables[self.t_index - 1])
        else:
            if self.t_index == 0:
                for table in self.tables:
                    for r_table in table:
                        self.outfile.write(self.sep.join(i if i else '' for i in r_table) + '\n')
            else:
                for r_table in self.tables[self.t_index - 1]:
                    self.outfile.write(self.sep.join(i if i else '' for i in r_table) + '\n')

    def close(self):
        self.pdf.close()
        self.pdf = None
        self.outfile.close()
        self.outfile = None
        self.output = None


################################################################################
@func_log
def pdf2doc(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    if argspec.table:
        pdffile = argspec.table
    else:
        pdffile = argspec.text
    try:
        p2t = Pdf2table(argspec, pdffile)
        if argspec.text:    # text로 PDF파일을 열었을때
            p2t.get_text()
        else:   # Table을 찾을때
            p2t.get_table()     # 페이지가 있을 때는 매개변수를 사용안함

        if p2t.count == 0:  # 페이지의 함수가 없는 경우 초기에 지정했던 0이 나옴
            msg = ('The table is not included in "%s"' % os.path.basename(pdffile))
            raise TableError(msg)

        p2t.close()

        print(os.path.abspath(argspec.output), end='')
        return 0
    except TableError as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 9
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
            display_name='PDF2Table',
            icon_path=get_icon_path(__file__),
            description='Converting from pdf file to text file',
    ) as mcxt:
        # ##################################### for app dependent options
        # ----------------------------------------------------------------------
        mcxt.add_argument('--table',
                          display_name='Table', show_default=True,
                          input_method='fileread',
                          input_group='radio=PDF File;default',
                          help='Select a pdf file for table')
        mcxt.add_argument('--text',
                          display_name='Text', show_default=True,
                          input_method='fileread',
                          input_group='radio=PDF File',
                          help='Select a pdf file for text')
        mcxt.add_argument('--output', display_name='Output Filepath', show_default=True,
                          input_method='filewrite',
                          help='Specify an absolute file path to save the output')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--page',
                          display_name='Page', type=int,
                          input_group='Table and Text option',
                          help='PDF page')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--table-index',
                          display_name='Table index', type=int, default=0,
                          input_group='Table option',
                          help='table index')
        mcxt.add_argument('--separator',
                          display_name='Separator', default=',',
                          input_group='Table option',
                          help='please enter a separator which will be inserted between words in exported .txt file')
        mcxt.add_argument('--vertical',
                          display_name='Vertical strategy', default="lines",
                          choices=["lines", "lines_strict", "text", "explicit"],
                          input_group='Table option',
                          help='for more information refer to the help page')
        mcxt.add_argument('--horizontal',
                          display_name='Horizontal strategy', default="lines",
                          choices=["lines", "lines_strict", "text", "explicit"],
                          input_group='Table option',
                          help='for more information refer to the help page')
        mcxt.add_argument('--explicit-v',
                          display_name='Explicit_vertical_lines', default=None,
                          choices=["lines", "recets", "curves"],
                          input_group='Table option',
                          help='for more information refer to the help page')
        mcxt.add_argument('--explicit-h',
                          display_name='Explicit_horizontal_lines', default=None,
                          choices=["lines", "recets", "curves"],
                          input_group='Table option',
                          help='for more information refer to the help page')
        mcxt.add_argument('--snap-tolerance',
                          display_name='Snap_tolerance', default=3, type=float,
                          input_group='Table option',
                          help='for more information refer to the help page')
        mcxt.add_argument('--join-tolerance',
                          display_name='Join_tolerance', default=3, type=int,
                          input_group='Table option',
                          help='for more information refer to the help page')
        mcxt.add_argument('--edge-min-length',
                          display_name='Edge_min_length', default=3, type=float,
                          input_group='Table option',
                          help='for more information refer to the help page')
        mcxt.add_argument('--min-words-vertical',
                          display_name='Min_words_vertical', default=3, type=float,
                          input_group='Table option',
                          help='for more information refer to the help page')
        mcxt.add_argument('--min-words-horizontal',
                          display_name='Min_words_horizontal', default=1, type=float,
                          input_group='Table option',
                          help='for more information refer to the help page')
        mcxt.add_argument('--keep-blank-chars',
                          display_name='Keep_blank_chars', action='store_true',
                          input_group='Table option',
                          help='for more information refer to the help page')
        mcxt.add_argument('--text-tolerance',
                          display_name='Text_tolerance', default=1, type=float,
                          input_group='Table option',
                          help='for more information refer to the help page')
        mcxt.add_argument('--text_x_tolerance',
                          display_name='Text_x_tolerance', default=1.5, type=float,
                          input_group='Table option',
                          help='for more information refer to the help page')
        mcxt.add_argument('--text_y_tolerance',
                          display_name='Text_y_tolerance', default=1.5, type=float,
                          input_group='Table option',
                          help='for more information refer to the help page')
        mcxt.add_argument('--intersection_tolerance',
                          display_name='Text_y_tolerance', default=3, type=int,
                          input_group='Table option',
                          help='for more information refer to the help page')
        mcxt.add_argument('--intersection-x-tolerance',
                          display_name='Intersection_x_tolerance', default=None, type=int,
                          input_group='Table option',
                          help='for more information refer to the help page')
        mcxt.add_argument('--intersection-y-tolerance',
                          display_name='Intersection_y_tolerance', default=None, type=int,
                          input_group='Table option',
                          help='for more information refer to the help page')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--encoding',
                          display_name='Encoding', default='utf-8',
                          help='Encoding for OutPut file')
        argspec = mcxt.parse_args(args)
        return pdf2doc(mcxt, argspec)
        # ##################################### for app dependent parameters


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
