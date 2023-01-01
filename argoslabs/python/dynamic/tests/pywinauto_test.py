from selenium import webdriver
import pywinauto
import time
import os

# setting
driver_path      = "%s\\Downloads\\chromedriver.exe" % os.environ['USERPROFILE']
driver           = webdriver.Chrome(executable_path=driver_path)
driver.implicitly_wait(10)

file_path = '%s\\Downloads\\test.jpg' % os.environ['USERPROFILE']

# Connect imgur
driver.get('https://imgur.com/upload')

# Select File Click
driver.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div/div[1]/div[2]/label')[0].click()

import locale
os_encoding = locale.getpreferredencoding()
if os_encoding == 'cp949':
    open_label = '열기'  # for Korean
elif os_encoding == 'cp932':
    open_label = '開く'  # for Japanese
else:
    open_label = 'Open'  # for Others

# pywinauto
findWindow = lambda: pywinauto.findwindows.find_windows(title=open_label)[0]
dialog = pywinauto.timings.wait_until_passes(2, 4, findWindow)
pwa_app = pywinauto.Application()
pwa_app.connect(handle=dialog)
window = pwa_app[open_label]
window.wait('ready', timeout=10)

# Input File Name
pywinauto.keyboard.send_keys("%N")
edit = window.Edit4
edit.set_focus()
edit.set_text(file_path)

# Open Click
button = window[f'{open_label}(&O):']
button.click()

time.sleep(3)

driver.close()
# exit()
