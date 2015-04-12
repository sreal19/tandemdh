from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from .forms import ProjectForm
from tandem.models import Project
from tandem import engine

def index(request):
    tempvariable = "this is cool"
    template = loader.get_template('tandem/index.html')
    context = {'tempvariable': tempvariable}
    return render(request, 'tandem/index.html', context)

def getinput(request):
    inputvariable = "What file do you want to upload"
    template = loader.get_template('tandem/getinput.html')
    context = {'inputvariable': inputvariable}
    return render(request, 'tandem/getproject.html', context)

def analyze(request):
    p = 'filename'
    context = p
    return render(request, 'tandem/analyze.html', context)
    #return HttpResponse("You're on the tandem analyze page")

def results(request):
    return HttpResponse("You're on the tandem results page")

def runengine(request):
    engine.main()
    return HttpResponse("Tandem as completed processing your files!")

def getproject(request):
    #if this is a POST request we need to process the form data
    if request.method == 'POST':
        #create a form instance and populate it with data from the request:
        form = ProjectForm(request.POST)

        #check whether it is valid
        if form.is_valid():
            #process the data in form.cleaned.data as required
            new_project = form.save()   #create new record from form data
            #...
            #redirect to a new URL:
            return HttpResponseRedirect('/thanks/')
    #if GET (or any other method) we will create a blank form
    else:
        form = ProjectForm()
    return render(request, 'getproject.html', {'form':form})