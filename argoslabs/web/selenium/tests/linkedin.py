# """
# ====================================
#  :mod:`Linkedin_invitation`
# ====================================
# .. moduleauthor:: Irene Cho
# .. note:: ARGOS-LABS License
#
# Description
# ===========
# ARGOS LABS LinkedIn selenium
# """
# # Authors
# # ===========
# #
# # * Irene Cho
# #
# # Change Log
# # --------
# #
# #  * [2021/02/01]
# #     - repeat with csv
#
# ################################################################################
# import os
# import sys
# import csv
# import traceback
# from alabs.common.util.vvlogger import get_logger
# from alabslib.selenium import PySelenium
# from tempfile import gettempdir
# import time
# from selenium.common.exceptions import TimeoutException
#
#
# ################################################################################
# class LinkedIn(PySelenium):
#
#     # ==========================================================================
#     def __init__(self, id, pwd , message, **kwargs):
#         kwargs['url'] = 'https://www.linkedin.com/search/results/people/?currentCompany=%5B%2213310151%22%5D&keywords=rpa&origin=FACETED_SEARCH'
#         self.id = id
#         self.pwd = pwd
#         self.message = message
#         PySelenium.__init__(self, **kwargs)
#         self.logger.zenity_info(f'Starting LinkedIn search')
#         self.cw = csv.writer(sys.stdout, lineterminator='\n')
#         #self.cw.writerow(('index', 'title', 'shipping_fee', 'price', 'shop', 'href'))
#
#     # ==========================================================================
#     @staticmethod
#     def get_safe_text(e, ndx=0):
#         if isinstance(e, list):
#             if not e:
#                 return ''
#             return e[ndx].text
#         return ''
#
#     # ==========================================================================
#     @staticmethod
#     def get_safe_attr(e, attr, ndx=0):
#         if isinstance(e, list):
#             if not e:
#                 return ''
#             return e[ndx].get_attribute(attr)
#         return ''
#
#     # ==========================================================================
#     def do_search(self):
#         try:
#             #Login Page
#             e = self.get_by_xpath('/html/body/div[1]/main/p/a',
#                                   cond='element_to_be_clickable')
#             self.safe_click(e)
#             self.implicitly_wait(after_wait=2)
#
#             #ID
#             #e = self.get_by_xpath('/html/body/div[1]/main/form/section/div[2]/input[1]')
#             e = self.get_by_xpath('/html/body/div/main/div[2]/div[1]/form/div[1]/input')
#             e.send_keys(self.id)
#
#             #PWD
#             e = self.get_by_xpath('/html/body/div/main/div[2]/div[1]/form/div[2]/input')
#             e.send_keys(self.pwd)
#
#             # Login Button
#             e = self.get_by_xpath('/html/body/div/main/div[2]/div[1]/form/div[3]/button',
#                                   cond='element_to_be_clickable',
#                                   move_to_element=True)
#             self.safe_click(e)
#             self.implicitly_wait(after_wait=5)
#
#             for i in range(1,3):
#                 # Click Connect
#                 e = self.get_by_xpath(
#                     f'/html/body/div[7]/div[3]/div/div[2]/div/div[2]/div/div[2]/ul/li[{i}]/div/div/div[3]/button',
#                     cond='element_to_be_clickable',
#                     move_to_element=True)
#                 self.safe_click(e)
#
#                 # Add note
#                 e = self.get_by_xpath(
#                     '/html/body/div[4]/div/div/div[3]/button[1]',
#                     cond='element_to_be_clickable',
#                     move_to_element=True)
#                 self.safe_click(e)
#
#                 # Input message
#                 e = self.get_by_xpath(
#                     '/html/body/div[4]/div/div/div[2]/div/textarea')
#                 e.send_keys(self.message)
#                 self.implicitly_wait(after_wait=10)
#
#                 # Close
#                 e = self.get_by_xpath('/html/body/div[4]/div/div/button',
#                                       cond='element_to_be_clickable',
#                                       move_to_element=True)
#                 self.safe_click(e)
#                 self.implicitly_wait(after_wait=5)
#
#
#             time.sleep(1000)
#
#
#         except Exception as e:
#             _exc_info = sys.exc_info()
#             _out = traceback.format_exception(*_exc_info)
#             del _exc_info
#             self.logger.error('do_search Error: %s\n' % str(e))
#             self.logger.error('%s\n' % ''.join(_out))
#             raise
#
#     # ==========================================================================
#     def start(self):
#         self.do_search()
#
#
# ################################################################################
# def do_start(**kwargs):
#     with LinkedIn(
#             kwargs['id'], kwargs['pwd'],
#             kwargs['message'],
#             browser=kwargs.get('browser', 'Chrome'),
#             width=int(kwargs.get('width', '1200')),
#             height=int(kwargs.get('height', '800')),
#             logger=kwargs['logger']) as ws:
#         ws.start()
#
#
# ################################################################################
# if __name__ == '__main__':
#     log_f = os.path.join(gettempdir(), "GoogleShopping.log")
#     logger = get_logger(log_f, logsize=1024*1024*10)
#     _kwargs = {
#         'browser': 'Chrome',
#         'id':'s',
#         'pwd': 'pwd',
#         'message': 'Sony A7 R3',
#         'logger': logger,
#     }
#     do_start(**_kwargs)
