"""
====================================
 :mod:`af_req_01`
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
#  * [2022/10/07]
#     - starting

################################################################################
import os
import sys
import csv
import traceback
from alabs.common.util.vvlogger import get_logger
from alabslib.selenium import PySelenium
from tempfile import gettempdir
from urllib import parse


################################################################################
class TruckList(PySelenium):

    # ==========================================================================
    @staticmethod
    def _build_url(search_keywords):
        # build url
        url = 'https://ryder.com/used-trucks/inventory?facets='
        for sk in search_keywords.split(','):
            sk = sk.strip()
            url += f'group={parse.quote(sk)};'
        url += '&view=crd'
        return url

    # ==========================================================================
    def __init__(self, search_keywords, **kwargs):
        self.search_keywords = search_keywords
        # kwargs['url'] = 'https://ryder.com/used-trucks/inventory?facets=group=SINGLE%20AXLE%20TRACTOR;group=SINGLE%20AXLE%20DAYCAB%20TRACTOR;group=S/A%20TRACTORS;&view=crd'
        kwargs['url'] = self._build_url(search_keywords)
        self.search_keywords = search_keywords
        PySelenium.__init__(self, **kwargs)
        self.logger.info(f'Starting Web Extracting Example...')
        self.cw = csv.writer(sys.stdout, lineterminator='\n')
        self.row_cnt = 0
        self.cw.writerow(('certified', 'title', 'price', 'miles', 'year', 'vehnum', 'location'))

    # ==========================================================================
    def get_page(self):
        try:
            self.implicitly_wait()
            # selarch list
            sl_e = self.get_by_xpath('//div[@class="search-results-container"]/ul')
            for s_e in sl_e.find_elements_by_xpath('.//div[@class="result-item-info"]'):
                self.driver.execute_script('arguments[0].scrollIntoView();', s_e)
                row = list()
                # certified
                e = s_e.find_element_by_xpath('.//div[@class="certified"]')
                row.append(e.text.strip())
                # title
                e = s_e.find_element_by_xpath('.//div[@class="title"]')
                row.append(e.text.strip())
                # price
                e = s_e.find_element_by_xpath('.//div[@class="price"]')
                txt = e.text.strip()
                if txt.endswith(' USD'):
                    txt = txt[:-4]
                row.append(txt)
                # miles
                e = s_e.find_element_by_xpath('.//div[@class="miles"]')
                txt = e.text.strip()
                if txt.startswith('Miles : '):
                    txt = txt[8:]
                row.append(txt)
                # year
                e = s_e.find_element_by_xpath('.//div[@class="year"]')
                txt = e.text.strip()
                if txt.startswith('Year: '):
                    txt = txt[6:]
                row.append(txt)
                # vehnum
                e = s_e.find_element_by_xpath('.//div[@class="vehicle-number"]')
                txt = e.text.strip()
                if txt.startswith('VEH #: '):
                    txt = txt[7:]
                row.append(txt)
                # location
                e = s_e.find_element_by_xpath('.//div[@class="location"]')
                row.append(e.text.strip())
                # write row
                self.cw.writerow(row)
                self.row_cnt += 1
            try:
                pg_e = self.get_by_xpath('//div[@class="pagination-plp"]')
                np_e = pg_e.find_element_by_xpath('.//div[3]/a')
                _title = np_e.get_attribute('title')
                _class = np_e.get_attribute('class')
                if _class == 'disabled':
                    return False
                self.safe_click(np_e)
                return True
            except:
                return False
        except Exception as e:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('add_data Error: %s\n' % str(e))
            self.logger.error('%s\n' % ''.join(_out))

    # ==========================================================================
    def start(self):
        while True:
            if not self.get_page():
                break
        # print(f'# of rows: {self.row_cnt}')


################################################################################
def do_start(**kwargs):
    if not ('search_keywords' in kwargs):
        raise ValueError(f'Invalid "search_keywords" parameters')
    with TruckList(**kwargs) as ws:
        ws.start()
    return 0


################################################################################
if __name__ == '__main__':
    log_f = os.path.join(gettempdir(), "TruckList.log")
    logger = get_logger(log_f, logsize=1024*1024*10)
    # search_keywords = [
    #     'SINGLE AXLE TRACTOR',
    #     'SINGLE AXLE DAYCAB TRACTOR',
    #     'S/A TRACTORS',
    # ]
    _kwargs = {
        'browser': 'Chrome',
        # 'headless': True,
        # 'browser': 'Edge',
        'search_keywords': 'SINGLE AXLE TRACTOR,SINGLE AXLE DAYCAB TRACTOR,S/A TRACTORS',
        'logger': logger,
    }
    do_start(**_kwargs)
