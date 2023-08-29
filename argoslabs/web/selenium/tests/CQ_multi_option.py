"""
====================================
 :mod:`multi_option`
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
#  * [2023/01/18]
#     - starting

################################################################################
import os
import sys
import traceback
from alabs.common.util.vvlogger import get_logger
from alabslib.selenium import PySelenium
from tempfile import gettempdir
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

################################################################################
class SSExample(PySelenium):

    # ==========================================================================
    def __init__(self, **kwargs):
        kwargs['url'] = 'https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_select_multiple'
        PySelenium.__init__(self, **kwargs)
        self.logger.info(f'Starting multiple option select Example...')

    # ==========================================================================
    def multi_select(self):
        try:
            self.switch_to_iframe('//iframe[@id="iframeResult"]')
            # multiple select
            item_1 = self.get_by_xpath('(//select[@id="cars"]/option)[1]')
            item_3 = self.get_by_xpath('(//select[@id="cars"]/option)[3]')
            ActionChains(self.driver).key_down(Keys.CONTROL).click(item_1).key_up(Keys.CONTROL).perform()
            ActionChains(self.driver).key_down(Keys.CONTROL).click(item_3).key_up(Keys.CONTROL).perform()
            # Submit button
            e = self.get_by_xpath('//input[@type="submit"]', move_to_element=True)
            self.safe_click(e)
            self.implicitly_wait(after_wait=30)
        except Exception as e:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('add_data Error: %s\n' % str(e))
            self.logger.error('%s\n' % ''.join(_out))

    # ==========================================================================
    def start(self):
        self.multi_select()


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
