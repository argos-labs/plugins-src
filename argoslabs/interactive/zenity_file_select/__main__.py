"""
====================================
 :mod:`argoslabs.interactive.file_selection`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Zenity File Selction Plugin
"""

################################################################################
import sys
from alabs.common.util.vvargs import ArgsError, ArgsExit
from argoslabs.interactive.zenity_file_select import main


################################################################################
if __name__ == '__main__':
    try:
        main()
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
