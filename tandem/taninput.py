from __future__ import unicode_literals
__author__ = 'sbr'
import os
import sys
import datetime
from cStringIO import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
import cv2
import numpy as np
import pytesseract
import nltk
from PIL import Image
from nltk.corpus.reader import WordListCorpusReader
from nltk.tokenize import RegexpTokenizer


def process_image(file):            #helper function to OCR a singe file
    input_image = (Image.open(file)).convert('RGB')
    output_data = pytesseract.image_to_string(input_image)
    return output_data

def ocrit(infullpath, file):          #run Tesseract OCR engine using process_image()
    cfile = os.path.splitext(file)[0]
    corpusfullpath = corpuspath + corpusfolder + '/' + cfile + '.txt'
    temp = open(corpusfullpath, 'w')
    temp.write (str(process_image(infullpath)))
    temp.close()



def image_extract(image):
    image_input = cv2.imread(image)
    image_size = image_input.size
    image_shape = image_input.shape
    image_meanrgb = cv2.mean(image_input)
    i_means, i_stds = cv2.meanStdDev(image_input)

    image_stats = np.concatenate([i_means,i_stds]).flatten()
    return image_size, image_shape, image_meanrgb, image_stats

def make_corpus_folder(x):              #Create a folder for the OCR Output/NLTK input
    dirname = 'corpus' + str(datetime.datetime.now())
    count = 1
    while True:
        try:
            os.mkdir(x + dirname)
            break
        except(OSError):
            dirname = 'corpus' + str(count)
            count += 1
            if count > 10:
                dirname = ''
                print "Aborting. Failed to create output folder!"
                sys.exit(9999)
            else:
                print "could not create folder ", x + dirname, "...retrying..."
    corpuspath = x + dirname
    return dirname

def analyze(serverpath):
    corpuspath = os.getenv("HOME") + "/data/tandemcorpus/"
    resultspath = os.getenv("HOME") + "/data/tandemout/"


    corpusfolder = make_corpus_folder(corpuspath) #create a subfolder in the tandemcorpus folder

    infiles = [ f for f in os.listdir(serverpath) if os.path.isfile(os.path.join(serverpath,f)) ]
    for file in infiles:
        print ("Processing " + file)
        infullpath = serverpath + file
        infilename = os.path.splitext(file)[0]
        inextension = os.path.splitext(file)[1]
        if inextension == '.tiff':
            ocrit(infullpath, file)
            isize, ishape, imeanrgb, istats = image_extract(infullpath)
        elif inextension == '.jpg':
           ocrit(infullpath, file)
           isize, ishape, imeanrgb, istats = image_extract(infullpath)
        elif inextension == '.png':
            ocrit(infullpath, file)
            isize, ishape, imeanrgb, istats = image_extract(infullpath)
        elif inextension == '.pdf':
            jpegfile = pdfconvert(infullpath, infilename, serverpath)
            isize, ishape, imeanrgb, istats = image_extract(jpegfile)
        else:
            print "\n", file + " is not an image file. Skipped... "
#        isizelist.append(isize)
#        ishapelist.append(ishape)
#        imeanrgblist.append(imeanrgb)
#        istatslist.append(istats)

