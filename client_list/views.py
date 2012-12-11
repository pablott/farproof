#from django.template import Context, loader

from django.shortcuts import render_to_response # Add get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
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
			message = 'You added Client: %r' % str(request.POST['name']) + ' - %r' % str(request.POST['email'])
			form = ClientForm() # Reset form after saving
			return render_to_response('client_add.html',
				{'form': form, 'message': message})
	else:
		form = ClientForm() # An unbound form
	return render_to_response('client_add.html', {
		'form': form,
	})

def client_search(request): # TODO Consider using a ClientSearchForm or such
	query = 0 # Initialize
	if request.method == 'GET': # If this view gets a search query...
		if 'name' in request.GET: # Check if a 'name' was given
			name = request.GET['name']
			query = Client.objects.filter(name__icontains=name) # TODO Checks if it exists
			message = 'You searched for: %r' % str(name) 
		else:
			message = 'You submitted an empty form.'
		return render_to_response('client_search.html', {'message': message, 'query': query})
	else: # If not, show empty form
		return render_to_response('client_search.html', {'query': query})

def client_view(request, client):
	jobs = Job.objects.filter(client__name__exact=client).order_by('name')
	return render_to_response('client_view.html', {
		'client_name': client, 
		'jobs': jobs,
	})
	

	
	
def job_add(request, client):
	client_id = Client.objects.get(name__exact=client).id
	if request.method == 'POST': # Form's been submitted
		post = request.POST.copy() # Make POST mutable, see: http://stackoverflow.com/questions/7572537/modifying-django-model-forms-after-post?rq=1
		post['client'] = client_id # Modify POST data to reflect client's name
		form = JobForm(post) # A form bound to the POST data
		if form.is_valid(): # Validate resulting form
			form.save() # Save form.cleaned_data to DB and inform user
			message = 'You added Job: %r' % str(request.POST['name']) + ' - %r' % str(request.POST['desc'])
			form = JobForm() # Reset form after saving
			return render_to_response('job_add.html',
				{'form': form, 'message': message, 'client_name': client,})
	else:
		# First time called: an unbound form
		form = JobForm() 
	return render_to_response('job_add.html', {
		'form': form,
		'client_name': client,
	})
	
def job_search(request, client):
	query = 0 # Initialize
	if request.method == 'GET': # If this view gets a search query...
		if 'name' in request.GET: # Check if a 'name' was given
			name = request.GET['name']
			query = Job.objects.filter(name__icontains=name) # TODO Checks if it exists
			message = 'You searched for: %r' % str(name) 
		else:
			message = 'You submitted an empty form.'
		return render_to_response('job_search.html', {'message': message, 'query': query, 'client_name': client,})
	else: # If not, show empty form
		return render_to_response('job_search.html', {'query': query, 'client_name': client,})

		
		
def job_view(request, client, job):
	items = Item.objects.filter(job__name__exact=job, job__client__name__exact=client).order_by('name')
	#client_exists = Client.objects.filter(name__exact=client)
	# Check URL leads to a real item in DB.
	# Notice how it explicitely asks for Job and for its parent Client
	# this way is impossible to fullfill the condition in the case there are 
	# two Jobs or Clients with the same name.
	exists = Job.objects.filter(name__exact=job, client__name__exact=client)
	if exists: # Check if URL exists
		return render_to_response('job_view.html', {
			'client_name': client,
			'job_name': job, 
			'items': items,
		})
	else:
		raise Http404

	
	
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
	
	