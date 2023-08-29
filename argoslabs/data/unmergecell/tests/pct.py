# import xlrd
#
# book = xlrd.open_workbook('sample-merged-excel.xls', formatting_info=True)
# ws = book.sheets()
# for i in ws:
#     print(i.cell('a1','a1').value)
import csv
import sys
c = csv.writer(sys.stdout,lineterminator = '\n')
h =( ('lng', 'encoding', 'cofidence'), ('kor', 'utf-8', '0.9'))
s = ('kor', 'utf-8', '0.9')
for i in h:
    c.writerow((i[0],i[1],i[2]))