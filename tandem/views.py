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


from .forms import MyUploadForm, ProjectForm

import buildcorpus, calculate
from TandemDH import settings
from tandem.models import Project
inputhome = ''
corpushome = ''
resultshome = ''
pname = ''
ziphome = settings.MEDIA_ROOT

def start_project():
    global inputhome, corpushome, resultshome
    mytime = time.strftime("%j:%H:%M:%S")
    timestamp = mytime.replace(":","")
    print "setting time"
    outstorage = FileSystemStorage()
    inputhome = outstorage.location + '/tandemin/' + timestamp
    corpushome = outstorage.location + '/tandemcorpus/' + timestamp
    resultshome = outstorage.location + '/tandemout/' + timestamp


def handle_uploaded_file(f):
    global inputhome
    inputpath = inputhome
    if os.path.exists(inputpath):
        pass
    else:
        os.mkdir(inputpath)
    fullname = inputpath + '/' + str(f.name)
    with open(fullname, 'wb+') as destination:
        for chunk in f.chunks():
                destination.write(chunk)

def build_the_corpus():
    global timestamp, inputhome, corpushome, resultshome
    processlist = buildcorpus.analysis_setup(inputhome, corpushome, resultshome)
    return processlist

def zipoutput(path, zip):
    for root, dirs, files in os.walk(path):
        print root
        for file in files:
            print "zipping"
            zip.write(os.path.join(root, file))

def upload(request):
    if request.method == 'POST':
        print "upload form method=POST"
        form = MyUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print "Form is valid"
            for f in request.FILES.getlist('attachments'):
                print "handling"
                handle_uploaded_file(f)
            return HttpResponseRedirect('analyze')
    else:
        print "fresh"
        form = MyUploadForm()
    template = loader.get_template('tandem/upload.html')
    context = RequestContext(request,{'form':form})
    return HttpResponse(template.render(context))

def index(request):
    tempvariable = "Press Go to Begin"
    context = {'tempvariable': tempvariable}
    return render(request, 'tandem/index.html', context)

def project(request):
    global inputhome, corpushome, resultshome, pname
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
        start_project()
        print "fresh form...start"
        form = ProjectForm()
    template = loader.get_template('tandem/project.html')
    context = RequestContext(request,{'form':form})
    return HttpResponse(template.render(context))
  #  return render(request, 'tandem/project.html', context)

def analyze(request):
    analyzevariable = build_the_corpus()
    context = {'analyzevariable': analyzevariable}
    return render(request, 'tandem/analyze.html', context)

def results(request):
    global corpushome, resultshome
    calculate.mainout(corpushome, resultshome)
    resultsvariable = [ f for f in os.listdir(resultshome) if os.path.isfile(os.path.join(resultshome,f)) ]

    context = {'resultsvariable': resultsvariable}
    return render(request, 'tandem/results.html', context)

def download(request):
    global resultshome, ziphome, pname
    resultsfolder = resultshome
  #  tandemout = zipfile.ZipFile("/Users/sbr/data/tandem.zip", 'w', zipfile.ZIP_DEFLATED)
  #  zipoutput(resultsfolder, tandemout)
  #  tandemout.close()

    shutil.make_archive(ziphome + '/tandem' + pname, 'zip', resultsfolder)
    filepath = ziphome + "/tandem" + pname + ".zip"
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))


    print "got here"
    downloadvar = "Success!"
    context = {'downloadvar': downloadvar}
    return render(request, 'tandem/download.html', context)
    #return response

def about(request):
  #  template = loader.get_template('tandem/about.html')
    aboutvariable = "about"
    context = {'aboutvariable': aboutvariable}
    return render(request, 'tandem/about.html', context)

def documentation(request):
    template = loader.get_template('documentation.html')
   # context = RequestContext
    return HttpResponse(template.render())

def terms(request):
    template = loader.get_template('terms.html')
    context = RequestContext
    return HttpResponse(template.render(context))

def team(request):
    template = loader.get_template('team.html')
    context = RequestContext
    return HttpResponse(template.render(context))

def sample(request):
    template = loader.get_template('sample.html')
    context = RequestContext
    return HttpResponse(template.render(context))