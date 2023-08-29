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
#  * [2021/05/31]
#     - starting

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
class YahooFinance(PySelenium):

    # ==========================================================================
    def __init__(self, **kwargs):
        kwargs['url'] = 'https://finance.yahoo.com/'
        PySelenium.__init__(self, **kwargs)
        self.logger.info(f'Starting Yahoo Finance top most')
        self.cw = csv.writer(sys.stdout, lineterminator='\n')
        self.cw.writerow(('symbol', 'name', 'price', 'change', 'change%', 'volume', '3-m-avg-vol', 'cap', 'ttm', '52weeks'))

    # ==========================================================================
    def get_most_active(self):
        try:
            # Click 
            e = self.get_by_xpath('//*[@id="data-util-col"]/section[5]/header/a',
                                  cond='element_to_be_clickable',
                                  move_to_element=True)
            self.safe_click(e)
            self.implicitly_wait()

            # tbody
            tbody = self.get_by_xpath('//*[@id="scr-res-table"]/div[1]/table/tbody',
                                      timeout=2)
            trs = tbody.find_elements_by_xpath('tr')
            for i, tre in enumerate(trs):
                # scrool into view
                self.driver.execute_script('arguments[0].scrollIntoView();', tre)
                row = list()
                tds = tre.find_elements_by_xpath('td')
                for j, tde in enumerate(tds):
                    row.append(tde.text)
                self.cw.writerow(row)

        except Exception as e:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('get_most_active Error: %s\n' % str(e))
            self.logger.error('%s\n' % ''.join(_out))
            raise

    # ==========================================================================
    def start(self):
        self.get_most_active()


################################################################################
def do_start(**kwargs):
    with YahooFinance(
            browser=kwargs.get('browser', 'Chrome'),
            headless=kwargs.get('headless', False),
            width=int(kwargs.get('width', '1200')),
            height=int(kwargs.get('height', '800')),
            logger=kwargs['logger']) as ws:
        ws.start()
        return 0


################################################################################
if __name__ == '__main__':
    log_f = os.path.join(gettempdir(), "YahooFinance.log")
    logger = get_logger(log_f, logsize=1024*1024*10)
    _kwargs = {
        'browser': 'Edge',
        # 'browser': 'Chrome',
        'headless': True,
        'logger': logger,
    }
    do_start(**_kwargs)
