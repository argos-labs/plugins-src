"""
====================================
 :mod:`argoslabs.citizen.log`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS citizen log
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
from datetime import datetime
import logging


################################################################################
class CitizenLog(object):
    OP_TYPE = ['Initialize','Add Log']
    FILE_TYPE = ['TXT','LOG','CSV']
    OUTPUT_FORMATS = {
        # Data & Time
        'YYYYMMDD-HHMMSS.mmm': "%Y%m%d-%H%M%S.%f",
        'YYYY-MM-DD HH:MM:SS.mmm': "%Y-%m-%d %H:%M:%S.%f",
        'YYYY/MM/DD HH:MM:SS.mmm': "%Y/%m/%d %H:%M:%S.%f",
        'MMDDYYYY-HHMMSS.mmm': "%m%d%Y-%H%M%S.%f",
        'MM-DD-YYYY HH:MM:SS.mmm': "%m-%d-%Y %H:%M:%S.%f",
        'MM/DD/YYYY HH:MM:SS.mmm': "%m/%d/%Y %H:%M:%S.%f",
        'M/D/YYYY HH:MM:SS.mmm': "%-m/%-d/%Y %H:%M:%S.%f" if sys.platform != 'win32' else "%#m/%#d/%Y %H:%M:%S.%f",
        'YYYYMMDD-HHMMSS': "%Y%m%d-%H%M%S",
        'YYYY-MM-DD HH:MM:SS': "%Y-%m-%d %H:%M:%S",
        'YYYY/MM/DD HH:MM:SS': "%Y/%m/%d %H:%M:%S",
        'MMDDYYYY-HHMMSS': "%m%d%Y-%H%M%S",
        'MM-DD-YYYY HH:MM:SS': "%m-%d-%Y %H:%M:%S",
        'MM/DD/YYYY HH:MM:SS': "%m/%d/%Y %H:%M:%S",
        'M/D/YYYY HH:MM:SS': "%-m/%-d/%Y %H:%M:%S" if sys.platform != 'win32' else "%#m/%#d/%Y %H:%M:%S",
        # Date
        'YYYYMMDD': "%Y%m%d",
        'YYYY-MM-DD': "%Y-%m-%d",
        'YYYY/MM/DD': "%Y/%m/%d",
        'MMDDYYYY': "%m%d%Y",
        'MM-DD-YYYY': "%m-%d-%Y",
        'MM/DD/YYYY': "%m/%d/%Y",
        'M/D/YYYY': "%-m/%-d/%Y" if sys.platform != 'win32' else "%#m/%#d/%Y",
        'DD-MM-YYYY': "%d-%m-%Y",
        'DD.MM.YYYY': "%d.%m.%Y",
        'DD-MM-YY': "%d-%m-%y",
        'DD.MM.YY': "%d.%m.%y",
    }


    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec


    # ==========================================================================
    def create_file_name(self,_format):
        filename = datetime.now().strftime(self.OUTPUT_FORMATS[_format])
        while '/' in filename:
            filename = filename.replace('/','')
        while ':' in filename:
            filename = filename.replace(':','')
        return filename


    # ==========================================================================
    def init_fun(self):
        if not self.argspec.file_type:
            raise Exception("File Type required.")
        if not self.argspec.output_format:
            raise Exception("DateTime Format required.")
        _format = self.argspec.output_format
        filename = self.create_file_name(_format)
        if self.argspec.file_type == 'TXT':
            filename = f"{self.argspec.output}" \
                       f"\\{self.argspec.fIle_name}_{filename}.txt"
            logging.basicConfig(filename=filename,
                                filemode='a',
                                format=f'event_time'
                                       f' >>> '
                                       f'event_message')
        elif self.argspec.file_type == 'LOG':
            filename = f"{self.argspec.output}" \
                       f"\\{self.argspec.fIle_name}_{filename}.log"
            logging.basicConfig(filename=filename,
                                filemode='a',
                                format=f'event_time'
                                       f' |'
                                       f'event_message')
        elif self.argspec.file_type == 'CSV':
            filename = f"{self.argspec.output}" \
                       f"\\{self.argspec.fIle_name}_{filename}.csv"
            logging.basicConfig(filename=filename,
                                filemode='a',
                                format=f'event_time'
                                       f','
                                       f'event_message')
        print(f'{filename}', end='')


    # ==========================================================================
    def add_fun(self):
        if not self.argspec.output_format:
            raise Exception("DateTime Format required.")
        _format = self.argspec.output_format
        separator = None
        if not self.argspec.log_file_path:
            raise Exception("Log File Path required.")
        filename = f"{self.argspec.log_file_path}"
        fileName, fileExtension = os.path.splitext(filename)
        if not fileExtension:
            raise Exception("Invalid file format.")
        elif fileExtension == '.log':
            separator = ' |'
        elif fileExtension == '.txt':
            separator = ' >>> '
        elif fileExtension == '.csv':
            separator = ','
        if not self.argspec.event_message:
            raise Exception("Event Message required.")
        if self.argspec.event_time_with_single_quotes:
            FORMAT = f"'{datetime.now().strftime(self.OUTPUT_FORMATS[_format])}'" \
                     f"{separator}" \
                     f"{self.argspec.event_message}"
        else:
            FORMAT = f"{datetime.now().strftime(self.OUTPUT_FORMATS[_format])}" \
                     f"{separator}" \
                     f"{self.argspec.event_message}"
        logging.basicConfig(format=FORMAT, filename=filename,
                            filemode='a')
        print(f'{filename}', end='')


    # ==========================================================================
    def do(self, op):
        if not op:
            raise Exception("Select Function type")
        elif op == 'Initialize':
            self.init_fun()
        elif op == 'Add Log':
            self.add_fun()
        else:
            raise Exception("Invalid operation.")


################################################################################
@func_log
def reg_op(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        f = CitizenLog(argspec)
        f.do(argspec.op)
        return 0
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
            group='2',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='Citizen Log',
            icon_path=get_icon_path(__file__),
            description='Log Plugins',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op', display_name='Function type',
                          choices=CitizenLog.OP_TYPE,
                          help='Type of operation')
        mcxt.add_argument('output', display_name='Output Folder',
                          input_method='folderwrite',
                          help='A folder to save the result file')
        mcxt.add_argument('file_type', display_name='File Type',
                          choices=CitizenLog.FILE_TYPE,
                          help='File Type support txt, log, csv.')
        mcxt.add_argument('output_format', display_name='DateTime Format',
                          choices=list(CitizenLog.OUTPUT_FORMATS.keys()),
                          help='Set the format of DateTimeStamp')
        # ##################################### for app optional parameters
        mcxt.add_argument('--event_time_with_single_quotes',
                          display_name='Event Time With Single Quotes',
                          action='store_true',
                          help='Event Time With Single Quotes.')
        mcxt.add_argument('--fIle_name', display_name='FIle Name',
                          default='Log',
                          help='FIle Name')
        mcxt.add_argument('--log_file_path', display_name='Log File Path',
                          help='Log File Path to store log data.')
        mcxt.add_argument('--event_message',
                          display_name='Event Message',
                          help='Event Message')
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
