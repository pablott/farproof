# Create your views here.
#from django.template import Context, loader
#from django.http import HttpResponse

from django.shortcuts import render_to_response # Add get_object_or_404
from farproof.client_list.models import Client, Job, Item, Page

#def serve(request, path, document_root, show_indexes=False)

def main(request):
	clients = Client.objects.all().order_by('name') #TODO: make it case insensitive
	return render_to_response('main.html', {'clients': clients})

def client_view(request, client):
	jobs = Job.objects.filter(client__name__exact=client).order_by('name')
	return render_to_response('client_view.html', {
		'client_name': client, 
		'jobs': jobs,
	})
	
def job_view(request, client, job):
	items = Item.objects.filter(job__name__exact=job).order_by('name')
	return render_to_response('job_view.html', {
		'client_name': client,
		'job_name': job, 
		'items': items
	})
	
def item_view_list(request, client, job, item):
	pages = Page.objects.filter(item__name__exact=item).order_by('number')
	return render_to_response('item_view_list.html', {
		'client_name': client,
		'job_name': job, 
		'item_name': item,
		'pages': pages
	})

def item_view_thumbs(request, client, job, item):
	pages = Page.objects.filter(item__name__exact=item).order_by('number')
	first_page = pages[0]
	#first_page = pages[0]
	#if first_page == 1:
	#	first_page = 'odd'
	#else:
	#	first_page = 'even'
	
	
	
	return render_to_response('item_view_thumbs.html', {
		'client_name': client,
		'job_name': job, 
		'item_name': item,
		'pages': pages,
		'first_page': first_page
	})	
	
def page_view(request, client, job, item, page):
	return render_to_response('page_view.html', {
		'client_name': client,
		'job_name': job, 
		'item_name': item,
		'page_num': page
	})
	
	