from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import RequestContext, loader

#class Inputfolder(CreateView):
#   model =
#    template_name = getfolder.html

#   def get_success_url(self):
#       return reverse('index')

def index(request):
    tempvariable = "this is cool"
    template = loader.get_template('tandem/index.html')
    context = {'tempvariable': tempvariable}
    return render(request, 'tandem/index.html', context)

def getinput(request):
    inputvariable = "What file do you want to upload"
    template = loader.get_template('tandem/getinput.html')
    context = {'inputvariable': inputvariable}
    return render(request, 'tandem/getinput.html', context)

def analyze(request):
    p = 'filename'
    context = p
    return render(request, 'tandem/analyze.html', context)
    #return HttpResponse("You're on the tandem analyze page")

def results(request):
    return HttpResponse("You're on the tandem results page")

