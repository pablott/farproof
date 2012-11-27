# Create your views here.
#from django.template import Context, loader
#from django.http import HttpResponse

from django.shortcuts import render_to_response # Add get_object_or_404
from farproof.client_list.models import Client, Job, Item, Page


def client_index(request):
	client_list = Client.objects.all()
	return render_to_response('client_list/client_list.html', {'client_list': client_list})

def client_contents(request, client):
	jobs = Job.objects.filter(client__name__exact=client)
	return render_to_response('client_contents/client_contents.html', {
		'client_name': client, 
		'jobs': jobs,
	})
	
def job_contents(request, client, job):
	items = Item.objects.filter(job__name__exact=job)
	return render_to_response('job_contents/job_contents.html', {
		'job_name': job, 
		'client_name': client,
		'items': items
	})
	
	
	
	