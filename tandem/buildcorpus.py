from __future__ import unicode_literals
__author__ = 'sbr'
import os
import sys
import shutil
from cStringIO import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from PIL import Image
import pytesseract



def process_image(file):            #helper function to OCR a singe file
    input_image = (Image.open(file)).convert('RGB')
    output_data = pytesseract.image_to_string(input_image)
    return output_data

def ocrit(infullpath, outfullpath, file):          #run Tesseract OCR engine using process_image()
    cfile = os.path.splitext(outfullpath)[0] + '.txt'
    temp = open(cfile, 'w')
    temp.write (str(process_image(infullpath)))
    temp.close()

def pdfconvert(infullpath, file, outfullpath, pages=None):         #Handle PDF
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    pdffile = open(infullpath, 'rb')
    for page in PDFPage.get_pages(pdffile, pagenums):
        interpreter.process_page(page)
    pdffile.close()
    converter.close()
    txtfilename = file

    jpgfile = os.path.splitext(outfullpath)[0] + '.jpg'
    txtfile = os.path.splitext(outfullpath)[0] + '.txt'
    text = output.getvalue()
    output.close
    temp = open(txtfile, 'w')
    temp.write (text)
    temp.close()

    imagemagick_string = 'convert ' + '"' + infullpath + '" "' + jpgfile + '"'
    os.system(imagemagick_string)


def analysis_setup(ipath, cpath, rpath):
    inputlist = []
    corpuspath = cpath

    if os.path.exists(corpuspath):
        pass
    else:
        os.mkdir(corpuspath)

    resultspath = rpath
    if os.path.exists(resultspath):
        pass
    else:
        os.mkdir(resultspath)

    infiles = [ f for f in os.listdir(ipath) if os.path.isfile(os.path.join(ipath,f)) ]
    for file in infiles:
        infullpath = ipath + '/' + file
        corpfullpath = corpuspath + '/' + file
        infilename = os.path.splitext(file)[0]
        inextension = os.path.splitext(file)[1]

        if inextension == '.tiff':
            inputlist.append(file)
            ocrit(infullpath, corpfullpath, file)
            print "corp=", corpuspath
            shutil.copy2(infullpath, corpfullpath)
        elif inextension == '.jpg':
            inputlist.append(file)
            ocrit(infullpath, corpfullpath, file)
            shutil.copy2(infullpath, corpfullpath)
        elif inextension == '.png':
            inputlist.append(file)
            ocrit(infullpath, corpfullpath, file)
            shutil.copy2(infullpath, corpfullpath)
        elif inextension == '.pdf':
            print file
            inputlist.append(file)
            pdfconvert(infullpath, infilename, corpfullpath)

    print inputlist
    return inputlist