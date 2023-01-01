#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:test_caller of helloworld
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS
"""

# 관련 작업자
# ===========
#
# 본 모듈은 다음과 같은 사람들이 관여했습니다:
#  * 채문창
#
# 작업일지
# --------
#
# 다음과 같은 작업 사항이 있었습니다:
#  * [2018/10/30]
#     - 본 모듈 작업 시작
################################################################################
import os
import sys
import time
import threading
import subprocess
from unittest import TestCase


################################################################################
class statusThread (threading.Thread):
    def __init__(self, statfile):
        threading.Thread.__init__(self)
        self.statfile = statfile
        self.is_break = False
    def run(self):
        print("Starting " + self.name)
        while not self.is_break:
            if os.path.exists(self.statfile):
                break
            time.sleep(1)
        ifp = open(self.statfile, 'r')
        while not self.is_break:
            new = ifp.readline()
            if new:
                print("%s" % new.rstrip())
            else:
                time.sleep(1)
        print("Exiting " + self.name)


################################################################################
def run_plugin_module(statfile):
    cmd = [
        sys.executable,
        '__main__.py',
        '--statfile',
        statfile,
        '--steps', '2',
    ]
    params = ['3000', 'y', '50', '0.5', '1.2.3.4', 'tom', 'jerry', 'foo', 'foo']
    cmd += params
    po = subprocess.Popen(cmd)
    return po


################################################################################
def main():
    mdir = os.path.dirname(__file__)
    os.chdir(mdir)
    print('working monitor=%s' % mdir)
    statfile = 'caller_status.log'
    if os.path.exists(statfile):
        os.unlink(statfile)
    po = run_plugin_module(statfile)
    sth = statusThread(statfile)
    # Start new Threads
    sth.start()
    while True:
        poll = po.poll()
        if poll is not None:
            break
    sth.is_break = True
    sth.join()
    # print ("Exiting Main Thread")
    with open(statfile) as ifp:
        s1 = ifp.read()
    with open('caller_status.org') as ifp:
        s2 = ifp.read()
    print('Successful status log? %s' % (s1 == s2))
    return s1 == s2


################################################################################
class TU(TestCase):
    # ==========================================================================
    def test_main(self):
        self.assertTrue(main())
