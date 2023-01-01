from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer

# import pixiedust

def parse_obj(lt_objs):

    # loop over the object list
    for obj in lt_objs:
        # print(obj.bbox)

        # if it's a textbox, print text and location
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            print ("%3.3f, %3.3f, %3.3f, %3.3f, %s" % (obj.bbox[0], obj.bbox[1], obj.bbox[2], obj.bbox[3], obj.get_text().replace('\n', '_')))

        # if it's a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure):
            parse_obj(obj._objs)

# Open a PDF file.
fp = open(r'광진invoice/CKCO.pdf', 'rb')

# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)

# Create a PDF document object that stores the document structure.
# Password for initialization as 2nd parameter
document = PDFDocument(parser)

# Check if the document allows text extraction. If not, abort.
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed

# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()

# # Create a PDF device object.
# device = PDFDevice(rsrcmgr)

laparams = LAParams()
print(laparams)

# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)

# Create a PDF interpreter object.
interpreter = PDFPageInterpreter(rsrcmgr, device)

# loop over all pages in the document
for page in PDFPage.create_pages(document):
    # Page Size in pints
    # 아래쪽의 layout 정보와 동일함
    # print(page.mediabox)

    # read the page into a layout object
    interpreter.process_page(page)
    layout = device.get_result()
    print(layout)

    parse_obj(layout._objs)

