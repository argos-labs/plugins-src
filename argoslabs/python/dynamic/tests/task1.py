import os
import pandas as pd
from pandas import ExcelWriter

wdir = r"{wdir}"
in_files = (
    os.path.join(wdir, '1.xlsx'),
    os.path.join(wdir, '2.xlsx'),
    os.path.join(wdir, '3.xlsx'),
)
out_file = os.path.join(wdir, 'task1.xlsx')
writer = ExcelWriter(out_file)
for filename in in_files:
    excel_file = pd.ExcelFile(filename)
    (_, f_name) = os.path.split(filename)
    (f_short_name, _) = os.path.splitext(f_name)
    for sheet_name in excel_file.sheet_names:
        df_excel = pd.read_excel(filename, sheet_name=sheet_name)
        df_excel.to_excel(writer, f_short_name+'_'+sheet_name, index=False)
writer.save()
print(os.path.abspath(out_file), end='')
