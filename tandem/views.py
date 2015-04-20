from django.shortcuts import get_object_or_404, render
#from django.views.generic import CreateView
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, QueryDict, HttpRequest
from django.template import RequestContext, loader
from django.core.files.storage import FileSystemStorage
#from django.shortcuts import render_to_response
#from .forms import UploadFileForm
from .forms import MyUploadForm
from django.core.files import File
from django.core.files.uploadhandler import load_handler
from django.core.files.uploadedfile import UploadedFile
from django.core.files.images import ImageFile


def handle_uploaded_file(f):
    print f.name
    mystorage = FileSystemStorage()
    path = mystorage.location
    fullname = path + '/' + str(f.name)

    with open(fullname, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload(request):
    if request.method == 'POST':
        form = MyUploadForm(request.POST, request.FILES)
        if form.is_valid():
            for f in request.FILES.getlist('attachments'):
                handle_uploaded_file(f)
            return HttpResponseRedirect('analyze')
        #    return HttpResponseRedirect(reverse('tandem.views.upload'))
    else:
        form = MyUploadForm()
    template = loader.get_template('tandem/upload.html')
    context = RequestContext(request,{'form':form})
    return HttpResponse(template.render(context))

def index(request):
    tempvariable = "Press Go to Begin"
    context = {'tempvariable': tempvariable}
    return render(request, 'tandem/index.html', context)

def analyze(request):
    analyzevariable = "this will be the filename"
    context = {'analyzevariable': analyzevariable}
    return render(request, 'tandem/analyze.html', context)

def results(request):
    return HttpResponse("You're on the tandem results page")

