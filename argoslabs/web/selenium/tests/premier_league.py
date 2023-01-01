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
#  * [2021/02/01]
#     - modify for Eng Win10
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


################################################################################
class PremierLeagure(PySelenium):

    # ==========================================================================
    def __init__(self, **kwargs):
        kwargs['url'] = 'https://www.premierleague.com/tables'
        PySelenium.__init__(self, **kwargs)
        self.logger.info(f'Starting Premier League')
        self.cw = csv.writer(sys.stdout, lineterminator='\n')
        self.cw.writerow(('position', 'club', 'played', 'won', 'drawn', 'lost',
                          'GF', 'GA', 'GD', 'Points'))

    # ==========================================================================
    @staticmethod
    def get_safe_text(e, ndx=0):
        if isinstance(e, list):
            if not e:
                return ''
            return e[ndx].text
        return ''

    # ==========================================================================
    def scrape_table(self):
        try:
            self.implicitly_wait()
            # full path : /html/body/main/div[2]/div[1]/div[5]/div/div/div/table/tbody
            trlist = self.get_by_xpath('//*[@id="mainContent"]/div[2]/div[1]/div[5]/'
                                       'div/div/div/table/tbody')
            rows = trlist.find_elements_by_xpath('tr')  # not (".//*")
            for i, tr in enumerate(rows):
                # skip if class is expandable
                cls = tr.get_attribute('class')
                if cls == 'expandable':
                    continue
                row = list()
                st_ndx = 2
                # position
                # /html/body/main/div[2]/div[1]/div[5]/div/div/div/table/tbody/tr[1]/
                # td[2]/span[1]
                e = tr.find_elements_by_xpath(f'td[{st_ndx+0}]/span[1]')
                row.append(self.get_safe_text(e))
                # club
                e = tr.find_elements_by_xpath(f'td[{st_ndx+1}]/a/span[2]')
                row.append(self.get_safe_text(e))
                # played
                e = tr.find_elements_by_xpath(f'td[{st_ndx+2}]')
                row.append(self.get_safe_text(e))
                # won
                e = tr.find_elements_by_xpath(f'td[{st_ndx+3}]')
                row.append(self.get_safe_text(e))
                # drawn
                e = tr.find_elements_by_xpath(f'td[{st_ndx+4}]')
                row.append(self.get_safe_text(e))
                # lost
                e = tr.find_elements_by_xpath(f'td[{st_ndx+5}]')
                row.append(self.get_safe_text(e))
                # GF
                e = tr.find_elements_by_xpath(f'td[{st_ndx+6}]')
                row.append(self.get_safe_text(e))
                # GA
                e = tr.find_elements_by_xpath(f'td[{st_ndx+7}]')
                row.append(self.get_safe_text(e))
                # GD
                e = tr.find_elements_by_xpath(f'td[{st_ndx+8}]')
                row.append(self.get_safe_text(e))
                # Points
                e = tr.find_elements_by_xpath(f'td[{st_ndx+9}]')
                row.append(self.get_safe_text(e))
                self.cw.writerow(row)

        except Exception as e:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('scrape_table Error: %s\n' % str(e))
            self.logger.error('%s\n' % ''.join(_out))
            raise

    # ==========================================================================
    def start(self):
        self.scrape_table()


################################################################################
def do_start(**kwargs):
    with PremierLeagure(
            browser=kwargs.get('browser', 'Chrome'),
            width=int(kwargs.get('width', '1200')),
            height=int(kwargs.get('height', '800')),
            logger=kwargs['logger']) as ws:
        ws.start()
        return 0


################################################################################
if __name__ == '__main__':
    log_f = os.path.join(gettempdir(), "PremierLeagure.log")
    logger = get_logger(log_f, logsize=1024*1024*10)
    _kwargs = {
        'browser': 'Chrome',
        # 'browser': 'Edge',
        'logger': logger,
    }
    do_start(**_kwargs)
