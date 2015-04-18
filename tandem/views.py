from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render_to_response
from .forms import UploadFileForm
from django.core.files import File
from django.core.files.uploadhandler import load_handler
from django.core.files.uploadedfile import UploadedFile
from django.core.files.images import ImageFile
upfile = ''

# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file
def handle_uploaded_file(f):
    global upfile
    print "upload type=", type(f)
    upfile = f.name
    mystorage = FileSystemStorage()
    path = mystorage.location
    fullname = path + '/' + str(upfile)

    with open(fullname, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload(request):
    if request.method == 'POST':
        print "post"
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('analyze')
        #    return HttpResponseRedirect(reverse('tandem.views.upload'))
    else:
        print "not post"
        form = UploadFileForm()
    template = loader.get_template('tandem/upload.html')
    context = RequestContext(request,{'form':form})
    return HttpResponse(template.render(context))

def index(request):
    tempvariable = "Press Go to Begin"
    context = {'tempvariable': tempvariable}
    return render(request, 'tandem/index.html', context)

def analyze(request):
    global upfile
    analyzevariable = upfile
    context = {'analyzevariable': analyzevariable}
    return render(request, 'tandem/analyze.html', context)

def results(request):
    return HttpResponse("You're on the tandem results page")

