from __future__ import unicode_literals
__author__ = 'sbr'
from django.core.files import File
from django.core.files.images import ImageFile
from django.core.files.storage import default_storage
import os
from django.core.files.base import ContentFile
import cv2
import numpy as np
import pytesseract
import nltk
from PIL import Image
from nltk.corpus.reader import WordListCorpusReader
from nltk.tokenize import RegexpTokenizer

#with open('tandemdh.ini', 'r') as g:
#    myfile2 = File(g)
#    testd = myfile2.readlines()[1]


def process_image(file):            #helper function to OCR a singe file
    input_image = (Image.open(file)).convert('RGB')
  #  input_image = input_image.convert('RGB')
    output_data = pytesseract.image_to_string(input_image)
    return output_data

def ocrit(file):          #run Tesseract OCR engine using process_image()
    temp = open("test.txt", 'w')
    temp.write (str(process_image(file)))
    temp.close()


def image_extract(image):
    image_input = cv2.imread(image)
    image_size = image_input.size
    image_shape = image_input.shape
    image_meanrgb = cv2.mean(image_input)
    i_means, i_stds = cv2.meanStdDev(image_input)

    image_stats = np.concatenate([i_means,i_stds]).flatten()
    x = 0
    for i in image_stats:
        print "x=",x,"stat=",image_stats[x]
        x += 1
    return image_size, image_shape, image_meanrgb, image_stats

with open(file, 'rb') as img:
    imgfile = ImageFile(img)
    print imgfile._get_size()
    ocrit(imgfile.name)
    print image_extract(imgfile.name)

with open(file, 'rb') as txt:
    txtfile = File(txt)
    txtcontent = txtfile.read()
    print type(txtcontent)
    print txtcontent

    tokenizer = RegexpTokenizer(r'\w+')
    item_count = 0
    total_chars = 0
    word_count = 0
    wordlist = []

    reader = WordListCorpusReader('.',txtfile.name)
    chunks = reader.words()

