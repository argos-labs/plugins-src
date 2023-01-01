import glob
import os
import pandas as pd
from pandas import ExcelWriter
from openpyxl import load_workbook

wdir = r"{wdir}"
in_files = (
    os.path.join(wdir, '1.xlsx'),
    os.path.join(wdir, '2.xlsx'),
    os.path.join(wdir, '3.xlsx'),
)
out_file = os.path.join(wdir, 'task2.xlsx')
writer = ExcelWriter(out_file, engine='openpyxl')
num_rows = 0
for filename in in_files:
    excel_file = pd.ExcelFile(filename)
    (_, f_name) = os.path.split(filename)
    (f_short_name, _) = os.path.splitext(f_name)
    for sheet_name in excel_file.sheet_names:
        df_excel = pd.read_excel(filename)
        df_excel.to_excel(writer,index=False,header=False,startrow=num_rows+1)
        num_rows += df_excel.shape[0]
writer.save()
print(os.path.abspath(out_file), end='')
