"""
====================================
 :mod:`argoslabs.pivot.table`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Managing Excel
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
import warnings
import pandas as pd

################################################################################
class Xlsx_pt(object):
    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.directory_path = None
        self.input_file_path = None


    # ==========================================================================
    def convert(self):
        if not self.argspec.input_file_path.endswith(".xlsx"):
            raise IOError('xlsx file only."%s"' % self.argspec.input_file_path)
        if not self.argspec.out_file_path.endswith(".xlsx"):
            raise IOError('xlsx file only."%s"' % self.argspec.out_file_path)
        if not self.argspec.pivot_index:
            raise Exception('Pivot Index required.')
        if not self.argspec.pivot_columns:
            raise Exception('Pivot Columns required.')
        if not self.argspec.output_sheet_name:
            self.argspec.output_sheet_name = self.argspec.input_sheet_name
        self.input_file_path = self.argspec.input_file_path
        df2 = pd.read_excel(self.input_file_path, sheet_name=self.argspec.input_sheet_name)
        df = pd.DataFrame(df2)
        for i in self.argspec.pivot_columns:
            df[i] = df[i].str.lower()
        pivot_table = pd.pivot_table(df, index=self.argspec.pivot_index,
                                     columns=self.argspec.pivot_columns,
                                     aggfunc='size', fill_value=0,
                                     margins_name='Total')
        pivot_table.loc['Total'] = pivot_table.sum()
        pivot_table_with_sum = pivot_table.assign(Total=pivot_table.sum(axis=1))
        if f'{self.argspec.out_file_path}' == f'{self.argspec.input_file_path}':
            with pd.ExcelWriter(self.argspec.out_file_path,mode='a') as writer:
                pivot_table_with_sum.to_excel(writer, sheet_name=self.argspec.output_sheet_name)
        else:
            pivot_table_with_sum.to_excel(self.argspec.out_file_path,
                                          sheet_name=self.argspec.output_sheet_name,
                                          startrow=3,
                                          startcol=2)
        print(self.argspec.out_file_path,end='')


################################################################################
@func_log
def reg_op(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        warnings.simplefilter("ignore", ResourceWarning)
        f = Xlsx_pt(argspec)
        f.convert()
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
            owner='ARGOS-LABS',
            group='9',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='Pivot Table',
            icon_path=get_icon_path(__file__),
            description='create Pivot Table',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('input_file_path', display_name='Input File path',
                          input_method='fileread',
                          help='xlsx file path')
        # ----------------------------------------------------------------------
        mcxt.add_argument('out_file_path', display_name='Output File path',
                          input_method='fileread',
                          help='xlsx file path')
        # ----------------------------------------------------------------------
        mcxt.add_argument('input_sheet_name', display_name='Input Sheet Name',
                          help='Input Sheet Name')
        # ----------------------------------------------------------------------
        mcxt.add_argument('pivot_index', display_name='Pivot Index',
                          action='append',
                          help='Pivot Index')
        # ----------------------------------------------------------------------
        mcxt.add_argument('pivot_columns', display_name='Pivot Columns',
                          action='append',
                          help='Pivot Columns')
        # ##################################### for app optional parameters
        mcxt.add_argument('--output_sheet_name', display_name='Output Sheet Name',
                          help='Output Sheet Name')

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
