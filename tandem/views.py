from django.shortcuts import get_object_or_404, render
#from django.views.generic import CreateView
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, QueryDict, HttpRequest
from django.template import RequestContext, loader
from django.core.files.storage import FileSystemStorage
#from django.shortcuts import render_to_response
import time
import os

from .forms import MyUploadForm, ProjectForm
from django.core.files import File
from django.core.files.uploadhandler import load_handler
from django.core.files.uploadedfile import UploadedFile
import buildcorpus
import calculate
from tandem.models import Project

time = time.strftime("%j:%H:%M:%S")
timestamp = time.replace(":","")
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

def upload(request):
    if request.method == 'POST':
        form = MyUploadForm(request.POST, request.FILES)
        if form.is_valid():
            for f in request.FILES.getlist('attachments'):
                handle_uploaded_file(f)
            return HttpResponseRedirect('analyze')
    else:
        form = MyUploadForm()
    template = loader.get_template('tandem/upload.html')
    context = RequestContext(request,{'form':form})
    return HttpResponse(template.render(context))

def index(request):
    tempvariable = "Press Go to Begin"
    context = {'tempvariable': tempvariable}
    return render(request, 'tandem/index.html', context)

def project(request):
    global inputhome, corpushome, resultshome
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
        return HttpResponseRedirect('tandem/upload')
    else:
        form = ProjectForm()
    template = loader.get_template('tandem/project.html')
    context = RequestContext(request,{'form':form})
    return HttpResponse(template.render(context))

def analyze(request):
    analyzevariable = "this will be the filename"
    analyzevariable = build_the_corpus()
    context = {'analyzevariable': analyzevariable}
    return render(request, 'tandem/analyze.html', context)

def results(request):
    global corpushome, resultshome
    calculate.mainout(corpushome, resultshome)
    resultsvariable = [ f for f in os.listdir(resultshome) if os.path.isfile(os.path.join(resultshome,f)) ]
    context = {'resultsvariable': resultsvariable}
    return render(request, 'tandem/results.html', context)

