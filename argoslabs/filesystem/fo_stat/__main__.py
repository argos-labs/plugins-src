"""
====================================
 :mod:`argoslabs.filesystem.fo_stat`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module filesystem fo_stat
"""
import sys
from alabs.common.util.vvargs import ArgsError, ArgsExit
from argoslabs.filesystem.fo_stat import main

################################################################################
if __name__ == '__main__':
    try:
        main()
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
