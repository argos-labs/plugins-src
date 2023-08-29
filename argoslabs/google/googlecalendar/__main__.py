"""
====================================
 :mod:`argoslabs.google.googlecalendar``
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS manages google calendar
"""

################################################################################
import sys
from alabs.common.util.vvargs import ArgsError, ArgsExit
from argoslabs.google.googlecalendar import main


################################################################################
if __name__ == '__main__':
    try:
        main()
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
