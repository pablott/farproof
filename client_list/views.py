#from django.template import Context, loader

from django.shortcuts import render_to_response # Add get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from farproof.client_list.models import Client, Job, Item, Page
from farproof.client_list.models import ClientForm, JobForm, ItemForm
#from django.template import RequestContext
#def serve(request, path, document_root, show_indexes=False)

def main(request):
	clients = Client.objects.all().order_by('name') #TODO: make it case insensitive
	return render_to_response('main.html', {'clients': clients})

def client_add(request):
	if request.method == 'POST': # If the form has been submitted...
		form = ClientForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			# Process the data in form.cleaned_data
			form.save()
			added = 'You added %r' % request.POST['name'] + ' - %r' % request.POST['email']
			return render_to_response('client_add.html',
				{'form': form, 'added': added})
	else:
		form = ClientForm(
		initial={'desc': 'dd'}) # An unbound form

	return render_to_response('client_add.html', {
		'form': form,
	})




		
		
		
def client_search(request):
	return render_to_response('client_search.html', {
	})

def client_result(request):
	if 'name' in request.GET:
		message = 'You searched for: %r' % request.GET['name']
	else:
		message = 'You submitted an empty form.'
	return HttpResponse(message)
	

	
	
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
		'items': items,
	})

def job_add(request, client):
	if request.method == 'POST': # If the form has been submitted...
		form = JobForm(request.POST) # A form bound to the POST data
		 # Modify POST data to reflect client's name
		if form.is_valid(): # Validate resulting form
			# Save form.cleaned_data to DB and inform
			form.save()
			added = 'You added a Job'
			
			return render_to_response('job_add.html',
				{'form': form, 'added': added, 'client': client,})
	else:
		# An unbound form
		client_id = Client.objects.filter(name=client)
		form = JobForm() 

	return render_to_response('job_add.html', {
		'form': form,
		'client_name': client,
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
	
	