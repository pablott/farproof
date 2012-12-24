#from django.template import Context, loader

from django.shortcuts import render_to_response # Add get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from farproof.client_list.models import Client, Job, Item, Page, Revision, Comment
from farproof.client_list.models import ClientAddForm, JobAddForm, ItemAddForm
#from django.template import RequestContext
#def serve(request, path, document_root, show_indexes=False)

def main(request):
	clients = Client.objects.all().order_by('name') #TODO: make it case insensitive
	return render_to_response('main.html', {'clients': clients})

def client_add(request):
	if request.method == 'POST': # If the form has been submitted...
		form = ClientAddForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			# Process the data in form.cleaned_data
			form.save()
			message = 'You added Client: %r' % str(request.POST['name']) + ' - %r' % str(request.POST['email'])
			form = ClientAddForm() # Reset form after saving
			return render_to_response('client_add.html',
				{'form': form, 'message': message})
	else:
		form = ClientAddForm() # An unbound form
	return render_to_response('client_add.html', {
		'form': form,
	})

def client_search(request): # TODO Consider using a ClientSearchForm or such
	query = 0 # Initialize
	if request.method == 'GET': # If this view gets a search query...
		if 'name' in request.GET: # Check if a 'name' was given
			name = request.GET['name']
			query = Client.objects.filter(name__icontains=name) # Checks if it exists
			message = 'You searched for: %r' % str(name) 
		else:
			message = 'You submitted an empty form.'
		return render_to_response('client_search.html', {'message': message, 'query': query})
	else: # If not, show empty form
		return render_to_response('client_search.html', {'query': query})

def client_view(request, client_pk):
	client = Client.objects.get(pk=client_pk)
	#Check if client exists and show it:
	if client:
		jobs = Job.objects.filter(client=client).order_by('name')
		return render_to_response('client_view.html', {
			'client': client,
			'jobs': jobs,
		})
	else:
		raise Http404
	
	
def job_add_old(request, client):
	check_path = Client.objects.filter(name__exact=client)
	if check_path:
		client_id = Client.objects.get(name__exact=client).id
		if request.method == 'POST': # Form's been submitted
			post = request.POST.copy() # Make POST mutable, see: http://stackoverflow.com/questions/7572537/modifying-django-model-forms-after-post?rq=1
			post['client'] = client_id # Modify POST data to reflect client's name
			form = JobAddForm(post) # A form bound to the POST data
			if form.is_valid(): # Validate resulting form
				form.save() # Save form.cleaned_data to DB and inform user
				message = 'You added Job: %r' % str(request.POST['name']) + ' - %r' % str(request.POST['desc'])
				form = JobAddForm() # Reset form after saving
				return render_to_response('job_add.html',
					{'form': form, 'message': message, 'client_name': client,})
		else:
			# First time called: an unbound form
			form = JobAddForm() 
		return render_to_response('job_add_old.html', {
			'form': form,
			'client_name': client,
		})
	else:
		raise Http404
		
		
		# HACER CAMBIOS SOBRE POST:
		# Cambiar Client, despues Job (asociado a Client)
		
		
def job_add(request, client):
	check_path = Client.objects.filter(name__exact=client)
	if check_path:
		client_id = Client.objects.get(name__exact=client).id
		if request.method == 'POST':
			post = request.POST.copy()
			post['client'] = client_id
			#form = JobAddForm(post)
			
			
			form_job = JobAddForm(post, instance=Job())
			form_item = ItemAddForm(request.POST, instance=Item())
			job_name = form_job['name']
			if form_job.is_valid():
				form_job.save()
				
				job_id = form_job['id']
				
				# = Item(number=(i+1),job=job)
				
				#job_id = Item.objects.get(name__exact=item_name, job__name__exact=job, job__client__name__exact=client).id 
				
			message = 'You added Job: %r' % str(request.POST['name']) + ' - %r' % str(request.POST['desc'])	
			#form_job = JobAddForm(post, instance=Job())
			#form_item = ItemAddForm(request.POST, instance=Item())



			#form_job_copy = form_job.copy() # Make POST mutable, see: http://stackoverflow.com/questions/7572537/modifying-django-model-forms-after-post?rq=1
			#form_job['desc'] = client_id # Modify POST data to reflect client's name
			#form = JobAddForm(form_job) # A form bound to the POST data
			return render_to_response('new_job_add.html',
				{'form_job': form_job, 'form_item': form_item, 'message': message, 'client_name': client,})
		else:
			# First time called: an unbound form
			form_job = JobAddForm() 
			form_item = ItemAddForm()
		return render_to_response('job_add.html', {
			'form_job': form_job,
			'form_item': form_item,
			'client_name': client,
		})
	else:
		raise Http404		
		
		
		
		
		
		
def job_search(request, client):
	check_path = Client.objects.filter(name__exact=client)
	if check_path:
		query = 0 # Initialize
		if request.method == 'GET': # If this view gets a search query...
			if 'name' in request.GET: # Check if a 'name' was given
				name = request.GET['name']
				query = Job.objects.filter(name__icontains=name).order_by('name') # Checks if it exists and put it in 'query'
				message = 'You searched for: %r' % str(name) 
			else:
				message = 'You submitted an empty form.'
			return render_to_response('job_search.html', {'message': message, 'query': query, 'client_name': client,})
		else: # If not, show empty form
			return render_to_response('job_search.html', {'query': query, 'client_name': client,})
	else:
		raise Http404

		
		
def job_view(request, client_pk, job_pk):
	# Notice how it explicitly asks for current Item's Job AND for that Job's parent Client.
	# It does two things: 
	# 1) Avoids returning an Item which name is equal to another Item under a different Job and/or Client.
	# 2) Raises a 404 whenever the Client and/or Job names don't exists.
	client = Client.objects.get(pk=client_pk)
	job = Job.objects.get(pk=job_pk, client=client) # Check if Job exists
	items = Item.objects.filter(job=job).order_by('name') # Check if Items inside Job
	if job:
		return render_to_response('job_view.html', {
			'client': client,
			'job': job, 
			'items': items,
		})
	else:
		raise Http404
	
def item_add(request, client, job):
	check_path = Job.objects.filter(name__exact=job, client__name__exact=client)
	if check_path:
		if request.method == 'POST': 
			post = request.POST.copy() 
			job_id = Job.objects.get(name__exact=job, client__name__exact=client).id 
			num_pages = int(post['num_pages'])
			start_page = int(post['start_page'])
			item_name = post['name']
			post['job'] = job_id  
			form = ItemAddForm(post) 
			if form.is_valid(): 
				# Save form
				form.save() 
				item_id = Item.objects.get(name__exact=item_name, job__name__exact=job, job__client__name__exact=client).id 
				message = 'You added Item: %r' % str(request.POST['name']) + ' - %r' % str(request.POST['desc']) + ' - %r' % str(request.POST['num_pages']) + ' - %r' % str(item_id) # It takes ID of new item correctly
				form = ItemAddForm() 
				
				# Create all the neccesary pages:
				for i in range(start_page,start_page+num_pages):
					item = Item.objects.get(name__exact=item_name, job__name__exact=job, job__client__name__exact=client)
					pages = Page(number=(i), item=item)
					pages.save()
				return render_to_response('item_add.html',
					{'form': form, 'message': message, 'client_name': client, 'job_name': job,})
		else:
			form = ItemAddForm()
		return render_to_response('item_add.html', {
			'form': form,
			'client_name': client,
			'job_name': job,
		})
	else:
		raise Http404
	

def item_view_list(request, client_pk, job_pk, item_pk):
	client = Client.objects.get(pk=client_pk)
	job = Job.objects.get(pk=job_pk, client=client)
	item = Item.objects.get(pk=item_pk, job=job)
	pages = Page.objects.filter(item=item).order_by('number')
	if item:
		return render_to_response('item_view_list.html', {
			'client': client,
			'job': job, 
			'item': item,
			'pages': pages,
		})
	else:
		raise Http404

		
		
def item_view_thumbs(request, client_pk, job_pk, item_pk):
	client = Client.objects.get(pk=client_pk)
	job = Job.objects.get(pk=job_pk, client=client)
	item = Item.objects.get(pk=item_pk, job=job)
	pages = Page.objects.filter(item=item).order_by('number')
	if pages:
		first_page = pages[0]
	else:
		first_page = 0 # Initialize variable in case 'pages' doesn't exist or it crashes
	if item:
		return render_to_response('item_view_thumbs.html', {
			'client': client,
			'job': job, 
			'item': item,
			'pages': pages,
			'first_page': first_page,
		})
	else:
		raise Http404

	
def page_view(request, client, job, item, page):
	check_path = Page.objects.filter(number__exact=page, item__name__exact=item, item__job__name__exact=job, item__job__client__name__exact=client)
	
	revision = Revision.objects.get(page__number__exact=page, page__item__name__exact=item, page__item__job__name__exact=job, page__item__job__client__name__exact=client)
	comment = Comment.objects.get(revision=revision, revision__page__number__exact=page, revision__page__item__name__exact=item, revision__page__item__job__name__exact=job, revision__page__item__job__client__name__exact=client).comment
	if check_path:
		return render_to_response('page_view.html', {
			'client_name': client,
			'job_name': job, 
			'item_name': item,
			'page_num': page,
			'revision': revision,
			'comment': comment,
		})
	else:
		raise Http404
	