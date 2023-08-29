#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.sns.whatsapp`
====================================
.. moduleauthor:: arun kumar <ak080495@gmail.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module sample
"""
# Authors
# ===========
#
# * arun kumar
# * Jerry Chae <mcchae@argos-labs.com>
#
# Change Log
# --------
#
#  * [2020/05/18]
#     - Code review by Jerry Chae
#  * [2020/05/11]
#     - starting

################################################################################
import os
import sys
import csv
import time
import xlrd
from alabs.common.util.vvargs import \
    ModuleContext, func_log, ArgsError, ArgsExit, get_icon_path
# noinspection PyPackageRequirements
from selenium import webdriver
# noinspection PyPackageRequirements
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
################################################################################
# from collections import OrderedDict
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

################################################################################
def new_chat(web_driver, user_name):

    new_user = WebDriverWait(web_driver, 300).until(

        ec.presence_of_element_located((By.XPATH,
                                        '//div[@class="_3FRCZ copyable-text selectable-text"]')))

    new_user.send_keys(user_name)
    new_user.send_keys(Keys.ENTER)


################################################################################
@func_log
def whatsapp(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    web_driver = None
    # print(web_driver)
    try:
        if argspec.driver == 'Chrome':
            web_driver = webdriver.Chrome(
                executable_path=argspec.driver_path
            )
        else:
            raise RuntimeError(f'Not supported Selenium Web Driver "{argspec.driver}"')
        web_driver.get('https://web.whatsapp.com/')
        _ = WebDriverWait(web_driver, 30).until(
            ec.presence_of_element_located(
                (By.XPATH, '//canvas[@aria-label="Scan me!"]'))
        )
        filepath = argspec.filepath
        message = argspec.msg

        friends = []
        if argspec.friendsfiletype == 'csv':
            with open(argspec.friends, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for line in csv_reader:
                    abc = dict(line)
                    friends.append(abc['name'])
        elif argspec.friendsfiletype == 'text':
            user_name_list = argspec.friends
            friends = user_name_list.split(',')
        elif argspec.friendsfiletype == 'xlsx':
            loc = (argspec.friends,)
            wb = xlrd.open_workbook(loc)
            sheet = wb.sheet_by_index(0)
            sheet.cell_value(0, 0)
            friends = []
            for i in range(1, sheet.nrows):
                for j in range(sheet.ncols):
                    if sheet.cell_value(0, j) == "name":
                        if type(sheet.cell_value(i, j)) == float:
                            friends.append(str(int(sheet.cell_value(i, j))))
                        else:
                            friends.append(str(sheet.cell_value(i, j)))
        else:
            print("for new choice")
        for user_name in friends:
            try:
                if not user_name.isdigit():
                    user = WebDriverWait(web_driver, 5).until(
                        ec.presence_of_element_located((By.XPATH,
                                                        '//span[@title="{}"]'.format(
                                                            user_name))))
                    user.click()
                else:
                    new_chat(web_driver, user_name)  # if name not found

            except TimeoutException:
                new_chat(web_driver, user_name)  # if name not found

            except NoSuchElementException:
                new_chat(web_driver, user_name)  # if name not found

            if not filepath:
                message_box = WebDriverWait(web_driver, 30).until(
                    ec.presence_of_element_located(
                        (By.XPATH,
                         '//div[@class="_3FRCZ copyable-text selectable-text"][@contenteditable="true"][@data-tab="1"]')
                    )
                )
                message_box.send_keys(message + Keys.ENTER)

            elif not message:

                attachment_box = WebDriverWait(web_driver, 30).until(

                    ec.presence_of_element_located((By.XPATH,
                                                    '//div[@title = "Attach"]')))

                attachment_box.click()

                image_box = WebDriverWait(web_driver, 30).until(

                    ec.presence_of_element_located((By.XPATH,
                                                    '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
                image_box.send_keys(filepath)

                send_button = WebDriverWait(web_driver, 300).until(

                    ec.presence_of_element_located((By.XPATH,
                                                    '//span[@data-icon="send"]')))
                send_button.click()

            else:
                message_box = WebDriverWait(web_driver, 30).until(
                    ec.presence_of_element_located((By.XPATH,
                                                    #     '//div[@class="_1Plpp"]'
                                                    '//div[@class="_3FRCZ copyable-text selectable-text"][@contenteditable="true"][@data-tab="1"]')))
                # class name some time changes so take a look on the class
                message_box.send_keys(message + Keys.ENTER)
                # ###message send######
                attachment_box = WebDriverWait(web_driver, 30).until(
                    ec.presence_of_element_located((By.XPATH,
                                                    '//div[@title = "Attach"]')))
                attachment_box.click()
                image_box = WebDriverWait(web_driver, 30).until(

                    ec.presence_of_element_located((By.XPATH,
                                                    '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
                image_box.send_keys(filepath)
                # gnored_exceptions=InterruptedError    it will fix Interrupted error it comes when click happens on outer div
                send_button = WebDriverWait(web_driver, 60, ignored_exceptions=InterruptedError).until(
                    ec.presence_of_element_located((By.XPATH,
                                                    # '//span[@data-icon="send-light"]')))
                                                    '//span[@data-icon="send"]')))
                send_button.click()

        time.sleep(10)  # needed for last file upload
        result = "message send to" + " " + str(friends) + " " + "sussessfully"
        print(result, end='')
        mcxt.logger.info('>>>end...')
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        if web_driver is not None:
            # web_driver.close()
            # print("quit")
            web_driver.quit()
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
        owner='Rooman',
        group='sns',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Whatsapp Rooman',
        icon_path=get_icon_path(__file__),
        description='send message whatsapp friends',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('msg',
                          display_name='message',
                          help='type message to send')
        mcxt.add_argument('friendsfiletype',
                          # nargs='+',
                          default='csv',
                          choices=['csv', 'text', 'xlsx'],
                          display_name='Friends file type',
                          help='type your friends name')

        mcxt.add_argument('friends',
                          # nargs='+',
                          display_name='Friends list',
                          input_method='fileread',
                          help='type or upload friends name')
        # ##################################### for app dependent options
        mcxt.add_argument('--driver', '-d',
                          default='Chrome',
                          choices=['Chrome'],
                          # choices=['Chrome', 'MS Edge', 'MSIE', 'Firefox'],
                          display_name='Web Browser',
                          help='Selenium web driver type to automate')
        mcxt.add_argument('--driver-path',
                          input_method='fileread',
                          display_name='Web driver path',
                          help='Select web driver path')
        mcxt.add_argument('--filepath', action='append',
                          input_method='fileread',
                          display_name='send file',
                          help='give path of img/video')
        argspec = mcxt.parse_args(args)
        return whatsapp(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
