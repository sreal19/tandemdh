from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, QueryDict, HttpRequest
from django.core.servers.basehttp import FileWrapper
from django.template import RequestContext, loader
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.views.static import serve
#from django.shortcuts import render_to_response
import time, tempfile, zipfile, zlib
import os, shutil
from cStringIO import StringIO


from .forms import MyUploadForm, ProjectForm

import buildcorpus, calculate
from TandemDH import settings
from tandem.models import Project
from tandem import startup

pname = ''
ziphome = settings.MEDIA_ROOT

def handle_uploaded_file(f):
    status = 'ok'
    inputhome, corpushome, resultshome = startup.get_paths()
    if inputhome != '':
        print inputhome, "uploading"
        fullname = inputhome + '/' + str(f.name)
        with open(fullname, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    else:
        status = "upload failure"
    return status

def build_the_corpus():
    inputhome, corpushome, resultshome = startup.get_paths()
    processlist = buildcorpus.analysis_setup(inputhome, corpushome, resultshome)
    return processlist

def make_zip(path, zip):
    zipdata = StringIO()
    zipf = zipfile.ZipFile(zipdata, 'w')

    for root, dirs, files in os.walk(path):
        print "zip folder", root
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close
    zipdata.seek(0)
    zipresponse = HttpResponse(zipdata.read())
    return zipresponse

def make_zip_new(path, zip):
    zipdata = StringIO()
    zipf = zipfile.ZipFile(zipdata, 'w', zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(path)
    for dirname, subdirs, files in os.walk(path):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname,filename))
            arcname = absname[len(abs_src) + 1:]
            print 'zipping %s as %s' % (os.path.join(dirname,filename), arcname)
            zipf.write(os.path.join(absname, arcname))
    zipf.close
    zipdata.seek(0)
    zipresponse = HttpResponse(zipdata.read())
    return zipresponse


def upload(request):
    upload_status = 'ok'
    if request.method == 'POST':
        form = MyUploadForm(request.POST, request.FILES)
        if form.is_valid():
            for f in request.FILES.getlist('attachments'):
                upload_status = handle_uploaded_file(f)
            if upload_status == 'ok':
                print "upload ok"
                return HttpResponseRedirect('analyze')
    else:
        form = MyUploadForm()
    if upload_status <> 'ok':
        print "upload failed"
    template = loader.get_template('tandem/upload.html')
    context = RequestContext(request,{'form':form})
    return HttpResponse(template.render(context))

def index(request):
    startup.run()
    tempvariable = "start"
    context = {'tempvariable': tempvariable}
    return render(request, 'tandem/index.html', context)

def project(request):
    global pname
    inputhome, corpushome, resultshome = startup.get_paths()
    p = Project()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        mystorage = FileSystemStorage()

        if form.is_valid():

            new_project = form.save(commit=False)
            new_project.input_folder = inputhome
            new_project.text_folder = corpushome
            new_project.dest_folder = resultshome
            new_project.save()
            pname = new_project.project_name
        return HttpResponseRedirect('upload')
    else:
        print "fresh form...start"
        form = ProjectForm()
    template = loader.get_template('tandem/project.html')
    context = RequestContext(request,{'form':form})
    return HttpResponse(template.render(context))
  #  return render(request, 'tandem/project.html', context)

def analyze(request):
    analyzevariable = build_the_corpus()
    if analyzevariable[0] == -1:
        build = "failed"
        context = {"build": build}
        return render(request, 'tandem/analyze.html', context)
    context = {'analyzevariable': analyzevariable}
    return render(request, 'tandem/analyze.html', context)

def results(request):
    inputhome, corpushome, resultshome = startup.get_paths()
    calculate.mainout(corpushome, resultshome)
    resultsvariable = [ f for f in os.listdir(resultshome) if os.path.isfile(os.path.join(resultshome,f)) ]

    context = {'resultsvariable': resultsvariable}
    return render(request, 'tandem/results.html', context)

def download(request):
    global ziphome, pname
    inputhome, corpushome, resultshome = startup.get_paths()
    resultsfolder = resultshome
    #try:
    response = make_zip(resultsfolder,ziphome)
    print 'zip ok'

    response['Content-Disposition']= 'attachment;filename=%s.zip' %('tandem')
    response['Content-Type']= 'application/zip'
    return response




'''
    tmpdir = tempfile.mkdtemp()
    try:
        tmparchive = os.path.join(tmpdir, "tandemzip")
        root_dir = ziphome
        data = open(shutil.make_archive(tmparchive, 'zip', root_dir), 'rb').read()
        print type(data)
        print len(data)
    finally:
        shutil.rmtree(tmpdir)

    #shutil.make_archive(ziphome + '/tandem' + pname, 'zip', resultsfolder)
    #filepath = ziphome + "/tandem" + pname + ".zip"
    response = HttpResponse(data)
    response['Content-Dispostiosn'] = 'attachement; filename=yippeee'
    context = {'response':response}
    return render(request, 'tandem/results.html',context,
                  content_type = 'applications/zip')
    #return serve(request, os.path.basename(filepath), os.path.dirname(filepath))


    print "got here"
    downloadvar = "Success!"
    context = {'downloadvar': downloadvar}
    #return render(request, 'tandem/download.html', context)
    #return response
'''
def about(request):
  #  template = loader.get_template('tandem/about.html')
    aboutvariable = "about"
    context = {'aboutvariable': aboutvariable}
    return render(request, 'tandem/about.html', context)

def documentation(request):
    docvar = "doc"
    context = {'docvar': docvar}
    return render(request, 'tandem/documentation.html', context)

def terms(request):
    termsvar ='terms'
    context = {'termsvar':termsvar}
    return render(request, 'tandem/terms.html', context)

def team(request):
    teamvar = "team"
    context = {'teamvar':teamvar}
    return render(request, 'tandem/team.html', context)

def sample(request):
    samplevar = "sample"
    context = {'samplevar':samplevar}
    return render(request, 'tandem/sample.html', context)