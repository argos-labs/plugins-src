"""
====================================
 :mod:`CQ_dynamic_selector`
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
#  * [2023/01/30]
#     - starting

################################################################################
import os
import sys
import traceback
from alabs.common.util.vvlogger import get_logger
from alabslib.selenium import PySelenium
from tempfile import gettempdir


################################################################################
class SSExample(PySelenium):

    # ==========================================================================
    def __init__(self, **kwargs):
        kwargs['url'] = 'http://localhost:8000'
        PySelenium.__init__(self, **kwargs)
        self.logger.info(f'Starting dynamic selector Example...')

    # ==========================================================================
    def dynamic_selector(self):
        try:
            e = self.get_by_xpath('(//table[@per="ilbo"]/tbody/tr[7]//div[@class="x-grid-item-container"])[1]')
            tables_e = e.find_elements_by_xpath('./table')
            for table_e in tables_e:
                tds_e = table_e.find_elements_by_xpath('./tbody/tr/td')
                t_combo = tds_e[2].text
                t_name = tds_e[4].text
                t_code = tds_e[5].text
                print(t_combo, t_name, t_code)
        except Exception as e:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('add_data Error: %s\n' % str(e))
            self.logger.error('%s\n' % ''.join(_out))

    # ==========================================================================
    def start(self):
        self.dynamic_selector()


################################################################################
def do_start(**kwargs):
    with SSExample(
            browser=kwargs.get('browser', 'Chrome'),
            width=int(kwargs.get('width', '1200')),
            height=int(kwargs.get('height', '800')),
            logger=kwargs['logger']) as ws:
        ws.start()
        return 0


################################################################################
if __name__ == '__main__':
    log_f = os.path.join(gettempdir(), "multi_option.log")
    logger = get_logger(log_f, logsize=1024*1024*10)
    _kwargs = {
        'browser': 'Chrome',
        # 'browser': 'Edge',
        'logger': logger,
    }
    do_start(**_kwargs)
