"""
====================================
 :mod:`argoslabs.vmoplugins.sqlite`
====================================
.. moduleauthor:: Hiep Tran <Tranquanghiep2009@gmail.com>
.. note:: ARGOS-LABS License

Description
===========
SQLite Execution Plugin
"""

################################################################################
import sys
from alabs.common.util.vvargs import ArgsError, ArgsExit

################################################################################
from argoslabs.vmoplugins.sqlite import main

if __name__ == '__main__':
    try:
        main()
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
