"""
====================================
 :mod:`ss_sample_01`
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
#  * [2021/01/27]
#     - starting

################################################################################
import os
import sys
import csv
import traceback
from alabs.common.util.vvlogger import get_logger
from alabslib.selenium import PySelenium
from tempfile import gettempdir


################################################################################
class SSExample(PySelenium):

    # ==========================================================================
    def __init__(self, name, dob, birth_place, **kwargs):
        kwargs['url'] = 'https://docs.google.com/forms/d/e/1FAIpQLSckvF5F81nJUUU' \
                        '1D_bJr4DJEQlm8Lxhr_ESG1Oi3Yfw5OCAcg/viewform?hl=en'
        self.name = name
        self.dob = dob
        self.birth_place = birth_place
        PySelenium.__init__(self, **kwargs)
        self.logger.info(f'Starting ARGOS LABS Web Form Example... "{name}"')
        self.cw = csv.writer(sys.stdout, lineterminator='\n')
        self.cw.writerow(('name', 'dob', 'birth_place'))

    # ==========================================================================
    def add_data(self):
        try:
            # Name
            e = self.get_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/'
                                  'div/div[2]/div/div[1]/div/div[1]/input')
            e.send_keys(self.name)

            # dob
            e = self.get_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/'
                                  'div/div[2]/div/div[1]/div/div[1]/input')
            e.send_keys(self.dob)

            # Birth Place
            e = self.get_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/'
                                  'div/div[2]/div/div[1]/div/div[1]/input')
            e.send_keys(self.birth_place)

            # Submit button
            e = self.get_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div',
                                  cond='element_to_be_clickable',
                                  move_to_element=True)
            self.implicitly_wait(after_wait=2)
            self.safe_click(e)
            self.implicitly_wait(after_wait=3)
            self.cw.writerow((self.name, self.dob, self.birth_place))
        except Exception as e:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('add_data Error: %s\n' % str(e))
            self.logger.error('%s\n' % ''.join(_out))

    # ==========================================================================
    def start(self):
        self.add_data()


################################################################################
def do_start(**kwargs):
    if not ('name' in kwargs and 'dob' in kwargs and 'birth_place' in kwargs):
        raise ValueError(f'Invalid "name", "dob" or "birth_place" parameters')
    with SSExample(
            kwargs['name'],
            kwargs['dob'],
            kwargs['birth_place'],
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
        # 'browser': 'Chrome',
        'browser': 'Edge',
        'name': 'kairoslab99',
        'dob': '1999-01-01',
        'birth_place': 'San Jose, CA USA',
        'logger': logger,
    }
    do_start(**_kwargs)
