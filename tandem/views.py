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
#from tandem import startup

pname = ''
ziphome = settings.MEDIA_ROOT
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
    return inputhome, corpushome, resultshome

def run():
    inpath, corpath, outpath = start_project()
    print "making input folder"
    make_input_folder(inpath)

    print "making corpus folder"
    make_corpus_folder(corpath)

    print "making results folder"
    make_results_folder(outpath)
    return inpath, corpath, outpath

def make_input_folder(inputpath):
    if os.path.exists(inputpath):
        print "inputpath exists=", inputpath
        pass
    else:
        print "making inputpath=", inputpath
        os.umask(0000)
        os.mkdir(inputpath)

def make_corpus_folder(corpuspath):
    if os.path.exists(corpuspath):
        print "corpuspath exists=", corpuspath
        pass
    else:
        print "making corpuspath=", corpuspath
        os.umask(0000)
        os.mkdir(corpuspath)

def make_results_folder(resultspath):
    if os.path.exists(resultspath):
        print "resultspath exists=", resultspath
        pass
    else:
        print "making resultspath=", resultspath
        os.umask
        os.mkdir(resultspath)

def handle_uploaded_file(f, request):
    status = 'ok'
    project_key = request.session['key']
    project = Project.objects.get(pk = project_key)
    inputhome = project.input_folder
    if inputhome != '':
        print inputhome, "uploading"
        fullname = inputhome + '/' + str(f.name)
        with open(fullname, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    else:
        print "inputhome=", inputhome
        status = "upload failure"
    return status

def build_the_corpus(request):
    project_key = request.session['key']
    project = Project.objects.get(pk = project_key)
    inputhome = project.input_folder
    corpushome = project.text_folder
    resultshome = project.dest_folder
    global inputhome, corpushome, resultshome
    processlist = buildcorpus.analysis_setup(inputhome, corpushome, resultshome)
    return processlist

def make_zip(path):
    zipdata = StringIO()
    zipf = zipfile.ZipFile(zipdata, 'w',)
   # info = zipfile.ZipInfo(zipf)
   # info.external_attr = 0777 << 16L
    for root, dirs, files in os.walk(path):
        print "zip folder", root
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close
    os.chmod(zipf, 0777)
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
        print "session", request.session
        form = MyUploadForm(request.POST, request.FILES)
        if form.is_valid():
            for f in request.FILES.getlist('attachments'):
                upload_status = handle_uploaded_file(f, request)
            if upload_status == 'ok':
                print "upload ok"
                return HttpResponseRedirect('analyze')
    else:
        form = MyUploadForm()
    if upload_status <> 'ok':
        print "upload status=", upload_status
    template = loader.get_template('tandem/upload.html')
    context = RequestContext(request,{'form':form})
    print request.session['proj'], request.session['key']
    return HttpResponse(template.render(context))

def index(request):
    tempvariable = "render index html"
    print tempvariable
    context = {'tempvariable': tempvariable}
    return render(request, 'tandem/index.html', context)

def project(request):
    indir, corpdir, resultdir = run()
    p = Project()
    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            print "form is valid"
            new_project = form.save(commit=False)
            new_project.input_folder = indir
            new_project.text_folder = corpdir
            new_project.dest_folder = resultdir
            new_project.save()
            print new_project.pk
            request.session['proj'] = new_project.project_name
            request.session['key'] = new_project.pk
            context = {'new_project':new_project}
            return HttpResponseRedirect('upload')
         #  return render(request,'tandem/upload.html',context)
        else:
            print "form is not valid"
            error = "Looks like you forgot something!"
            context = RequestContext(request,{'error':error})
            template = loader.get_template('tandem/project.html')
            return HttpResponse(template.render(context))
    else:
        print "fresh form...start"
        form = ProjectForm()
    template = loader.get_template('tandem/project.html')
    context = RequestContext(request,{'form':form})
    return HttpResponse(template.render(context))

def analyze(request):
    analyzevariable = build_the_corpus(request)
    if analyzevariable[0] == -1:
        build = "failed"
        context = {"build": build}
        return render(request, 'tandem/analyze.html', context)
    context = {'analyzevariable': analyzevariable}
    return render(request, 'tandem/analyze.html', context)

def results(request):
    project_key = request.session['key']
    project = Project.objects.get(pk = project_key)
    corpushome = project.text_folder
    resultshome = project.dest_folder
    calculate.mainout(corpushome, resultshome)
    resultsvariable = [ f for f in os.listdir(resultshome) if os.path.isfile(os.path.join(resultshome,f)) ]

    context = {'resultsvariable': resultsvariable}
    return render(request, 'tandem/results.html', context)

def download(request):
    global ziphome
    project_key = request.session['key']
    project = Project.objects.get(pk = project_key)
    resultshome = project.dest_folder

    shutil.make_archive(ziphome + '/tandem' + pname, 'zip', resultshome)
    filepath = ziphome + "/tandem" + pname + ".zip"
    print "creating zip at", filepath
    print "zipping files at ", resultshome
    response = HttpResponse()
    response['Content-Dispostiosn'] = 'attachement; filename=yippeee'
    context = {'response':response}
   # return render(request, 'tandem/results.html',context,
   #               content_type = 'applications/zip')
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
def about(request):
  #  template = loader.get_template('tandem/about.html')
    aboutvariable = "about"
    context = {'aboutvariable': aboutvariable}
    return render(request, 'tandem/about.html', context)

def documentation(request):
    docvar = "doc"
    context = {'docvar': docvar}
    return render(request, 'tandem/documentation.html', context)

def prepare(request):
    print "render prepare"
    prepvar = "prep"
    context = {'prepvar': prepvar}
    return render(request, 'tandem/prepare.html', context)

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

def datacheck(request):
    print request.GET
    if 'results' in request.GET:
        filepath = settings.MEDIA_ROOT + "sample/tandemout.zip"
    else:
        filepath = settings.MEDIA_ROOT + "sample/tandemin.zip"
    print "returning ", filepath
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))