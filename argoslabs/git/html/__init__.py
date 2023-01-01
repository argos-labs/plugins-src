"""
====================================
 :mod:`argoslabs.git.html`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS managing Ms Teams
"""
# Authors
# ===========
#
# * Arun Kumar
#
# Change Log
# --------
#
#  * [2022/08/14]
#     - send message to chanell
#

################################################################################
import os
import sys
import requests
import subprocess
import urllib.request
from io import StringIO
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import pathname2url
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import win32com.client as client
import warnings


################################################################################
class Gitmd2docx(object):
    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.html_path = None
        self.html_path_url = None
        self.pdf_path = None
        self.docx_path = None

    # ==========================================================================
    def md2docx(self):
        outst = StringIO()
        filename = self.argspec.gitmdlink.split('/')[-1]
        if not filename.lower().endswith('.md'):
            raise Exception('Git MD Link not end with .md file')
        else:
            md2html = self.md2html()
            if self.argspec.word:
                html2docx = self.html2docx()
                outst.write('html_path,html_path_url,docx_path')
                outst.write('\n')
                outst.write(f'{self.html_path},{md2html},{html2docx}')
            elif self.argspec.chromepath:
                html2pdf = self.html2pdf()
                pdf2docx = self.pdf2docx()
                outst.write('html_path,html_path_url,pdf_path,docx_path')
                outst.write('\n')
                outst.write(f'{self.html_path},{md2html},{html2pdf},{pdf2docx}')
            else:
                outst.write('html_path,html_path_url')
                outst.write('\n')
                outst.write(f'{self.html_path},{md2html}')
            outst.write('\n')
            print(outst.getvalue(), end='')

    # ==========================================================================
    def md2html(self):
        try:
            fp = urllib.request.urlopen(self.argspec.gitmdlink)
        except Exception as err:
            return str(err)
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        soup = BeautifulSoup(mystr, "lxml")
        head = soup.find("head")
        body = soup.find("div", attrs={"id": 'readme'})
        mystr = str(head) + str(body)
        replace_href = replace_src = self.argspec.username
        while f'href="/{replace_href}' in mystr:
            mystr = mystr.replace(f'href="/{replace_href}',
                                  f'href="https://github.com/'
                                  f'{replace_href}')
        while f'src="/{replace_src}' in mystr:
            mystr = mystr.replace(f'src="/'
                                  f'{replace_src}',
                                  f'src="https://github.com/'
                                  f'{replace_src}')
        fp.close()
        if self.argspec.filename:
            self.html_path = f'{self.argspec.output}/{self.argspec.filename}.html'
        else:
            self.html_path = f'{self.argspec.output}/readme.html'
        with open(self.html_path, "w", encoding="utf-8") as f:
            mystr = mystr.replace("\n", "")
            mystr = mystr.replace("'", "`")
            f.write(str(mystr))
        self.html_path_url = urljoin('file:', pathname2url(self.html_path))
        return self.html_path_url

    # ==========================================================================
    def html2pdf(self):
        self.pdf_path = f'{self.argspec.output}/{self.argspec.filename}.pdf'
        cmd = f"{self.argspec.chromepath} " \
              f"--disable-gpu " \
              f"--headless " \
              f"--print-to-pdf-no-header " \
              f"--disable-pdf-tagging " \
              f"--print-to-pdf={self.pdf_path} " \
              f"{self.html_path_url}"
        if self.argspec.chromepath == 'start chrome':
            try:
                os.system(cmd)
                return self.pdf_path
            except Exception as err:
                return str(err)
        elif os.path.basename(self.argspec.chromepath) == 'chrome.exe':
            if os.path.exists(self.argspec.chromepath):
                try:
                    proc = subprocess.Popen(cmd)
                    proc.wait(timeout=30)
                    return self.pdf_path
                except Exception as err:
                    return str(err)
            else:
                raise Exception(
                    f'The file {self.argspec.chromepath} does not exist')
        else:
            raise Exception('Enter "start chrome" or "chrome path"')

    # ==========================================================================
    def pdf2docx(self):
        if self.argspec.filename:
            self.docx_path = f'{self.argspec.output}/{self.argspec.filename}.docx'
        else:
            self.docx_path = f'{self.argspec.output}/readme.docx'
        if os.path.exists(self.docx_path):
            raise IOError('Same name docx file exist."%s"' % self.docx_path)
        word = client.Dispatch("Word.Application")
        try:
            word.Visible = 0
            doc = word.Documents.Open(self.pdf_path)
            doc.SaveAs(self.docx_path, FileFormat=16)
            doc.Close()
            word.Quit()
            return self.docx_path
        except Exception as err:
            word.Quit()
            return str(err)

    # ==========================================================================
    @staticmethod
    def add_borders(word):
        for table in word.ActiveDocument.Tables:
            table.Borders.Enable = True
            table.Borders.OutsideColorIndex = 16
            table.Borders.InsideColorIndex = 16

    # ==========================================================================
    def add_image(self, word):
        for sp in word.ActiveDocument.InlineShapes:
            sp.Hyperlink.Address = sp.Hyperlink.Address \
                .replace('https://github.com',
                         'https://raw.githubusercontent.com') \
                .replace('blob/', '')
            url = sp.Hyperlink.Address
            filename = url.split('/')[-1]
            if filename.lower().endswith(
                    ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                r = requests.get(url, allow_redirects=True)
                file_path = f'{self.argspec.output}/{filename}'
                open(file_path, 'wb').write(r.content)
                sp.Range.InlineShapes.AddPicture(FileName=file_path,
                                                 LinkToFile=True)
                sp.Delete()
            else:
                r = requests.get(url, allow_redirects=True)
                file_path = f'{self.argspec.output}/{filename}'
                open(file_path, 'wb').write(r.content)

    # ==========================================================================
    @staticmethod
    def add_table_padding(word):
        table_count = word.ActiveDocument.Tables.Count
        for t in range(table_count):
            row_count = word.ActiveDocument.Tables[t].Rows.Count
            for r in range(row_count):
                cell_count = word.ActiveDocument.Tables[t].Rows[r].Cells.Count
                for c in range(cell_count):
                    cell_value = word.ActiveDocument.Tables[t].Rows[r].Cells[c]
                    cell_value.TopPadding = 6
                    cell_value.BottomPadding = 6
                    cell_value.LeftPadding = 13
                    cell_value.RightPadding = 13

    # ==========================================================================
    @staticmethod
    def add_heading_space(word):
        for h in word.ActiveDocument.Paragraphs:
            if 'Heading 1' in str(h.Style):
                h.SpaceAfter = 16
            elif 'Heading 2' in str(h.Style):
                h.SpaceBefore = 24
                h.SpaceAfter = 16
            elif 'Heading 3' in str(h.Style):
                h.SpaceBefore = 24
                h.SpaceAfter = 16
            else:
                pass

    # ==========================================================================
    def html2docx(self):
        if self.argspec.filename:
            self.docx_path = f'{self.argspec.output}/{self.argspec.filename}.docx'
        else:
            self.docx_path = f'{self.argspec.output}/readme.docx'
        if os.path.exists(self.docx_path):
            raise IOError('Same name docx file exist."%s"' % self.docx_path)
        word = client.Dispatch("Word.Application")
        try:
            word.Visible = 0
            doc = word.Documents.Open(self.html_path)
            self.add_borders(word)
            self.add_image(word)
            self.add_table_padding(word)
            self.add_heading_space(word)
            doc.SaveAs(self.docx_path, FileFormat=16)
            doc.Close()
            word.Quit()
            return self.docx_path
        except Exception as err:
            word.Quit()
            return str(err)


################################################################################
@func_log
def reg_op(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        warnings.simplefilter("ignore", ResourceWarning)
        f = Gitmd2docx(argspec)
        f.md2docx()
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
    with ModuleContext(
            owner='ARGOS-LABS-DEMO',
            group='2',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='Git HTML Extract',
            icon_path=get_icon_path(__file__),
            description='MD file to html',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('gitmdlink', display_name='Git MD Link',
                          help='git link to readme.md file')
        mcxt.add_argument('username', display_name='Username',
                          help='Username of git repo')
        mcxt.add_argument('output', display_name='Output Folder',
                          input_method='folderwrite',
                          help='An folder to save the result file')
        # ##################################### for app optional parameters
        mcxt.add_argument('--filename', display_name='File Name',
                          help='File Name without extension and without space')
        mcxt.add_argument('--chromepath', display_name='Chrome Path',
                          help='Chrome Path of system or start chrome command')
        mcxt.add_argument('--word', display_name='Word Editor',
                          action='store_true',
                          help='Word Editor need for docx')
        argspec = mcxt.parse_args(args)
        return reg_op(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
