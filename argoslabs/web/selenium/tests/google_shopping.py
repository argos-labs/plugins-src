"""
====================================
 :mod:`google_shopping`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Rossum API unittest module
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/01/31]
#     - repeat with csv

################################################################################
import os
import sys
import csv
import traceback
from alabs.common.util.vvlogger import get_logger
from alabslib.selenium import PySelenium
from tempfile import gettempdir
from selenium.common.exceptions import TimeoutException


################################################################################
class GoogleShopping(PySelenium):

    # ==========================================================================
    def __init__(self, search, **kwargs):
        kwargs['url'] = 'https://www.google.com/'
        self.search = search
        PySelenium.__init__(self, **kwargs)
        self.logger.info(f'Starting Google Shopping search "{search}"')
        self.cw = csv.writer(sys.stdout, lineterminator='\n')
        self.cw.writerow(('index', 'title', 'shipping_fee', 'price', 'shop', 'href'))

    # ==========================================================================
    @staticmethod
    def get_safe_text(e, ndx=0):
        if isinstance(e, list):
            if not e:
                return ''
            return e[ndx].text
        return ''

    # ==========================================================================
    @staticmethod
    def get_safe_attr(e, attr, ndx=0):
        if isinstance(e, list):
            if not e:
                return ''
            return e[ndx].get_attribute(attr)
        return ''

    # ==========================================================================
    def do_search(self):
        try:
            # Search
            e = self.get_by_xpath('/html/body/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input')
            e.send_keys(self.search)

            # Search button
            e = self.get_by_xpath('/html/body/div[2]/div[2]/form/div[2]/div[1]/div[3]/center/input[1]',
                                  cond='element_to_be_clickable',
                                  move_to_element=True)
            self.safe_click(e)
            self.implicitly_wait()

            # Shopping Group
            e = self.get_by_xpath('//*[@id="hdtb-msb-vis"]/div[4]/a',
                                  cond='element_to_be_clickable')
            self.safe_click(e)
            self.implicitly_wait()

            #
            try:
                glist = self.get_by_xpath('//*[@id="rso"]/div[2]/div[2]/div',
                                          timeout=2)
            except TimeoutException as er:
                glist = self.get_by_xpath('//*[@id="rso"]/div/div[2]/div',
                                          timeout=2)
            gls = glist.find_elements_by_xpath('div')  # ".//*")
            for i, ge in enumerate(gls):
                # scrool into view
                self.driver.execute_script('arguments[0].scrollIntoView();', ge)
                row = list()
                # index
                row.append(f'{i+1}')
                # title of goods
                e = ge.find_elements_by_xpath('div/div/div[2]/a/h4')
                row.append(self.get_safe_text(e))
                # shipping_fee of goods
                e = ge.find_elements_by_xpath('div/div/div[2]/div[2]')
                row.append(self.get_safe_text(e))
                # price of goods
                e = ge.find_elements_by_xpath('div/div/div[2]/div[4]/div/div[2]/span/span[1]/span')
                row.append(self.get_safe_text(e))
                # shop of goods
                e = ge.find_elements_by_xpath('div/div/div[2]/div[4]/div/div[2]/a')
                row.append(self.get_safe_text(e))
                # link of goods
                row.append(self.get_safe_attr(e, 'href'))
                self.cw.writerow(row)

        except Exception as e:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('do_search Error: %s\n' % str(e))
            self.logger.error('%s\n' % ''.join(_out))
            raise

    # ==========================================================================
    def start(self):
        self.do_search()


################################################################################
def do_start(**kwargs):
    with GoogleShopping(
            kwargs['search'],
            browser=kwargs.get('browser', 'Chrome'),
            width=int(kwargs.get('width', '1200')),
            height=int(kwargs.get('height', '800')),
            logger=kwargs['logger']) as ws:
        ws.start()
        return 0


################################################################################
if __name__ == '__main__':
    log_f = os.path.join(gettempdir(), "GoogleShopping.log")
    logger = get_logger(log_f, logsize=1024*1024*10)
    _kwargs = {
        'browser': 'Chrome',
        # 'browser': 'Edge',
        # 'search': 'New Balance 608 7 ½ 4E',
        # 'search': 'New Balance 608 7 1/2 4E',
        'search': 'Sony A7 R3',
        'logger': logger,
    }
    do_start(**_kwargs)
