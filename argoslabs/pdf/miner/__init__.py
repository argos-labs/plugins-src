#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.pdf.miner`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for pdf miner
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/09]
#     - 그룹에 "2-Business Apps" 넣음
#  * [2020/06/03]
#     - starting
#

################################################################################
import os
import sys
import csv
import pdfminer
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pprint import pformat


################################################################################
class PDFMiner(object):
    # ==========================================================================
    header = ('pageid', 'width', 'height', 'x0', 'y0', 'x1', 'y1', 'text')

    # ==========================================================================
    def __init__(self, pdf_file):
        if not os.path.exists(pdf_file):
            raise IOError(f'Cannot find pdf file "{pdf_file}"')
        self.pdf_file = pdf_file
        # for internal
        self.pages = []

    # ==========================================================================
    def _parse_obj(self, lt_objs, textboxes):
        for obj in lt_objs:
            # if it's a textbox, print text and location
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                # print("%3.3f, %3.3f, %3.3f, %3.3f, %s" % (
                #     obj.x0, obj.y0, obj.x1, obj.y1, obj.get_text().strip()
                # ))
                assert(obj.bbox[0] == obj.x0 and obj.bbox[1] == obj.y0 and
                       obj.bbox[2] == obj.x1 and obj.bbox[3] == obj.y1)
                textboxes.append([round(obj.x0, 3), round(obj.y0, 3),
                                  round(obj.x1, 3), round(obj.y1, 3),
                                  obj.get_text().strip()])
            # if it's a container, recurse
            elif isinstance(obj, pdfminer.layout.LTFigure):
                # noinspection PyProtectedMember
                self._parse_obj(obj._objs, textboxes)

    # ==========================================================================
    def do_miner(self):
        with open(self.pdf_file, 'rb') as ifp:
            parser = PDFParser(ifp)
            document = PDFDocument(parser)
            if not document.is_extractable:
                raise PDFTextExtractionNotAllowed('Image base PDF cannot be extract text')
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(document):
                interpreter.process_page(page)
                layout = device.get_result()
                # print(layout)
                page_d = {
                    'pageid': layout.pageid,
                    'width': round(layout.width, 3),
                    'height': round(layout.height, 3),
                    'rotate': layout.rotate,
                    'textboxes': []
                }
                # noinspection PyProtectedMember
                self._parse_obj(layout._objs, page_d['textboxes'])
                self.pages.append(page_d)

    # ==========================================================================
    def next(self, text, pageid=0, startswith=False, endswith=False, contains=False,
             left_down_origin=False):
        for page_d in self.pages:
            if 0 < pageid != page_d['pageid']:
                continue
            for tb in page_d['textboxes']:
                t_found = False
                if contains:
                    if tb[4].find(text) >= 0:
                        t_found = True
                elif endswith:
                    if tb[4].endswith(text):
                        t_found = True
                elif startswith:
                    if tb[4].startswith(text):
                        t_found = True
                else:
                    if tb[4] == text:
                        t_found = True
                if t_found:
                    if not left_down_origin:
                        y0 = round(page_d['height'] - tb[1], 3)
                        y1 = round(page_d['height'] - tb[3], 3)
                        tb[1] = min(y0, y1)
                        tb[3] = max(y0, y1)
                    yield [page_d['pageid'], page_d['width'], page_d['height'],
                           tb[0], tb[1], tb[2], tb[3], tb[4]]

    # ==========================================================================
    def get(self, text, pageid=0, startswith=False, endswith=False, contains=False,
            left_down_origin=False, order_by_column=7, desc=False):
        rows = list()
        for row in self.next(text, pageid, startswith, endswith, contains,
                             left_down_origin):
            rows.append(row)
        order_by_column -= 1
        if 0 <= order_by_column < 8:
            rows.sort(key=lambda x: x[order_by_column], reverse=desc)
        return rows

    # ==========================================================================
    def __repr__(self):
        sl = list()
        sl.append(f'# of pages: {len(self.pages)}')
        for page_d in self.pages:
            sl.append(pformat(page_d, 4))
        return '\n'.join(sl)


################################################################################
@func_log
def do_pdfminer(mcxt, argspec):
    try:
        mcxt.logger.info('>>>starting...')

        if not argspec.text:
            raise ValueError('invalid "Search Text"')
        pm = PDFMiner(argspec.pdffile)
        pm.do_miner()
        # print(pm)
        rows = pm.get(argspec.text, pageid=argspec.page,
                      startswith=argspec.startswith, endswith=argspec.endswith,
                      contains=argspec.contains,
                      left_down_origin=argspec.left_down_origin,
                      order_by_column=argspec.order_by_column,
                      desc=argspec.desc)
        c = csv.writer(sys.stdout, lineterminator='\n')
        c.writerow(PDFMiner.header)
        for row in rows:
            c.writerow(row)
        return 0
    except Exception as e:
        msg = str(e)
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
        group='2',  # Business Apps
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='PDF Miner',
        icon_path=get_icon_path(__file__),
        description='Get Information of TextBox',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('pdffile',
                          display_name='PDF File',
                          input_method='fileread',
                          help='PDF File')
        mcxt.add_argument('text',
                          display_name='Search Text',
                          help='Text to search')
        # ##################################### for app dependent options
        mcxt.add_argument('--page',
                          display_name='Page', show_default=True,
                          default=0, type=int,
                          help='Page to search, default is [[0]] which is all, first page is 1')
        mcxt.add_argument('--startswith',
                          display_name='Starts With', action='store_true',
                          help='If this flag is set then the text to search is starting with')
        mcxt.add_argument('--endswith',
                          display_name='Ends With', action='store_true',
                          help='If this flag is set then the text to search is ending with')
        mcxt.add_argument('--contains',
                          display_name='Contains', action='store_true',
                          help='If this flag is set then the text to search is contained')
        mcxt.add_argument('--left-down-origin',
                          display_name='LeftDown Orig', action='store_true',
                          help='If this flag is set then left down is origin (0,0)')
        mcxt.add_argument('--order-by-column',
                          display_name='Order By Col',
                          default=7, type=int,
                          help='Order by column, default is lower y, [[7]] which is bottom y')
        mcxt.add_argument('--desc',
                          display_name='Descending', action='store_true',
                          help='If this flag is set then order by desc')
        argspec = mcxt.parse_args(args)
        return do_pdfminer(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
