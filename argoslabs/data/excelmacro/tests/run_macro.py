#Import the following library to make use of the DispatchEx to run the macro
import os
import sys
import win32com.client as win32
# noinspection PyUnresolvedReferences
import pywintypes


################################################################################
def run_macro(filename, func, *args):
    if not os.path.exists(filename):
        raise IOError('Cannot read file "%s"' % filename)

    excel_macro = None
    try:
        # DispatchEx is required in the newest versions of Python.
        excel_macro = win32.DispatchEx("Excel.Application")

        # excel_path = os.path.expanduser(filename)
        excel_path = os.path.abspath(filename)
        workbook = excel_macro.Workbooks.Open(Filename=excel_path, ReadOnly=1)
        # workbook = excel_macro.Workbooks.Open(filename)
        excel_macro.Application.Run(func, *args)  # excelsheet.xlsm!modulename.macroname
        #Save the results in case you have generated data
        workbook.Save()
        return 0
    except pywintypes.com_error as err:
        sys.stderr.write('Excel Error:%s\n' % (str(err)))
    except Exception as err:
        sys.stderr.write('%s\n' % str(err))
    finally:
        if excel_macro is not None:
            excel_macro.Application.Quit()
            del excel_macro


################################################################################
if __name__ == '__main__':
    # run_macro('stoptime.xls', 'Calculate')
    run_macro('macro_test01.xls', 'StartMe', 1, 'Hello World!')
