"""
====================================
 :mod:`argoslabs.google.googlesearch``
====================================
.. moduleauthor:: Myeongkook Park <Myeongkook@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Managing Google Sheets
"""

################################################################################
import sys
from alabs.common.util.vvargs import ArgsError, ArgsExit
from argoslabs.google.googlesearch import main


################################################################################
if __name__ == '__main__':
    try:
        main()
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
