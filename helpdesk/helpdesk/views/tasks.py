from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.core.cache import cache

from helpdesk.models import Ticket, Queue
from helpdesk.coordinate import Coordinate



def coordinatesync(request):
	c = Coordinate()
	for q in Queue.objects.all():
		if q.coordinate_id is not None:
			jobs = c.List(q.coordinate_id)
			cache.set('1',jobs['items'],3600)
	return HttpResponse('ok')