__author__ = 'sbr'
import os
import sys
import csv
import numpy as np
import cv2
from nltk.corpus import stopwords
from nltk.corpus.reader import WordListCorpusReader
from nltk.tokenize import RegexpTokenizer

def image_extract(image):
    image_input = cv2.imread(image)
    image_size = image_input.size
    image_shape = image_input.shape
    image_meanrgb = cv2.mean(image_input)
    i_means, i_stds = cv2.meanStdDev(image_input)

    image_stats = np.concatenate([i_means,i_stds]).flatten()
    return image_size, image_shape, image_meanrgb, image_stats

def tokenize_file(file, corpus_root, english_stops):            #tokenize input file, count words, characters, remove stopwords
    tokenizer = RegexpTokenizer(r'\w+')
    item_count = 0
    total_chars = 0
    word_count = 0
    wordlist = []

    reader = WordListCorpusReader(corpus_root, file)
    chunks = reader.words()

    for item in chunks:
        total_chars += len(chunks[item_count])
        word_tokens = tokenizer.tokenize(chunks[item_count])
        word_count += len(word_tokens)
        item_count += 1
        for word in word_tokens:
            wordlist.append(word)
    stopsout = [word for word in wordlist if word.lower() not in english_stops]
    return wordlist, stopsout, word_count, total_chars

def build_sorted_ascii(wordlist):       #convert to ascii, lowercase and sort
    i = 0
    templist = []
    for word in wordlist:
        temp = wordlist[i].encode('ascii', 'ignore')
        templist.append(temp.lower())
        i += 1
    sorted_wordlist = sorted(templist)
    return sorted_wordlist

def build_unique_list(inlist):        #find unique words and count them
    unique = [inlist[0].lower()]
    countlist = [1]
    i = 1
    o = 0

    for i in range(1, len(inlist)):
        if inlist[i].lower() == unique[o]:
            countlist[o] += 1
        else:
            unique.append(inlist[i].lower())
            countlist.append(1)
            o += 1
        i += 1
    return unique, countlist

def merge_all(folder):
    txtfiles = [ f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f)) ]
    wholebook = folder + '/Tandem' + 'AllText.txt'
    with open(wholebook, 'w') as outfile:
        for file in txtfiles:
            fullname = folder + '/'+ file
            if os.path.splitext(file)[1] == '.txt':
                with open(fullname) as infile:
                    outfile.write(infile.read())

def write_first_row(outfolder, outname, filename0, imgsize, imgshape, imgmeanrgb, imgstats, txtdat):               #write the first row of the main output file
    global outputopen, goflag
    #print "stats=", imgstats
    with open(outname, 'wb') as csvfile:
        tandemwriter = csv.writer(csvfile, delimiter=',',
                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
        tandemwriter.writerow(['File','Total Word Count', 'Total Characters', 'Average Word Length',
                   'Unique Word Count', 'Count wout Stopword', 'Image Size','Image Shape 1', 'Image Shape 2',
                   'Image Shape 3', 'Image Mean R', 'Image Mean G', 'Image Mean B', 'Image Mean 4','Image Stats'])
        tandemwriter.writerow([filename0]+[txtdat[0]]+[txtdat[1]]+[txtdat[2]]+[txtdat[3]]+
                      [txtdat[4]]+[imgsize]+[imgshape]+[imgmeanrgb]+[imgstats])
        outputopen = True
        write_the_lists(outfolder, filename0, txtdat)

def write_the_rest(outfolder, outname, filename0, imgsize, imgshape, imgmeanrgb, imgstats, txtdat):
    #write subsequent rows of main output file

    with open(outname, 'a') as csvfile:
            tandemwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            tandemwriter.writerow([filename0]+[txtdat[0]]+ [txtdat[1]]+[txtdat[2]]+[txtdat[3]]+
                    [txtdat[4]]+[imgsize]+[imgshape]+[imgmeanrgb]+[imgstats])
    write_the_lists(outfolder, filename0, txtdat)

def write_the_last(outfolder, outname, filename0, txtdat):                #write subsequent rows of main output file
    with open(outname, 'a') as csvfile:
            tandemwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            tandemwriter.writerow([filename0]+[txtdat[0]]+ [txtdat[1]]+[txtdat[2]]+[txtdat[3]]+
                    [txtdat[4]])
    write_the_lists(outfolder, filename0, txtdat)

def write_the_lists(folder, filename, txtdat):
    #write list of all the words
    words_csv = folder + '/' + filename + '_allwords.csv'
    with open(words_csv, 'wb') as csvfile:
            wlwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            wlwriter.writerow(['All Words'])
            for item in txtdat[6]:
                wlwriter.writerow([item])

    #write a list of unique words with counts other than stop words
    unique_csv = folder + '/' + filename + '_unique.csv'
    with open(unique_csv, 'wb') as csvfile:
            i = 0
            unwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            unwriter.writerow(['Unique Non Stop Words', 'Count'])
            for i in range (0, len(txtdat[5])):
                unwriter.writerow([txtdat[5][i]]+[txtdat[5][i]])
                i += 1

def mainout(corpusfolder, outfolder):
    global outputopen
    outputopen = False
    isize = 0
    ishape  = 0
    imeanrgb = []
    istats = []
    isizelist = []
    ishapelist = []
    imeanrgblist = []
    istatslist = []
    english_stops = stopwords.words('english')

    merge_all(corpusfolder)         #combine all the textfiles into one large textfile

    outfile = outfolder + '/tandem' + 'main.csv'


    corpfiles = [ f for f in os.listdir(corpusfolder) if os.path.isfile(os.path.join(corpusfolder,f)) ]
    for file in corpfiles:
        if os.path.splitext(file)[1] <> '.txt':
            imgfile = corpusfolder + '/' + file
            isize, ishape, imeanrgb, istats = image_extract(imgfile)
            isizelist.append(isize)
            ishapelist.append(ishape)
            imeanrgblist.append(imeanrgb)
            istatslist.append(istats)
    nltkfiles = [ g for g in os.listdir(corpusfolder) if os.path.isfile(os.path.join(corpusfolder,g)) ]
    count = 0
    for file in nltkfiles:
        nltkdata = []
        if os.path.splitext(file)[1] == '.txt':
            namestring = os.path.splitext(file)[0]
            allwords, nonstops, allcount, allchar = tokenize_file(file, corpusfolder, english_stops)
            if allcount == 0:
                avg_word_length = 'na'
            else:
                avg_word_length = round(float(allchar)/float(allcount), 2)
            ascii_sorted = []
            ascii_sorted = build_sorted_ascii(allwords)
            nonstop_sorted = []
            nonstop_sorted = build_sorted_ascii(nonstops)
            if len(nonstop_sorted) > 0:
                unique_nonstop_words, nonstop_counts  = build_unique_list(nonstop_sorted)
            else:
                unique_nonstop_words = []
                nonstop_counts = []
            nltkdata.append(allcount)
            nltkdata.append(allchar)
            nltkdata.append(avg_word_length)
            nltkdata.append(len(unique_nonstop_words))
            nltkdata.append(len(nonstops))
            nltkdata.append(unique_nonstop_words)
            nltkdata.append(ascii_sorted)
            if outputopen:
                print "writing the rest"
                if namestring <> "TandemAllText":
                    write_the_rest(outfolder, outfile, namestring, isizelist[count], ishapelist[count],
                        imeanrgblist[count], istatslist[count], nltkdata)
                else:
                    write_the_last(outfolder, outfile, namestring, nltkdata)
            else:
                print "count=", count
                write_first_row(outfolder, outfile, namestring, isizelist[count], ishapelist[count],
                    imeanrgblist[count], istatslist[count], nltkdata)
            print namestring
            if namestring <> "TandemAllText":
                count += 1




