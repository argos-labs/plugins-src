"""
====================================
 :mod:`mcchae-egloos`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS extract all articals from mcchae.egloos.com
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/28]
#     - try to save folder
#  * [2021/03/11]
#     - starting

################################################################################
import os
import sys
import pprint
import traceback
from alabs.common.util.vvlogger import get_logger
from alabslib.selenium import PySelenium
# from tempfile import gettempdir


################################################################################
class ExtractEgloos(PySelenium):

    # ==========================================================================
    @staticmethod
    def _get_safe_filename(fn):
        return "".join([c for c in fn if c.isalpha() or c.isdigit() or c == ' ']).rstrip()

    # ==========================================================================
    def __init__(self, output_folder, category, **kwargs):
        self.output_folder = output_folder
        self.category = category
        # for internal
        self.wdir = os.path.join(self.output_folder, self._get_safe_filename(self.category))
        if not os.path.exists(self.wdir):
            os.makedirs(self.wdir)
        kwargs['url'] = f'http://mcchae.egloos.com/category/{category}'
        PySelenium.__init__(self, **kwargs)
        self.logger.info(f'Starting extracting ... "{category}"')
        self.page = {}

    # ==========================================================================
    def _write(self, e, sl):
        children = e.find_elements_by_xpath(".//*")
        if children:
            for ce in children:
                self._write(ce, sl)
        else:
            if e.text:
                sl.append(e.text)

    # ==========================================================================
    def do_page(self):
        try:
            self.page = {}
            self.page['egloos_url'] = self.driver.current_url
            self.page['egloos_page_id'] = self.driver.current_url.split('/')[-1]
            # title
            e = self.get_by_xpath(f'//*[@id="section_content"]/div[1]/div/div[1]/div/h2/a')
            self.page['title'] = e.get_attribute('title')
            # 댓글수
            e = self.get_by_xpath(f'//*[@id="section_content"]/div[1]/div/div[2]/ul/li[4]')
            v = e.text  # '덧글수 : 0'
            v = v.split(':')[1].strip()
            self.page['num_reply'] = v
            
            # text contents :       //*[@id="section_content"]/div[1]/div/div[2]/div[1]
            e = self.get_by_xpath(f'//*[@id="section_content"]/div[1]/div/div[2]/div[1]')
            sl = list()
            # v = e.get_attribute('innerText')
            self._write(e, sl)
            self.page['contents_text'] = v

            pprint.pprint(self.page)
            self.driver.execute_script("window.history.go(-1)")
            self.implicitly_wait()
        except Exception as e:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('do_list_page Error: %s\n' % str(e))
            self.logger.error('%s\n' % ''.join(_out))

    # ==========================================================================
    def do_list_page(self):
        try:
            for i in range(10):
                # Name : //*[@id="titlelist_list"]/ul/li[10]/a
                try:
                    e = self.get_by_xpath(f'//*[@id="titlelist_list"]/ul/li[{i+1}]/a',
                                        cond='element_to_be_clickable',
                                        move_to_element=True,
                                        timeout=1)
                    self.safe_click(e)
                    self.implicitly_wait()
                    self.do_page()
                except:
                    break
        except Exception as e:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('do_list_page Error: %s\n' % str(e))
            self.logger.error('%s\n' % ''.join(_out))

    # ==========================================================================
    def start(self):
        self.do_list_page()


################################################################################
def do_start(**kwargs):
    with ExtractEgloos(
            kwargs['output_folder'],
            kwargs['category'],
            browser=kwargs.get('browser', 'Chrome'),
            width=int(kwargs.get('width', '1200')),
            height=int(kwargs.get('height', '800')),
            logger=kwargs['logger']) as ws:
        ws.start()


################################################################################
if __name__ == '__main__':
    _output_folder = '/Users/mcchae/work/Books/Egloos'
    if not os.path.exists(_output_folder):
        os.makedirs(_output_folder)
    log_f = os.path.join(_output_folder, "ExtractEgloos.log")
    logger = get_logger(log_f, logsize=1024*1024*10)
    _kwargs = {
        'browser': 'Chrome',
        'output_folder': _output_folder,
        'category': 'Develop%20Tip',
        'logger': logger,
    }
    do_start(**_kwargs)
