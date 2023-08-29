import os
import sys
import csv
from io import StringIO
from docx import Document
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph


################################################################################
def iter_block_items(parent):
    """
    Generate a reference to each paragraph and table child within *parent*,
    in document order. Each returned value is an instance of either Table or
    Paragraph. *parent* would most commonly be a reference to a main
    Document object, but also works for a _Cell object, which itself can
    contain paragraphs and tables.
    """
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
        # print(parent_elm.xml)
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("something's not right")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


################################################################################
def get_csv_table(table, is_merge=False, merge_check_col=0):
    so = StringIO()
    c = csv.writer(so, lineterminator='\n')
    p_row = None
    for i, row in enumerate(table.rows):
        row = [cell.text for cell in row.cells]
        if not is_merge:
            c.writerow(row)
            continue
        if row[merge_check_col]:
            if p_row:
                c.writerow(p_row)
            p_row = row
        else:
            if not p_row:
                p_row = row
            else:
                for i in range(len(row)):
                    if row[i]:
                        p_row[i] += '\n' + row[i]
    if p_row:
        c.writerow(p_row)
    return so.getvalue()


################################################################################
def ext_docx(docx_file, is_merge=False, merge_check_col=0):
    if not os.path.exists(docx_file):
        raise IOError(f'Cannot read docx file "{docx_file}"')
    document = Document(docx_file)
    table_cnt = 0
    for block in iter_block_items(document):
        # print('found one')
        # print(block.text if isinstance(block, Paragraph) else '<table>')
        print()
        if isinstance(block, Paragraph):
            print(block.text)
        else:
            print(get_csv_table(document.tables[table_cnt],
                                is_merge=is_merge,
                                merge_check_col=merge_check_col))
            table_cnt += 1


################################################################################
if __name__ == '__main__':
    # _docx_file = 'foo-01.docx'
    _docx_file = 'basic.docx'
    ext_docx(_docx_file, is_merge=True)
