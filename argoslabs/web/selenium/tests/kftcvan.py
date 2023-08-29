"""
====================================
 :mod:`kftcvan`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Selenium test
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2022/10/05]
#     - starting: 12일까지 풀어달라고 영준팀장이 부탁

################################################################################
import os
import sys
import traceback
from alabs.common.util.vvlogger import get_logger
from alabslib.selenium import PySelenium
from tempfile import gettempdir
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


################################################################################
class KFTCExample(PySelenium):

    # ==========================================================================
    def __init__(self, userid, passwd, **kwargs):
        kwargs['url'] = 'https://www.kftcvan.or.kr/member/login/form.do'
        self.userid = userid
        self.passwd = passwd
        PySelenium.__init__(self, **kwargs)
        self.logger.info(f'Starting KFTC VAN... "{userid}"')

    # ==========================================================================
    def login(self):
        try:
            # userid
            e = self.get_by_xpath('//input[@name="usr_id"]')
            e.send_keys(self.userid)

            # passwd
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.TAB)
            actions.perform()

            # e.send_keys(Keys.TAB)
            # self.send_keys_clipboard(e, Keys.TAB)
            e.send_keys(self.passwd)
            # e = self.get_by_xpath('//input[@id="passWd"]')
            # # e.send_keys(self.passwd)
            # self.safe_click(e)
            # self.send_keys_clipboard(e, self.passwd)

            # login button
            e.send_keys(Keys.ENTER)
            # e = self.get_by_xpath('//a[@class="btn_login"]')
            # self.safe_click(e)

            self.implicitly_wait(after_wait=3)
        except Exception as e:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('add_data Error: %s\n' % str(e))
            self.logger.error('%s\n' % ''.join(_out))

    # ==========================================================================
    def start(self):
        self.login()


################################################################################
def do_start(**kwargs):
    if not ('userid' in kwargs and 'passwd' in kwargs):
        raise ValueError(f'Invalid "userid", "passwd" or "birth_place" parameters')
    with KFTCExample(
            kwargs['userid'],
            kwargs['passwd'],
            browser=kwargs.get('browser', 'Chrome'),
            width=int(kwargs.get('width', '1200')),
            height=int(kwargs.get('height', '800')),
            logger=kwargs['logger']) as ws:
        ws.start()
        return 0


################################################################################
if __name__ == '__main__':
    log_f = os.path.join(gettempdir(), "SSExample.log")
    logger = get_logger(log_f, logsize=1024*1024*10)
    _kwargs = {
        'browser': 'Chrome',
        # 'browser': 'Edge',
        'userid': 'A43',
        'passwd': 'a86060547!',
        'logger': logger,
    }
    do_start(**_kwargs)
