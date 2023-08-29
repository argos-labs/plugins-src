"""
====================================
 :mod:`argoslabs.api.graphql`
====================================
.. moduleauthor:: Arun Kumar <ak080495@gmail.com>
.. note:: ARGOS-LABS License

Description
===========
GraphQL API
"""

################################################################################
import sys
from alabs.common.util.vvargs import ArgsError, ArgsExit
from argoslabs.api.graphql import main


################################################################################
if __name__ == '__main__':
    try:
        main()
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
