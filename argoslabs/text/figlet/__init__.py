"""
====================================
 :mod:`argoslabs.text.figlet`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module to use pyfiglet
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/12]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2021/02/02]
#     - starting

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from pyfiglet import Figlet


################################################################################
DIRECTION_LIST = [
    'auto',
    'left-to-right',
    'right-to-left',
]
JUSTIFY_LIST = [
    'auto',
    'left',
    'right',
]


################################################################################
@func_log
def do_figlet(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if not argspec.message:
            raise ValueError(f'Invalid Message')
        direction = argspec.direction
        justify = argspec.justify
        width = int(argspec.width)
        f = Figlet(font=argspec.font, direction=direction,
                   justify=justify, width=width)
        print(f.renderText(argspec.message), end='')
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
        owner='ARGOS-LABS',
        group='9',  # Utility Tools
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='ASCII Art',
        icon_path=get_icon_path(__file__),
        description='''AscII Art using Figlet''',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('font',
                          display_name='Font',
                          choices=Figlet().getFonts(),
                          default='standard',
                          help='Select font for ascii art')
        mcxt.add_argument('message',
                          display_name='Message',
                          help='Message for ASCII Art')

        # ##################################### for app dependent options
        mcxt.add_argument('--direction',
                          display_name='Text Direction',
                          choices=DIRECTION_LIST,
                          default=DIRECTION_LIST[0],
                          help='Text direction, default [[auto]] means font''s direction')
        mcxt.add_argument('--justify',
                          display_name='Text Justify',
                          choices=JUSTIFY_LIST,
                          default=JUSTIFY_LIST[0],
                          help='Text justfy, default [[auto]] means font''s justify')
        mcxt.add_argument('--width',
                          display_name='Text Width',
                          type=int,
                          default=80,
                          help='Text width, default [[80]] columns')
        argspec = mcxt.parse_args(args)
        return do_figlet(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
