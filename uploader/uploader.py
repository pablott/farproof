import os, subprocess
import json
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render_to_response # Add get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from celery.result import AsyncResult
from celery.task.control import inspect
from farproof.client_list.models import PDFFile
from farproof.process.process import process

# TODO: MD5 client-side checksum verified by server-side checksum

	
@csrf_exempt
def uploader(request, client_pk, job_pk, item_pk):
	data = 'empty'
	if request.is_ajax():
		uploads = request.FILES.getlist('uploads') # this is a MultiValueDict 
		for f in uploads:
			print('Saving file: '+f.name)
			pdf = PDFFile()
			pdf.save()
			pdf.f = File(f)
			pdf.save()
			
			task = process.delay(32, pdf, client_pk, job_pk, item_pk, SEPS=True)
			request.session['task_id'] = task.id
			data = task.id
	else:
		data = 'No file list in AJAX request.'
		
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def queue_poll(request):
	task_list = []
	if request.is_ajax():
		# Query active tasks:
		active_tasks = inspect().active()
		for t in active_tasks['celery@pc-PC']: # TODO: get queue name dynamically.
			task_id = t.get('id')
			task = AsyncResult(task_id)
			
			# Associate UUID to task_state so the client end of the polling
			# mechanism can identify task one by one, like this:
			# [{task_id, task_state}]
			state = task.result or task.state
			state.update({'id': task_id})
			task_list.append(state)
		# print task_list
	else:
		task_list = 'Not an AJAXed task list.'
			
	json_data = json.dumps(task_list)
	print json_data
	return HttpResponse(json_data, content_type='application/json')		

	