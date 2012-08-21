from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.core.cache import cache
from django.utils import simplejson as simplejson

def home(request):
	return render_to_response('home/home.html',None)


def jobs(request):
	json = simplejson.dumps(cache.get('1'))
	return HttpResponse(json,content_type="application/json")