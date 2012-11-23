# Create your views here.
#from django.template import Context, loader
#from django.http import HttpResponse

from django.shortcuts import render_to_response # Add get_object_or_404
from farproof.client_list.models import Client, Job, Item


def client_index(request):
	client_list = Client.objects.all()
	#return HttpResponse( m )
	#t = loader.get_template('view/index.html')
	#c = Context({
	#	'client_list': client_list,
	#})
	#return HttpResponse(t.render(c))
	return render_to_response('client_list/client_list.html', {'client_list': client_list})

def client_contents(request, q_client_name):
	client_contents = Job.objects.all()
	#return HttpResponse( m )
	#t = loader.get_template('view/index.html')
	#c = Context({
	#	'client_list': client_list,
	#})
	#return HttpResponse(t.render(c))
	#if q_client_name = Client.client_name :
	item_contents = Item.objects.all()
	#client_contents = 0
	return render_to_response('client_contents/client_contents.html', {'client_contents': client_contents, 'client_name': q_client_name, 'item_contents': item_contents})
	

	
	
	
	
	