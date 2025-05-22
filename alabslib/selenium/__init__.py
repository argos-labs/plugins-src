"""
====================================
 :mod:`alabslib.selenium`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS base class to use Selenium
"""
# Authors
# ===========
#
# * Jerry Chae
# * taehoon ahn
# * Wanjin Choi
# Change Log
# --------
#  * [2025/05/20]
#    - chrome 옵션을 yaml파일을 읽어 추가할 수 있도록 하는 기능 추가
#  * [2024/07/02]
#     - driver_execute_script 기능 추가(javascript)
#     - get_by_xpath() timeout 오류 수정
#  * [2022/12/07]
#     - 교봉씨 요청으로 다음 두 개의 옵션을 크롬에 넣음
#       --no-sandbox --disable-dev-shm-usage
#  * [2022/02/22]
#     - "profile.default_content_setting_values.automatic_downloads": 1
#  * [2022/02/03]
#     - chrome_options merged into options
#  * [2022/01/19]
#     - pdf output: only for Chrome
#       using pyperclip.copy(f)
#             pyautogui.hotkey('ctrl', 'v')
#             pyautogui.press('enter')
#  * [2021/12/01]
#     - for clipboard : to evoid NAVER capture, add send_keys_clipboard
#  * [2021/04/28]
#     - A1 Mac에서 Edge 버전 구하기
#  * [2021/04/21]
#     - Chrome, Edge 에 대해서 자동으로 해당 버전 링크 구하기
#  * [2021/03/11]
#     - Chrome 89 버전용 링크 추가
#  * [2021/03/03]
#     - Mac porting 시작
#  * [2021/01/17]
#     - get_by_xpath에 move_to_element flag 추가
#  * [2020/12/02]
#     - starting

import os
import platform
import re
import sys
import csv
import stat
import xlrd
import time
import glob
import json
import shutil
import locale
import logging
import requests
import traceback
import pyperclip
import subprocess
from tempfile import gettempdir
from zipfile import ZipFile
from urllib.parse import urljoin
# for selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
# for bs
from bs4 import BeautifulSoup
# for Edge and EdgeOptions
from msedge.selenium_tools import Edge, EdgeOptions
# For Screen Capture
from Screenshot import Screenshot_Clipping


################################################################################
class PySelenium(object):
    # ==========================================================================
    BROWSERS = {
        'Chrome': {
            'driver-download-home': 'https://chromedriver.chromium.org'
                                    '/downloads',
            'rec': re.compile(r'ChromeDriver\s[\d.]+')
        },
        'Edge': {
            'driver-download-base': 'https://msedgedriver.azureedge.net/',
        }
        # 'Firefox',
    }
    CACHE_FOLDER = os.path.join(gettempdir(), 'PySelenium.cahce')
    PDF_FOLDER = os.path.join(CACHE_FOLDER, 'PDF_Download')
    EXP_COND = {
        'title_is': EC.title_is,
        'title_contains': EC.title_contains,
        'presence_of_element_located': EC.presence_of_all_elements_located,
        'visibility_of_element_located': EC.visibility_of_element_located,
        'visibility_of': EC.visibility_of,
        'presence_of_all_elements_located': EC.presence_of_all_elements_located,
        'text_to_be_present_in_element': EC.text_to_be_present_in_element,
        'text_to_be_present_in_element_value':
            EC.text_to_be_present_in_element_value,
        'frame_to_be_available_and_switch_to_it':
            EC.frame_to_be_available_and_switch_to_it,
        'invisibility_of_element_located': EC.invisibility_of_element_located,
        'element_to_be_clickable': EC.element_to_be_clickable,
        'staleness_of': EC.staleness_of,
        'element_to_be_selected': EC.element_to_be_selected,
        'element_located_to_be_selected': EC.element_located_to_be_selected,
        'element_selection_state_to_be': EC.element_selection_state_to_be,
        'element_located_selection_state_to_be':
            EC.element_located_selection_state_to_be,
        'alert_is_present': EC.alert_is_present,
    }

    # ==========================================================================
    def chrome_option_add(self, wo,chrome_option):
        self.chrome_options = wo
        # 리스트나 튜플일 경우
        if isinstance(chrome_option, (list, tuple)):
            for opt in chrome_option:
                self.chrome_options.add_argument(opt)
        #달랑하나 있을경우
        elif isinstance(chrome_option, str):
            self.chrome_options.add_argument(chrome_option)

    def _get_browser_version(self):
        if self.platform == 'win32':
            if self.browser == 'Chrome':
                cmd = [
                    'powershell',
                    '-command',
                    r"(Get-Item (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe').'(Default)').VersionInfo",
                ]
                # '''
                # ProductVersion   FileVersion      FileName
                # --------------   -----------      --------
                # 87.0.4280.66     87.0.4280.66     C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
                # '''
                po = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                po.wait()
                out = po.stdout.read().decode().strip()
                if out.find('ProductVersion') <= 0:
                    lines = out.split('\n')
                    bv = lines[-1].split()[0]
                    rs = bv.split('.')[0]
                    po.stdout.close()
                    return rs
                else:
                    raise IOError(f'"{self.browser}" '
                                  f'is not installed is this system')
            # todo: "Edge Legacy"
            elif self.browser == 'Edge':
                cmd = [
                    'reg.exe',
                    'QUERY',
                    "HKEY_CURRENT_USER\Software\Microsoft\Edge\BLBeacon",
                    '/t',
                    'REG_SZ',
                    '/reg:32',
                    '/v',
                    'version',
                ]
                # '''
                # HKEY_CURRENT_USER\Software\Microsoft\Edge\BLBeacon
                #     version    REG_SZ    88.0.705.50
                # '''
                po = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                po.wait()
                os_encoding = locale.getpreferredencoding()
                out = po.stdout.read().decode(os_encoding).strip()
                for line in out.split('\n'):
                    line = line.strip()
                    if line.startswith('version'):
                        rs = line.split()[-1]
                        po.stdout.close()
                        return rs
                raise IOError(
                    f'"{self.browser}" is not installed is this system')
            else:
                raise NotImplementedError(
                    f'to get {self.browser} browser version')
        elif self.platform == 'darwin':
            if self.browser == 'Chrome':
                chrome_exe = (f'/Applications/Google Chrome.app/'
                              f'Contents/MacOS/Google Chrome')
                if not os.path.exists(chrome_exe):
                    raise RuntimeError(f'Cannot find Chrome at "{chrome_exe}"')
                cmd = [
                    chrome_exe,
                    '--version',
                ]
                # Google Chrome 88.0.4324.192
                po = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                po.wait()
                out = po.stdout.read().decode().strip()
                if out.find('Google Chrome') >= 0:
                    bv = out.split()[-1]
                    return bv.split('.')[0]
                else:
                    raise IOError(
                        f'"{self.browser}" is not installed is this system')
            elif self.browser == 'Edge':
                info_f = '/Applications/Microsoft Edge.app/Contents/Info.plist'
                if not os.path.exists(info_f):
                    raise RuntimeError(
                        f'Cannot find Edge at "/Applications/Microsoft Edge.app"')
                with open(info_f) as ifp:
                    b_found = False
                    for line in ifp:
                        if b_found:
                            # must be like  <string>90.818.21042449</string>
                            fa = re.findall(r'([\d.]+)', line)
                            if not fa:
                                raise RuntimeError(
                                    'Cannot find Edge version at Mac')
                            return fa[0]
                        if line.find('CFBundleShortVersionString') > 0:
                            b_found = True

            else:
                raise NotImplementedError(
                    'Linux, Mac need to be get browser version')
        else:
            raise NotImplementedError(
                'Linux, Mac need to be get browser version')

    # ==========================================================================
    def _get_web_driver(self, drive_f):
        if self.browser == 'Chrome':

            if not os.path.exists(self.PDF_FOLDER):
                os.makedirs(self.PDF_FOLDER)

            appState = {
                "recentDestinations": [
                    {
                        "id": "Save as PDF",
                        "origin": "local"
                    }
                ],
                "selectedDestinationId": "Save as PDF",
                "version": 2,
            }

            profile = {
                'printing.print_preview_sticky_settings.appState': json.dumps(
                    appState),
                'savefile.default_directory': self.PDF_FOLDER,
                "plugins.always_open_pdf_externally": True,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
                "profile.default_content_setting_values.automatic_downloads": 1,
            }
            wo =webdriver.ChromeOptions()
            self.chrome_option_add(wo,self.chrome_options)
            # chrome_options merged into options
            wo.add_experimental_option('prefs', profile)
            wo.add_argument('--kiosk-printing')
            wo.add_argument('--no-sandbox')
            wo.add_argument('--disable-dev-shm-usage')

            if not self.headless:
                wd = webdriver.Chrome(executable_path=drive_f, options=wo)
            else:
                wo.add_argument('headless')
                wo.add_argument(f'window-size={self.width}x{self.height}')
                wo.add_argument("disable-gpu")
                wd = webdriver.Chrome(executable_path=drive_f, options=wo)
            return wd
        if self.browser == 'Edge':
            # if self.platform == 'darwin' and platform.platform().find('arm64') > 0:
            #     wo = webdriver.EdgeOption
            if not self.headless:
                wd = webdriver.Edge(executable_path=drive_f)
            else:
                wo = EdgeOptions()
                wo.use_chromium = True
                wo.add_argument('headless')
                wo.add_argument(f'window-size={self.width}x{self.height}')
                wo.add_argument("disable-gpu")
                wd = Edge(executable_path=drive_f, options=wo)
            return wd
        raise NotImplementedError(
            f'Need to implement for the driver {self.browser} at {self.platform}')

    # ==========================================================================
    def _get_download_url_chrome_gr_114_old(self):
        hp_url = 'https://googlechromelabs.github.io/chrome-for-testing/'
        r = requests.get(hp_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        for x in soup.find_all('section'):
            if self.browser_version + '.' in x.text:
                for code in x.find_all('code'):
                    d_link = None
                    if (self.platform == 'win32' and
                            '/chromedriver-win32.zip' in code.text):
                        d_link = code.text
                    elif (self.platform == 'win64' and
                          '/chromedriver-win64.zip' in code.text):
                        d_link = code.text
                    elif (self.platform == 'linux' and
                          '/chromedriver-linux64.zip' in code.text):
                        d_link = code.text
                    elif self.platform == 'darwin':
                        if (platform.platform().find(
                                'arm64') > 0 and
                                '/chromedriver-mac-arm64.zip' in code.text):
                            d_link = code.text
                        elif '/chromedriver-mac-x64.zip' in code.text:
                            d_link = code.text
                    if d_link:
                        return d_link

    # ==========================================================================
    def _get_download_url_chrome_gr_114(self):
        d_link = None
        hp_url = (f'https://googlechromelabs.github.io/chrome-for-testing/'
                  f'latest-patch-versions-per-build-with-downloads.json')
        r = requests.get(hp_url)
        json_data = r.json()
        for build, details in json_data['builds'].items():
            if build.split(".")[0] == self.browser_version:
                for download_info in details['downloads']:
                    if download_info == 'chromedriver' and self.browser_version in build:
                        data = details['downloads']['chromedriver']
                        if self.platform == 'win32':
                            d_link = next((item['url'] for item in data if
                                           item['platform'] == 'win32'), None)
                        elif self.platform == 'win64':
                            d_link = next((item['url'] for item in data if
                                           item['platform'] == 'win64'), None)
                        elif self.platform == 'linux':
                            d_link = next((item['url'] for item in data if
                                           item['platform'] == 'linux64'), None)
                        elif self.platform == 'darwin':
                            if platform.platform().find('arm64') > 0:
                                d_link = next((item['url'] for item in data if
                                               item['platform'] == 'mac-arm64'),
                                              None)
                            else:
                                d_link = next((item['url'] for item in data if
                                               item['platform'] == 'mac-x64'),
                                              None)
        if d_link:
            return d_link
        else:
            raise Exception(
                f"Url not found for selenium chromedriver {self.platform}")

    # ==========================================================================
    def _get_download_url_chrome(self):
        # for chrome greater version 114
        if int(self.browser_version) > 114:
            hp_url = self._get_download_url_chrome_gr_114()
            return hp_url
        hp_url = self.BROWSERS[self.browser].get('driver-download-home')
        if not hp_url:
            raise ReferenceError(
                f'Cannot get download link homepage for {self.browser} '
                f'with version {self.browser_version}')
        r = requests.get(hp_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        for x in soup.find_all('a'):
            atext = x.text
            rec = self.BROWSERS[self.browser].get('rec')
            m = rec.search(atext)
            if m is None:
                continue
            version = atext.split()[1]
            if version.startswith(self.browser_version + '.'):
                href = x.get('href')
                r = requests.get(href)
                soup = BeautifulSoup(r.text, 'html.parser')
                # chromedriver_linux64.zip
                d_link = None
                if self.platform == 'win32':
                    d_link = urljoin(href, version + '/chromedriver_win32.zip')
                elif self.platform == 'linux':
                    d_link = urljoin(href,
                                     version + '/chromedriver_linux64.zip')
                elif self.platform == 'darwin':
                    if platform.platform().find('arm64') > 0:
                        d_link = urljoin(href,
                                         version + '/chromedriver_mac64_m1.zip')
                    else:
                        d_link = urljoin(href,
                                         version + '/chromedriver_mac64.zip')
                if d_link:
                    return d_link
        raise LookupError(
            f'Cannot find web Chrome driver for version "{self.browser_version}" on "{self.platform}"')

    # ==========================================================================
    def _get_download_url_edge(self):
        href = self.BROWSERS[self.browser].get('driver-download-base')
        if not href:
            raise ReferenceError(
                f'Cannot get download link homepage for {self.browser} with version {self.browser_version}')
        # https://msedgedriver.azureedge.net/90.0.818.42/edgedriver_win32.zip

        version = self.browser_version
        d_link = None
        if self.platform == 'win32':
            if platform.machine().endswith('64'):
                d_link = urljoin(href, version + '/edgedriver_win64.zip')
            else:
                d_link = urljoin(href, version + '/edgedriver_win32.zip')
        # elif self.platform == 'linux':
        #     d_link = urljoin(href, version + '/edgedriver_linux64.zip')
        elif self.platform == 'darwin':
            # test arm64 but failed instead use mac64 on M1
            # if platform.platform().find('arm64') > 0:
            #     d_link = urljoin(href, version + '/edgedriver_arm64.zip')
            # else:
            d_link = urljoin(href, version + '/edgedriver_mac64.zip')
        if d_link:
            return d_link
        raise LookupError(
            f'Cannot find web Edge driver for version "{self.browser_version}" on "{self.platform}"')

    # ==========================================================================
    def _get_download_url(self):
        if self.browser == 'Chrome':
            return self._get_download_url_chrome()
        elif self.browser == 'Edge':
            return self._get_download_url_edge()

        raise ReferenceError(
            f'Cannot get driver link for the version "{self.browser_version}"')

    # ==========================================================================
    # for chrome greater 114
    @staticmethod
    def _download_driver_gt_114(url, drive_f):
        r = requests.get(url, allow_redirects=True)
        is_unzip = url.lower().endswith('.zip')
        if is_unzip:
            with open(f'{drive_f}.zip', 'wb') as ofp:
                ofp.write(r.content)
            tmp_d = os.path.join(gettempdir(), os.path.basename(drive_f))
            with ZipFile(f'{drive_f}.zip') as zfp:
                zflist = zfp.namelist()
            wd_name = None
            for zf in zflist:
                wd_name = zf
            if not wd_name:
                raise ReferenceError(
                    f'Cannot find webdriver at "{drive_f}.zip"')
            with ZipFile(f'{drive_f}.zip') as zfp:
                zfp.extract(wd_name, tmp_d)
            for f in glob.glob(os.path.join(tmp_d, '*', '*')):
                shutil.move(f, drive_f)
                break
            shutil.rmtree(tmp_d)
            os.remove(f'{drive_f}.zip')
        else:
            with open(drive_f, 'wb') as ofp:
                ofp.write(r.content)
        st = os.stat(drive_f)
        os.chmod(drive_f, st.st_mode | stat.S_IEXEC)

    # ==========================================================================
    def _download_driver(self, drive_f):
        # download and save to cache
        url = self._get_download_url()
        # for chrome greater 114
        if int(self.browser_version) > 114:
            self._download_driver_gt_114(url, drive_f)
        else:
            r = requests.get(url, allow_redirects=True)
            is_unzip = url.lower().endswith('.zip')
            if is_unzip:
                with open(f'{drive_f}.zip', 'wb') as ofp:
                    ofp.write(r.content)
                tmp_d = os.path.join(gettempdir(), os.path.basename(drive_f))
                with ZipFile(f'{drive_f}.zip') as zfp:
                    zflist = zfp.namelist()
                wd_name = None
                for zf in zflist:
                    print(zf)
                    if zf.find('/') > 0 or zf.find('\\') > 0:
                        continue
                    wd_name = zf
                    break
                if not wd_name:
                    raise ReferenceError(
                        f'Cannot find webdriver at "{drive_f}.zip"')
                with ZipFile(f'{drive_f}.zip') as zfp:

                    zfp.extract(wd_name, tmp_d)
                for f in glob.glob(os.path.join(tmp_d, '*')):
                    print(f, drive_f)
                    shutil.move(f, drive_f)
                    break
                shutil.rmtree(tmp_d)
                os.remove(f'{drive_f}.zip')
            else:
                with open(drive_f, 'wb') as ofp:
                    ofp.write(r.content)
            st = os.stat(drive_f)
            os.chmod(drive_f, st.st_mode | stat.S_IEXEC)

    # ==========================================================================
    def _get_driver(self):
        if not os.path.exists(self.CACHE_FOLDER):
            os.makedirs(self.CACHE_FOLDER)
        bn = f'{self.platform}_{self.browser}_{self.browser_version}.exe'
        drive_f = os.path.join(self.CACHE_FOLDER, bn)
        if os.path.exists(drive_f):
            return self._get_web_driver(drive_f)
        self._download_driver(drive_f)
        if os.path.exists(drive_f):
            return self._get_web_driver(drive_f)
        raise RuntimeError(f'Cannot get web driver')

    # ==========================================================================
    def __init__(self, browser='Chrome', headless=False,
                 url='www.google.com',
                 width=1200, height=800, logger=None, chrome_options=None):
        try:
            if browser not in self.BROWSERS:
                raise ReferenceError(
                    f'Cannot get info for the browser "{browser}"')
            self.browser = browser
            self.headless = headless
            self.url = url
            self.width = width
            self.height = height
            self.chrome_options = chrome_options
            if logger is None:
                logger = logging.getLogger('PySelenium')
            self.logger = logger
            # for internal uses
            self.platform = sys.platform
            self.browser_version = self._get_browser_version()
            self.driver = None
            self.main_handle = None
        except Exception as err:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('open Error: %s\n' % str(err))
            self.logger.error('%s\n' % ''.join(_out))
            raise

    # ==========================================================================
    def open(self):
        try:

            self.driver = self._get_driver()
            self.driver.set_window_size(self.width, self.height)
            self.driver.get(self.url)
            self.logger.info(f'open: get <{self.url}> with <{self.width},{self.height}>')
            self.implicitly_wait()
        except Exception as e:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('open Error: %s\n' % str(e))
            self.logger.error('%s\n' % ''.join(_out))
            raise

    # ==========================================================================
    def close(self):
        try:
            self.driver.close()
            self.logger.info(f'closed')
        except Exception as e:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('close Error: %s\n' % str(e))
            self.logger.error('%s\n' % ''.join(_out))
            raise

    # ==========================================================================
    def __enter__(self):
        self.open()
        return self

    # ==========================================================================
    def __exit__(self, *args):
        self.close()

    # ==========================================================================
    @staticmethod
    def get_safe_path(*_args):
        if sys.platform == 'win32':
            args = []
            for i in range(len(_args)):
                args.append(_args[i].replace('/', '\\'))
        else:
            args = _args
        p = os.path.join(*args)
        d = os.path.dirname(p)
        if not os.path.exists(d):
            os.makedirs(d)
        return p

    # ==========================================================================
    def implicitly_wait(self, imp_wait=3, after_wait=1):
        try:
            if imp_wait > 0:
                self.driver.implicitly_wait(imp_wait)
            if after_wait > 0:
                time.sleep(after_wait)
        except Exception as e:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('implicitly_wait Error: %s\n' % str(e))
            self.logger.error('%s\n' % ''.join(_out))
            raise

    # ==========================================================================
    def get_by_xpath(self, xp,
                     cond='presence_of_element_located',
                     timeout=None,
                     cond_text=None,
                     wait_until_valid_text=False,
                     move_to_element=False):
        if cond not in self.EXP_COND:
            cond = None
        if not cond:
            return self.driver.find_element_by_xpath(xp)
        if timeout == None :
            timeout = 10
        else:
            pass
        cond_f = self.EXP_COND[cond]
        args = [(By.XPATH, xp)]
        if cond in (
                'text_to_be_present_in_element',
                'text_to_be_present_in_element_value'):
            args.append(cond_text)
        try:
            e = WebDriverWait(self.driver, timeout).until(cond_f(*args))
        except TimeoutException:
            self.logger.error(f"Timeout waiting for condition '{cond}' with xpath '{xp}'")
            return None
        if isinstance(e, bool):
            cond_f = self.EXP_COND['presence_of_element_located']
            args = [(By.XPATH, xp)]
            e = WebDriverWait(self.driver, timeout).until(cond_f(*args))
        if isinstance(e, list):
            e = e[0]
        if not isinstance(e, WebElement):
            self.logger.error(f"Expected WebElement but got {type(e)}")
            print(e)
        if wait_until_valid_text:
            for i in range(timeout):
                if e.text:
                    break
                time.sleep(1)
                self.logger.debug(f'get_by_xpath: waiting valid text ... [{i + 1}]')
        if move_to_element:
            # actions = ActionChains(self.driver)
            # actions.move_to_element(e).perform()
            self.driver.execute_script('arguments[0].scrollIntoView();', e)
        return e

    # ==========================================================================
    def move_to_element(self, e):
        self.driver.execute_script('arguments[0].scrollIntoView();', e)

    # ==========================================================================
    def key_action(self, key=Keys.TAB, count=1):
        actions = ActionChains(self.driver)
        for _ in range(count):
            actions = actions.send_keys(key)
        actions.perform()


    # ==========================================================================
    def mouse_action_click(self, e, x=0, y=0):
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(e, x, y)
        actions.click()
        actions.perform()

    # ==========================================================================
    def safe_click(self, e):
        # selenium.common.exceptions.ElementClickInterceptedException:
        # Message: element click intercepted
        try:
            e.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", e)

    # ==========================================================================
    @staticmethod
    def send_keys(e, keys):
        e.send_keys(keys)

    # ==========================================================================
    def send_keys_clipboard(self, e, keys, timeout=1):
        self.safe_click(e)
        pyperclip.copy(keys)
        self.send_keys(e, Keys.CONTROL + 'v')
        time.sleep(timeout)

    # ==========================================================================
    @staticmethod
    def get_download_path():
        """Returns the default downloads path for linux or windows"""
        if os.name == 'nt':
            import winreg
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]
            return location
        else:
            return os.path.join(os.path.expanduser('~'), 'downloads')

    # ==========================================================================
    def alert_action(self, action='accept', timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.alert_is_present(),
                'Timed out waiting for alert')
            alert = self.driver.switch_to.alert
            if action == 'accept':
                alert.accept()
                self.logger.info("alert accepted")
            else:
                alert.dismiss()
                self.logger.info("alert dissmissed")
        except TimeoutException:
            self.logger.info(f"no alert with timeout {timeout}")

    # ==========================================================================
    def close_all_popups(self):
        # 팝업창이 여러개 일때 닫기
        main = self.driver.window_handles
        self.main_handle = main_handle = main[0]
        for handle in main:
            if handle != main_handle:
                self.driver.switch_to.window(handle)
                self.driver.close()
        self.driver.switch_to.window(main_handle)

    # ==========================================================================
    def switch_to_window(self, index=1):
        # 해당 n번째 (1부터 시작) 팝업창으로 스위칭
        main = self.driver.window_handles
        self.main_handle = main_handle = main[0]
        for i, handle in enumerate(main):
            if handle == main_handle:
                continue
            if i == index:
                self.driver.switch_to.window(handle)
                break

    # ==========================================================================
    def switch_to_main_window(self):
        if self.main_handle is not None:
            self.driver.switch_to.window(self.main_handle)

    # ==========================================================================
    def scroll_by(self, x=0, y=0):
        if x > 0:
            x = f'+{x}'
        if y > 0:
            y = f'+{y}'
        self.driver.execute_script(f"scrollBy({x},{y});")

    # ==========================================================================
    def switch_to_iframe(self, xpath):
        self.switch_from_iframe()
        iframe = self.get_by_xpath(xpath)
        self.driver.switch_to.frame(iframe)

    # ==========================================================================
    def switch_to_iframe_by_name(self, iframe):
        self.switch_from_iframe()
        self.driver.switch_to.frame(iframe)

    # ==========================================================================
    def switch_from_iframe(self):
        self.driver.switch_to.default_content()

    # ==========================================================================
    def select_by_visible_text(self, xpath, text):
        e = self.get_by_xpath(xpath)
        s = Select(e)
        s.select_by_visible_text(text)

    # ==========================================================================
    def select_by_value(self, xpath, value):
        e = self.get_by_xpath(xpath)
        s = Select(e)
        s.select_by_value(value)

    # ==========================================================================
    def select_by_index(self, xpath, index):
        e = self.get_by_xpath(xpath)
        s = Select(e)
        s.select_by_index(index)

    # ==========================================================================
    @staticmethod
    def safe_download_move(glob_f, target_f, timeout=10):
        is_found = False
        for _ in range(timeout):
            if is_found:
                break
            for f in glob.glob(glob_f):
                # 저장하던 중일 수 있으므로 약간 기다림
                time.sleep(0.5)
                shutil.move(f, target_f)
                is_found = True
                break
            time.sleep(1)
        if not is_found:
            raise RuntimeError(f'safe_download_move: Cannot download file '
                               f'"{target_f}"')

    # ==========================================================================
    def xls_to_csv(self, xls_f, csv_f, num_headers=1, is_append=False):
        self.logger.debug(f'xls_to_csv: {xls_f} => {csv_f}')
        if not os.path.exists(xls_f):
            raise IOError(f'Cannot read Excel file "{xls_f}"')
        mode = 'a' if is_append else 'w'
        with open(csv_f, mode, encoding='utf-8') as ofp:
            c = csv.writer(ofp, lineterminator='\n')
            wb = xlrd.open_workbook(xls_f)
            ws = wb.sheet_by_index(0)
            for r_ndx in range(num_headers, ws.nrows):  # exclude header
                row = []
                for c_ndx in range(ws.ncols):
                    v = ws.cell(r_ndx, c_ndx).value
                    if not v:
                        v = ''
                    row.append(v)
                c.writerow(row)

    # ==========================================================================
    def new_tab(self, url):
        self.driver.execute_script(f'window.open("{url}","_blank");')

    # ==========================================================================
    def close_tab(self):
        self.driver.execute_script(f'window.close();')

    # ==========================================================================
    def full_screenshot(self, f, save_pdf=False):
        if not save_pdf:
            obj = Screenshot_Clipping.Screenshot()
            img_loc = obj.full_Screenshot(self.driver,
                                          save_path=os.path.dirname(f),
                                          image_name=os.path.basename(f))
            return img_loc
        try:
            if self.browser != 'Chrome':
                raise RuntimeError(f'PDF Save functionality is '
                                   f'only supported for Chrome Browser')
            fn, ext = os.path.splitext(f)
            if ext.lower() != '.pdf':
                f = fn + '.pdf'
            import pyautogui
            self.driver.execute_script('window.print();')
            time.sleep(1)
            # 한글 입력 안되어 pyperclip 이용
            # pyautogui.typewrite(f)
            pyperclip.copy(f)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            return f
        except Exception as err:
            raise IOError(f'Cannot save PDF "{f}"{err}')

    # ==========================================================================
    def driver_execute_script(self,e):
        self.driver.execute_script(f"{e}")

    # ==========================================================================
    def start(self):
        raise NotImplementedError('Inherited Object must have start() method')
