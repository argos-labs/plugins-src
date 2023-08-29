#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.arun.text`
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
#
# Change Log
# --------
#
#  * [2019/03/08]
#     - add icon
#  * [2018/11/28]
#     - starting

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from selenium import webdriver
import time,sys
from selenium.common.exceptions import NoSuchElementException

################################################################################
@func_log
def whatsapp(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        def new_chat(user_name):
            new_chat = chrome_browser.find_element_by_xpath(
                '//div[@class="gQzdc"]')
            new_chat.click()

            new_user = chrome_browser.find_element_by_xpath(
                '//div[@class="_2S1VP copyable-text selectable-text"]')
            new_user.send_keys(user_name)

            time.sleep(1)

            try:
                user = chrome_browser.find_element_by_xpath(
                    '//span[@title="{}"]'.format(user_name))
                user.click()
            except NoSuchElementException:
                print('Given user "{}" not found in the contact list'.format(
                    user_name))
                user = chrome_browser.find_element_by_xpath(
                    '//span[@title]'.format(user_name))
                user.click()

            except Exception as e:
                chrome_browser.close()
                print(e)
                sys.exit()

        chrome_browser = webdriver.Chrome(
            executable_path=
            argspec.path
            # 'C:\work\packages\chromedriver_win32\chromedriver'
        )
        chrome_browser.get('https://web.whatsapp.com/')

        time.sleep(15)
        filepath = argspec.filepath

        message = argspec.msg
        outstr = argspec.friends
        user_name_list = outstr.split(',')

        for user_name in user_name_list:

            try:
                user = chrome_browser.find_element_by_xpath(
                    '//span[@title="{}"]'.format(user_name))
                user.click()
            except NoSuchElementException as se:
                new_chat(user_name)   #if name not found

            if not filepath:
                # print("Empty String!")
                time.sleep(5)
                message_box = chrome_browser.find_element_by_xpath(
                    '//div[@class="_1Plpp"]')
                message_box.send_keys(message
                                      )
                time.sleep(5)
                message_box = chrome_browser.find_element_by_xpath(
                    '//button[@class="_35EW6"]')

                message_box.click()
            elif not message:

                time.sleep(5)
                attachment_box = chrome_browser.find_element_by_xpath(
                    '//div[@title = "Attach"]')

                attachment_box.click()

                image_box = chrome_browser.find_element_by_xpath(
                    '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
                image_box.send_keys(filepath)

                time.sleep(10)
                send_button = chrome_browser.find_element_by_xpath(
                    '//span[@data-icon="send-light"]')
                send_button.click()
                time.sleep(10)

            else:
                time.sleep(5)
                message_box = chrome_browser.find_element_by_xpath(
                    '//div[@class="_1Plpp"]')

                message_box.send_keys(message

                                      )
                time.sleep(5)
                message_box = chrome_browser.find_element_by_xpath(
                    '//button[@class="_35EW6"]')

                message_box.click()
                time.sleep(5)
                attachment_box = chrome_browser.find_element_by_xpath(
                    '//div[@title = "Attach"]')

                attachment_box.click()

                image_box = chrome_browser.find_element_by_xpath(
                    '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
                image_box.send_keys(filepath)

                time.sleep(10)
                send_button = chrome_browser.find_element_by_xpath(
                    '//span[@data-icon="send-light"]')
                send_button.click()
                time.sleep(10)
        chrome_browser.close()



        result = "message send to" + " " + outstr+ " " + "sussessfully"
        print(result, end='')
        mcxt.logger.info('>>>end...')
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
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
        owner='ARGOS-LABS-DEMO',
        group='Rooman',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Whatsapp Rooman',
        icon_path=get_icon_path(__file__),
        description='send message whatsapp friends',
    ) as mcxt:
        # ##################################### for app dependent parameters

        mcxt.add_argument('friends',
                          display_name='Friends Name',
                          help='type your friends name')
        mcxt.add_argument('path',
                          display_name='Chromedriver path',
                          help='type Chromedriver path')
        mcxt.add_argument('msg',
                          display_name='message',
                          help='type message to send')
        mcxt.add_argument('filepath',
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
