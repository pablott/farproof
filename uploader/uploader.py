import os, subprocess
from django.core.files import File
from django.shortcuts import render_to_response # Add get_object_or_404
from farproof.client_list.models import Client, Job, Item, Page, Revision, PDFFile
from farproof.process.process import process


# TODO: JSON and MD5 client-side checksum verified by server-side checksum

# This first function gets files from POST 
# and writes them using the write_file() function below
from django.utils import simplejson
from django.template.loader import render_to_string
from django.template import RequestContext
from farproof.client_list.ajax import sayhello

def file_upload(request, client_pk, job_pk, item_pk):
	client = Client.objects.get(pk=client_pk)
	job = Job.objects.get(pk=job_pk, client=client)
	item = Item.objects.get(pk=item_pk, job=job)

	if request.method == 'POST':
		upload_list = request.FILES.getlist('uploads') # this is a MultiValueDict 
		write_file(upload_list, client, job, item)
		
		# message = "Uploaded files: "
		# total_size = 0
		# for file in upload_list:
		# http://stackoverflow.com/questions/117250/how-do-i-get-a-decimal-value-when-using-the-division-operator-in-python
			# message = message + file.name +" - "+ file.content_type +" - "+ str(round(file.size/1048576.0, 2))+"MB"
			# total_size = total_size + file.size
		# message = message +" / "+ str(total_size/1048576.0) + "MB"
	else:
		upload_list = "empty"
		message = "upload something"
	
	return render_to_response('file_upload.html', {
		'client': client,
		'job': job,
		'item': item,
		'upload_list': upload_list,
		# 'message': message,
	})

def write_file(upload_list, client, job, item):
	for f in upload_list:
		print('Saving file: '+f.name)
		pdf = PDFFile()
		pdf.save()
		pdf.f = File(f)
		pdf.save()
		
		process.delay(150, pdf, client, job, item, SEPS=False)
		