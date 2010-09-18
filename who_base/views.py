# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext

def dashboard(request):
    return render_to_response('who_base/index.html',  {},
                              context_instance=RequestContext(request))
