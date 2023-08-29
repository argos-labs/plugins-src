import os
import win32com.client

excel = win32com.client.Dispatch('Excel.Application')
excel_file = r'W:\ARGOS-LABS\src\plugins\argoslabs\data\excel\tests\Credentials.xlsx'
book = excel.Workbooks.Open(excel_file, None, True, None, 'argos0520')

temp_file = r'W:\ARGOS-LABS\src\plugins\argoslabs\data\excel\tests\Credentials-tmp.xlsx'
if os.path.exists(temp_file):
    os.remove(temp_file)
book.SaveAs(temp_file, None, '')
book.Close()
