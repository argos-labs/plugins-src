################################################################################
import os
import pdfminer
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pprint import pformat


################################################################################
class PDFMiner(object):
    # ==========================================================================
    def __init__(self, pdf_file):
        if not os.path.exists(pdf_file):
            raise IOError(f'Cannot find pdf file "{pdf_file}"')
        self.pdf_file = pdf_file
        # for internal
        self.pages = []

    # ==========================================================================
    def _parse_obj(self, lt_objs, textboxes):
        for obj in lt_objs:
            # if it's a textbox, print text and location
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                # print("%3.3f, %3.3f, %3.3f, %3.3f, %s" % (
                #     obj.x0, obj.y0, obj.x1, obj.y1, obj.get_text().strip()
                # ))
                assert(obj.bbox[0] == obj.x0 and obj.bbox[1] == obj.y0 and
                       obj.bbox[2] == obj.x1 and obj.bbox[3] == obj.y1)
                textboxes.append((round(obj.x0, 3), round(obj.y0, 3),
                                  round(obj.x1, 3), round(obj.y1, 3),
                                  obj.get_text().strip()))
            # if it's a container, recurse
            elif isinstance(obj, pdfminer.layout.LTFigure):
                # noinspection PyProtectedMember
                self._parse_obj(obj._objs, textboxes)

    # ==========================================================================
    def do_miner(self):
        with open(self.pdf_file, 'rb') as ifp:
            parser = PDFParser(ifp)
            document = PDFDocument(parser)
            if not document.is_extractable:
                raise PDFTextExtractionNotAllowed('Image base PDF cannot be extract text')
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(document):
                interpreter.process_page(page)
                layout = device.get_result()
                # print(layout)
                page_d = {
                    'pageid': layout.pageid,
                    'width': layout.width,
                    'height': layout.height,
                    'rotate': layout.rotate,
                    'textboxes': []
                }
                # noinspection PyProtectedMember
                self._parse_obj(layout._objs, page_d['textboxes'])
                self.pages.append(page_d)

    # ==========================================================================
    def __repr__(self):
        sl = list()
        sl.append(f'# of pages: {len(self.pages)}')
        for page_d in self.pages:
            sl.append(pformat(page_d, 4))
        return '\n'.join(sl)


################################################################################
if __name__ == '__main__':
    pm = PDFMiner('광진invoice/all5.pdf')
    pm.do_miner()
    print(pm)
