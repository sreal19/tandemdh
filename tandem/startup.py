__author__ = 'sbr'


from django.core.files.storage import FileSystemStorage
import os, time

inputhome = ''
corpushome = ''
resultshome = ''

print "start"


def start_project():
    global inputhome, corpushome, resultshome
    mytime = time.strftime("%j:%H:%M:%S")
    timestamp = mytime.replace(":","")
    print "setting time"
    outstorage = FileSystemStorage()
    print "outstorage=", outstorage.location
    inputhome = outstorage.location + '/tandemin/' + timestamp
    corpushome = outstorage.location + '/tandemcorpus/' + timestamp
    resultshome = outstorage.location + '/tandemout/' + timestamp

def make_input_folder(inputpath):

    if os.path.exists(inputpath):
        print "inputpath exists=", inputpath
        pass
    else:
        print "making inputpath=", inputpath
        os.mkdir(inputpath)

def make_corpus_folder(corpuspath):
    corp_bld_status = 0
    if os.path.exists(corpuspath):
        print "corpuspath exists=", corpuspath
        pass
    else:
        print "making corpuspath=", corpuspath
        os.mkdir(corpuspath)

def make_results_folder(resultspath):
    if os.path.exists(resultspath):
        print "resultspath exists=", resultspath
        pass
    else:
        print "making resultspath=", resultspath
        os.mkdir(resultspath)

def get_paths():
    global inputhome, corpushome, resultshome
    return inputhome, corpushome, resultshome

def run():
    start_project()
    print "making input folder"
    make_input_folder(inputhome)

    print "making corpus folder"
    make_corpus_folder(corpushome)

    print "making results folder"
    make_results_folder(resultshome)



