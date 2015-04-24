import os
import zipfile
import zlib

def zipoutput(resultsfolder, tandemout):
    for root, dirs, files in os.walk(resultsfolder):
        for file in files:
            tandemout.write(os.path.join(root, file))


resultsfolder = '/Users/sbr/data/tandemout/113212012/'
zipfileout =  '/Users/sbr/data/tandemout/113212012/tandem.zip'
tandemout = zipfile.ZipFile(zipfileout, 'w', zipfile.ZIP_DEFLATED)
zipoutput(resultsfolder, tandemout)
tandemout.close()