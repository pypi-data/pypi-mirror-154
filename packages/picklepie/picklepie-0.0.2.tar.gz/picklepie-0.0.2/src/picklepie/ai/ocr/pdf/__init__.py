import PyPDF2 as __pdf

import picklepie as __pp

# https://www.simplifiedpython.net/pdf-to-text-python-extract-text-from-pdf-documents-using-pypdf2-module/
# https://realpython.com/pdf-python/

class __result :
    num_of_pages = None
    author = None
    creator = None
    producer = None
    subject = None
    title = None
    text = {}

def read (a_file='') :
    loc_pdf = open(a_file,'rb')
    loc_reader = __pdf.PdfFileReader(loc_pdf)
    loc_result = __result()
    loc_information = loc_reader.getDocumentInfo()
    loc_information.author
    loc_information.creator
    loc_information.producer
    loc_information.subject
    loc_information.title
    loc_result.num_of_pages = loc_reader.numPages
    for i in range(loc_reader.numPages) :
        loc_result.text[i+1] = loc_reader.getPage(i).extractText()
    return loc_result
