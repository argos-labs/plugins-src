"""
====================================
 :mod:`argoslabs.crypt.base64`
====================================
.. moduleauthor:: Venkatesh Vanjre <vvanjre@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module crypt.base64
"""

################################################################################
import sys
from alabs.common.util.vvargs import ArgsError, ArgsExit
from argoslabs.crypt.base64 import main


################################################################################
if __name__ == '__main__':
    try:
        main()
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
