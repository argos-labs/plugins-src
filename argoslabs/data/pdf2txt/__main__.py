"""
====================================
 :mod:`argoslabs.data.pdf2txt`
====================================
.. moduleauthor:: Irene Cho <irenee@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS PDF Conversion(pdf -> txt) plugin
"""

################################################################################
import sys
from alabs.common.util.vvargs import ArgsError, ArgsExit
from argoslabs.data.pdf2txt import main


################################################################################
if __name__ == '__main__':
    try:
        main()
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
