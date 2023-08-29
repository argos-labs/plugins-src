"""
====================================
 :mod:`argoslabs.simple.counter`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS simple counter
"""
# Authors
# ===========
#
# * Arun Kumar
#
# Change Log
# --------
#


################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class SimpleCounter(object):
    # ==========================================================================
    OP_TYPE = ['Initialize',
               'Count Up',
               'Count Down']

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec

    # ==========================================================================
    def do(self, op):
        if not op:
            raise Exception("Select Function type")
        elif op == 'Initialize':
            if self.argspec.end_numbers and self.argspec.start_number:
                result = self.argspec.start_number
                print(result, end='')
                return 0
            else:
                raise Exception("start_number and end_numbers required.")
        elif op == 'Count Up':
            if self.argspec.increment:
                countup = self.argspec.start_number + self.argspec.increment
            else:
                countup = self.argspec.start_number + 1
            if countup > self.argspec.end_numbers:
                sys.stderr.write(f'{countup} exceed {self.argspec.end_numbers}')
                return 1
            elif countup <= self.argspec.end_numbers:
                print(f'{countup}', end='')
                return 0
            else:
                raise Exception("start_number and end_numbers required.")
        elif op == 'Count Down':
            if self.argspec.increment:
                count_down = self.argspec.start_number + self.argspec.increment
            else:
                count_down = self.argspec.start_number - 1
            if count_down < self.argspec.end_numbers:
                sys.stderr.write(f'{count_down} exceed {self.argspec.end_numbers}')
                return 1
            elif count_down >= self.argspec.end_numbers:
                print(f'{count_down}', end='')
                return 0
            else:
                raise Exception("start_number and end_numbers required.")
        else:
            raise Exception("Invalid operation.")


################################################################################
@func_log
def reg_op(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        f = SimpleCounter(argspec)
        result = f.do(argspec.op)
        return result
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 99
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
            owner='ARGOS-LABS',
            group='7',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='Simple Counter',
            icon_path=get_icon_path(__file__),
            description='Simple Counter',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op', display_name='Function type',
                          choices=SimpleCounter.OP_TYPE,
                          help='Type of operation')
        mcxt.add_argument('start_number', display_name='Start Number',
                          type=int,
                          default=1,
                          help='Start Number start the operation and continue')
        mcxt.add_argument('end_numbers', display_name='End Number',
                          type=int,
                          default=1,
                          help='End Number end the operation')
        # ##################################### for app optional parameters
        mcxt.add_argument('--increment', display_name='Increment',
                          type=int,
                          default=1,
                          help='Increment can be +ve or -ve, default -1 or +1')
        argspec = mcxt.parse_args(args)
        return reg_op(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
