#from django.template import Context, loader

from django.shortcuts import render_to_response # Add get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from farproof.client_list.models import Client, Job, Item, Page, Revision, Comment
from farproof.client_list.models import ClientAddForm, JobAddForm, ItemAddForm
#from django.template import RequestContext
#def serve(request, path, document_root, show_indexes=False)

import subprocess


def main(request):
	clients = Client.objects.filter(active=True).order_by('name') #TODO: make it case insensitive
	clients_unactive = Client.objects.filter(active=False).order_by('name')
	return render_to_response('main.html', {
		'clients': clients,
		'clients_unactive': clients_unactive,
	})

	
def client_add(request):
	if request.method == 'POST': # If the form has been submitted...
		form = ClientAddForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			# Process the data in form.cleaned_data
			form.save()
			message = 'You added Client: %r' % str(request.POST['name']) #+ ' - %r' % str(request.POST['email'])
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
	query_unactive = 0
	if request.method == 'GET': # If this view gets a search query...
		if 'name' in request.GET: # Check if a 'name' was given
			name = request.GET['name']
			query = Client.objects.filter(name__icontains=name, active=True)
			query_unactive = Client.objects.filter(name__icontains=name, active=False)
			message = 'You searched for: %r' % str(name) 
		else:
			message = 'You submitted an empty form.'
		return render_to_response('client_search.html', {'message': message, 'query': query, 'query_unactive': query_unactive})
	else: # If not, show empty form
		return render_to_response('client_search.html', {'query': query, 'query_unactive': query_unactive})

		
def client_view(request, client_pk):
	client = Client.objects.get(pk=client_pk)
	#Check if client exists and show it:
	if client:
		jobs = Job.objects.filter(client=client, active=True).order_by('name')
		jobs_unactive = Job.objects.filter(client=client, active=False).order_by('name')
		return render_to_response('client_view.html', {
			'client': client,
			'jobs': jobs,
			'jobs_unactive': jobs_unactive,
		})
	else:
		raise Http404
		
		
def job_add(request, client_pk):
	client = Client.objects.get(pk=client_pk)
	message = ''
	if client:
		if request.method == 'POST':
			post = request.POST.copy()
			post['job-client'] = client.pk
			form_job = JobAddForm(post, instance=Job(), prefix="job")
			form_item = ItemAddForm(post, instance=Item(), prefix="item")
			if form_job.is_valid():
				last_job = form_job.save()
				post['item-job'] = last_job.pk
				if form_item.is_valid():
					form_item.save()
					message = 'You added Job: %r'%str(request.POST['job-name'])+' - %r'%str(request.POST['job-desc'])+', Item%r'%str(request.POST['item-name'])+' - %r'%str(request.POST['item-desc'])
			return render_to_response('job_add.html',
				{'form_job': form_job, 'form_item': form_item, 'message': message, 'client': client,})
		else:
			# First time called: unbound forms
			form_job = JobAddForm(prefix="job") 
			form_item = ItemAddForm(prefix="item")
		return render_to_response('job_add.html', {
			'form_job': form_job,
			'form_item': form_item,
			'client': client,
		})
	else:
		raise Http404		
		
		
def job_search(request, client_pk):
	client = Client.objects.get(pk=client_pk)
	if client:
		query = 0 # Initialize
		query_unactive = 0
		if request.method == 'GET': # If this view gets a search query...
			if 'name' in request.GET: # Check if a 'name' was given
				name = request.GET['name']
				# Checks if it exists and put it in 'query':
				query = Job.objects.filter(name__icontains=name, client=client, active=True).order_by('name') 
				query_unactive = Job.objects.filter(name__icontains=name, client=client, active=False).order_by('name')
				message = 'You searched for: %r' % str(name) 
			else:
				message = 'You submitted an empty form.'
			return render_to_response('job_search.html', {
				'client': client,
				'message': message,
				'query': query,
				'query_unactive': query_unactive,
			})
		else: # If not, show empty form
			return render_to_response('job_search.html', {'client': client,})
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
	
	
def item_add(request, client_pk, job_pk):
	client = Client.objects.get(pk=client_pk)
	job = Job.objects.get(pk=job_pk, client=client) # Check if Job exists
	if job:
		if request.method == 'POST': 
			post = request.POST.copy() 
			num_pages = int(post['num_pages'])
			start_page = int(post['start_page'])
			post['job'] = job.pk
			form = ItemAddForm(post)
			if form.is_valid(): 
				# Save Item
				last_item = form.save() 
				# Create all the neccesary pages:
				for i in range(start_page, start_page+num_pages):
					page = Page(number=(i), item=last_item)
					page.save()
				# Add a initial PENDING Revision to each new page:
				last_pages = Page.objects.filter(item=last_item)
				for page in last_pages:
					revision = Revision(rev_number=0, page=page)
					revision.save()
				message = 'You added Item: %r' % str(request.POST['name']) + ' - %r' % str(request.POST['desc']) + ' - %r' % str(request.POST['num_pages'])
				return render_to_response('item_add.html',
					{'form': form, 'message': message, 'client': client, 'job': job,})
		else:
			form = ItemAddForm()
		return render_to_response('item_add.html', {
			'form': form,
			'client': client,
			'job': job,
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
	revisions = Revision.objects.all().order_by('-pk')
	pages = Page.objects.filter(item=item).order_by('number')
	if pages:
		first_page = pages[0]
	else:
		first_page = 0 # Initialize variable in case 'pages' doesn't exist or it crashes (has to be an int)
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


# Gets page.number and decides how to fill odd and even pages.
# Uses inclusion_tags in the template. These get a page_even or page_odd
# and get all the information from the database.
def page_view(request, client_pk, job_pk, item_pk, page_num):
	client = Client.objects.get(pk=client_pk)
	job = Job.objects.get(pk=job_pk, client=client)
	item = Item.objects.get(pk=item_pk, job=job)
	page = Page.objects.get(number=page_num, item=item)
	pages = Page.objects.filter(item=item).order_by('number')
	# Order by inverted creation date and get first (which is the last created for that page):
	revisions = Revision.objects.filter(page=page).order_by('-creation') 
	
	# Get first and last pages of query
	# last_page counts one form end of query (this is because django doesn't support negative indexing)
	first_page = pages[0]
	last_page = pages[pages.count()-1] 
		
	# Logic for even pages:
	if page.number%2==0:
		# Logic for LAST even page
		# (because it has to initialize page_odd or it crashes):
		if page == last_page:
			page_even = page
			page_odd = 0
		# Otherwise page is assigned to even and the odd is calculated by adding 1 to page.number
		else:
			page_even = page
			page_odd = Page.objects.get(number=page.number+1, item=item)
	# Logic for odd pages:
	else:
		# Logic for odd page ONLY if it is the first
		# (because it has to initialize page_even or it crashes):
		if page == first_page:
			page_odd = page
			page_even = 0
		# Otherwise page is assigned to odd and the even is calculated by substracting 1 to page.number
		else:
			page_odd = page
			page_even = Page.objects.get(number=page.number-1, item=item)

	if page:
		return render_to_response('page_view.html', {
			'client': client,
			'job': job, 
			'item': item,
			'page': page,
			'pages': pages,
			'page_even': page_even,
			'page_odd': page_odd,
			'first_page': first_page,
			'last_page': last_page,
			'revisions': revisions,
		})
	else:
		raise Http404
		
		
def page_info(request, client_pk, job_pk, item_pk, page_num):
	client = Client.objects.get(pk=client_pk)
	job = Job.objects.get(pk=job_pk, client=client)
	item = Item.objects.get(pk=item_pk, job=job)
	page = Page.objects.get(number=page_num, item=item)
	# Order by inverted creation date and get first (which is the last created for that page):
	revisions = Revision.objects.filter(page=page).order_by('-creation') 
	if page:
		return render_to_response('page_info.html', {
			'client': client,
			'job': job, 
			'item': item,
			'page': page,
			'revisions': revisions,
		})
	else:
		raise Http404
	
	
