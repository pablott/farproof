import subprocess
from django.shortcuts import render_to_response # Add get_object_or_404
from farproof.client_list.models import Client, Job, Item, Page
from farproof.client_list.models import UploadFileForm

from farproof.process.process import *


PATH = "D:/tmp/"


def file_upload(request, client_pk, job_pk, item_pk, page_num):
	client = Client.objects.get(pk=client_pk)
	job = Job.objects.get(pk=job_pk, client=client)
	item = Item.objects.get(pk=item_pk, job=job)
	page = Page.objects.get(number=page_num, item=item)

	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			message = "file sent"
			write_file(request.FILES['uploads'])
	else:
		message = "upload something"
		form = UploadFileForm()
	return render_to_response('file_upload.html', {
		'client': client,
		'job': job, 
		'item': item,
		'page': page,
		'form': form,
		'message': message,
	})

def write_file(f):
	with open(PATH + 'upload.pdf', 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	handle_uploaded_file(300)
			
			