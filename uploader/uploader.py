import os, subprocess
import json
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render_to_response # Add get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from celery.result import AsyncResult
from farproof.client_list.models import PDFFile
from farproof.process.process import process

# TODO: MD5 client-side checksum verified by server-side checksum

	
@csrf_exempt
def uploader(request, client_pk, job_pk, item_pk):
	data = 'empty'
	if request.is_ajax():
		uploads = request.FILES.getlist('uploads') # this is a MultiValueDict 
		print(uploads)
		for f in uploads:
			print('Saving file: '+f.name)
			pdf = PDFFile()
			pdf.save()
			pdf.f = File(f)
			pdf.save()
			
			task = process.delay(32, pdf, client_pk, job_pk, item_pk, SEPS=False)
			request.session['task_id'] = task.id
			data = task.id
	else:
		data = 'Not file list in AJAX request.'
		
	json_data = json.dumps(data)

	return HttpResponse(json_data, mimetype='application/json')


@csrf_exempt
def queue_poll(request):
	data = 'empty'
	if request.is_ajax():
		if 'task_id' in request.POST.keys() and request.POST['task_id']:
			task_id = request.POST['task_id']
			# print(task_id)
			task = AsyncResult(task_id)
			data = task.result or task.state
		else:
			data = 'No task_id found.'
	else:
		data = 'Not an AJAX request.'

	json_data = json.dumps(data)

	return HttpResponse(json_data, mimetype='application/json')

	