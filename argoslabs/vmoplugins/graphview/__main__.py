"""
====================================
 :mod:`argoslabs.vmoplugins.graphview`
====================================
.. moduleauthor:: Binh Ha <binh.ha@vmodev.com>
.. note:: YOURLABS License

Description
===========
YOUR LABS plugin module sample
"""

################################################################################
import sys
from alabs.common.util.vvargs import ArgsError, ArgsExit
import argoslabs.vmoplugins.graphview as graph

################################################################################
if __name__ == '__main__':
    try:
        graph.main()
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
