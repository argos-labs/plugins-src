"""
====================================
 :mod:`argoslabs.text.figlet`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module to use Selenium
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/12]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2021/02/02]
#     - starting

################################################################################
import os
import sys
from unittest import TestCase
from argoslabs.text.figlet import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        ...

    # ==========================================================================
    def test0010_fail_empty(self):
        # sg = sys.gettrace()
        # if sg is None:  # Not in debug mode
        #     print('Skip testing at test/build time')
        #     return
        try:
            _ = main('')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_success(self):
        of = 'stdout.txt'
        try:
            r = main('standard',
                     'Hello world?',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == r''' _   _      _ _                            _     _ ___ 
| | | | ___| | | ___   __      _____  _ __| | __| |__ \
| |_| |/ _ \ | |/ _ \  \ \ /\ / / _ \| '__| |/ _` | / /
|  _  |  __/ | | (_) |  \ V  V / (_) | |  | | (_| ||_| 
|_| |_|\___|_|_|\___/    \_/\_/ \___/|_|  |_|\__,_|(_) 
                                                       
''')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0120_success_font(self):
        of = 'stdout.txt'
        try:
            r = main('slant',
                     'Hello world?',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == r'''    __  __     ____                             __    _____ 
   / / / /__  / / /___     _      ______  _____/ /___/ /__ \
  / /_/ / _ \/ / / __ \   | | /| / / __ \/ ___/ / __  / / _/
 / __  /  __/ / / /_/ /   | |/ |/ / /_/ / /  / / /_/ / /_/  
/_/ /_/\___/_/_/\____/    |__/|__/\____/_/  /_/\__,_/ (_)   
                                                            
''')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0130_success_direction(self):
        of = 'stdout.txt'
        try:
            r = main('slant',
                     'Hello world?',
                     '--direction', 'right-to-left',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == r'''                       ___      ____                            ____     __  __
                      /__ \____/ / /________ _      __   ____  / / /__  / / / /
                       / _/ __  / / ___/ __ \ | /| / /  / __ \/ / / _ \/ /_/ / 
                      /_// /_/ / / /  / /_/ / |/ |/ /  / /_/ / / /  __/ __  /  
                     (_) \__,_/_/_/   \____/|__/|__/   \____/_/_/\___/_/ /_/   
                                                                               
''')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0140_success_justify(self):
        of = 'stdout.txt'
        try:
            r = main('slant',
                     'Hello world?',
                     '--width', '44',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == r'''    __  __     ____    
   / / / /__  / / /___ 
  / /_/ / _ \/ / / __ \
 / __  /  __/ / / /_/ /
/_/ /_/\___/_/_/\____/ 
                       
                      __    _____ 
 _      ______  _____/ /___/ /__ \
| | /| / / __ \/ ___/ / __  / / _/
| |/ |/ / /_/ / /  / / /_/ / /_/  
|__/|__/\____/_/  /_/\__,_/ (_)   
                                  
''')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
