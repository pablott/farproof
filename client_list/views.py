# Create your views here.
#from django.template import Context, loader
#from django.http import HttpResponse

from django.shortcuts import render_to_response # Add get_object_or_404
from farproof.client_list.models import Client, Job, Item


def client_index(request):
	client_list = Client.objects.all()
	return render_to_response('client_list/client_list.html', {'client_list': client_list})

def client_contents(request, client):
	# client_contents = Job.objects.all()
	jobs = Job.objects.filter(client__client_name__exact=client)
	item_contents = 8 # placeholder
	return render_to_response('client_contents/client_contents.html', {
		'client_name': client, 
		'jobs': jobs,
		'item_contents': item_contents
	})
	

def job_contents(request, job):
	# client_contents = Job.objects.all()
	items = Item.objects.filter(job__job_name__exact=job)
	item_contents = 8 # placeholder
	return render_to_response('job_contents/job_contents.html', {
		'job_name': job, 
		'item': items,
		'item_contents': item_contents
	})
	
	
	
	