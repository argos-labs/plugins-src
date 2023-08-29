"""
====================================
 :mod:`argoslabs.api.filedownloader`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS managing API File Downloader
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
import pathlib
import sys
import requests
import warnings
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from urllib3.exceptions import InsecureRequestWarning


################################################################################


class Url2file(object):


    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec


    # ==========================================================================
    def filedownloader(self):
        try:
            filename = os.path.basename(self.argspec.url)
            file_extension = pathlib.Path(filename).suffix
            if self.argspec.filename:
                filename = f'{self.argspec.filename}{file_extension}'
            r = requests.get(self.argspec.url, allow_redirects=True, verify=False)
            file_path = f'{self.argspec.directory_path}/{filename}'
            open(file_path, 'wb').write(r.content)
            print(file_path, end='')
        except Exception as err:
            raise Exception(str(err))


################################################################################
@func_log
def reg_op(mcxt, argspec):
    warnings.simplefilter("ignore", ResourceWarning)
    warnings.simplefilter("ignore", InsecureRequestWarning)
    mcxt.logger.info('>>>starting...')
    try:
        f = Url2file(argspec)
        f.filedownloader()
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
            owner='ARGOS-LABS-DEMO',
            group='10',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='File Downloader',
            icon_path=get_icon_path(__file__),
            description='managing API File Downloader',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('url', display_name='URI',
                          help='URI Have file extension')
        # ----------------------------------------------------------------------
        mcxt.add_argument('directory_path', display_name='Directory Path',
                          help='Output Folder', input_method='folderread')
        # ##################################### for app optional parameters
        mcxt.add_argument('--filename', display_name='File Name',
                          help='File Name without extension and without space')
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
