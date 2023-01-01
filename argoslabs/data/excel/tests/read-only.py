import openpyxl

wb = openpyxl.load_workbook(r"C:\work\Bots\ExcelAdv\TestXLXS_0613.xlsx",
                            data_only=True)
ws = wb['Sheet1']
v = ws['C1'].value
print(v)
