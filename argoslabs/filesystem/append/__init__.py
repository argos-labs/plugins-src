"""
====================================
 :mod:`argoslabs.filesystem.append`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for appending to a file
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2019/12/02]
#     - starting

################################################################################
import os
import sys
import csv
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
OP_LIST = [
    'String',
    'Line',
    'CSV Row',
]


################################################################################
@func_log
def do_append(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    ofp = None
    try:
        if argspec.op not in OP_LIST:
            raise IOError('Invalid Operation "%s"' % argspec.op)
        if not argspec.append_file:
            raise IOError('Invalid append-file')
        if not argspec.contents:
            raise ValueError('Contents to append is not given!')
        try:
            ofp = open(argspec.append_file, 'a', encoding='utf-8')
        except Exception:
            raise IOError('Cannot write to the file "%s"' % argspec.append_file)
        if argspec.op == 'Line':
            argspec.end_with_line = True
        if argspec.op in ('String', 'Line'):
            for c in argspec.contents:
                ofp.write(c)

        elif argspec.op == 'CSV Row':
            c = csv.writer(ofp, lineterminator='\n')
            c.writerow(argspec.contents)
        if argspec.end_with:
            ofp.write(argspec.end_with)
        if argspec.end_with_line:
            ofp.write('\n')
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        if ofp is not None:
            ofp.close()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
        owner='ARGOS-LABS',
        group='filesystem',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='File Append',
        icon_path=get_icon_path(__file__),
        description='Append operation to a file',
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--end-with',
                          display_name='End With Str',
                          help='String ends with')
        # ######################################## for app dependent options
        mcxt.add_argument('--end-with-line',
                          display_name='End Line', action='store_true',
                          help='String ends with new line')
        # ##################################### for app dependent parameters
        mcxt.add_argument('op',
                          display_name='Operation', choices=OP_LIST,
                          help='Type of operation for appending')
        mcxt.add_argument('append_file',
                          display_name='Append file', input_method='filewrite',
                          help='file to append')
        mcxt.add_argument('contents',
                          display_name='Contents', nargs="+",
                          help='Contents to append')
        argspec = mcxt.parse_args(args)
        return do_append(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
