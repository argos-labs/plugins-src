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
class SSExample(PySelenium):

    # ==========================================================================
    def __init__(self, csv_file, csv_encoding, **kwargs):
        kwargs['url'] = 'https://docs.google.com/forms/d/e/1FAIpQLSckvF5F81nJUU' \
                        'U1D_bJr4DJEQlm8Lxhr_ESG1Oi3Yfw5OCAcg/viewform?hl=en'
        self.csv_file = csv_file
        self.csv_encoding = csv_encoding
        PySelenium.__init__(self, **kwargs)
        self.logger.info(f'Starting ARGOS LABS Web Form Example... CSV "{csv_file}"')
        self.cw = csv.writer(sys.stdout, lineterminator='\n')
        self.cw.writerow(('name', 'dob', 'birth_place'))

    # ==========================================================================
    def add_data(self, name, dob, birth_place):
        try:
            # Name
            e = self.get_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/'
                                  'div/div[2]/div/div[1]/div/div[1]/input')
            e.send_keys(name)

            # BOD
            e = self.get_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/'
                                  'div/div[2]/div/div[1]/div/div[1]/input')
            e.send_keys(dob)

            # Birth Place
            e = self.get_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/'
                                  'div/div[2]/div/div[1]/div/div[1]/input')
            e.send_keys(birth_place)

            # Submit button
            e = self.get_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div',
                                  cond='element_to_be_clickable',
                                  move_to_element=True)
            # self.implicitly_wait(after_wait=2)
            self.safe_click(e)
            self.implicitly_wait()
            _ = self.get_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[2]',
                                  cond='text_to_be_present_in_element',
                                  cond_text='Solution Intro - Excel to Web',
                                  timeout=2)
            e = self.get_by_xpath(
                '/html/body/div[1]/div[2]/div[1]/div/div[4]/a',
                cond='element_to_be_clickable',
                move_to_element=True)
            self.safe_click(e)
            self.implicitly_wait()
            self.cw.writerow((name, dob, birth_place))
        except Exception as e:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('add_data Error: %s\n' % str(e))
            self.logger.error('%s\n' % ''.join(_out))

    # ==========================================================================
    def start(self):
        if not os.path.exists(self.csv_file):
            raise IOError(f'Cannot find CSV file "{self.csv_file}"')
        with open(self.csv_file, 'r', encoding=self.csv_encoding) as ifp:
            row_count = sum(1 for _ in ifp)
            ifp.seek(0)
            cr = csv.reader(ifp)
            for i, row in enumerate(cr):
                if i == 0:
                    continue
                self.logger.info(f'adding data [{i}/{row_count-1}]')
                self.add_data(row[0], row[-2], row[-1])


################################################################################
def do_start(**kwargs):
    with SSExample(
            kwargs['csv_file'],
            kwargs['csv_encoding'],
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
        'csv_file': 'ss_sample.csv',
        'csv_encoding': 'utf-8',
        'logger': logger,
    }
    do_start(**_kwargs)
