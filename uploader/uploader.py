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
	if request.is_ajax() and request.FILES:
		uploads = request.FILES.getlist('uploads') # this is a MultiValueDict 
		for f in uploads:
			print('Saving file: '+f.name)
			pdf = PDFFile()
			pdf.save()
			pdf.f = File(f)
			pdf.title = f.name
			pdf.save()
			
			task = process.delay(pdf, client_pk, job_pk, item_pk, SEPS=True)
			data = 'Tasks started...'
	else:
		data = 'No file list in AJAX request.'
		
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def queue_poll(request):
	task_list = []
	if request.is_ajax():
		# Query active tasks:
		active_tasks = inspect().active() or inspect().scheduled()
		print active_tasks
		for t in active_tasks['celery@pc-PC']: # TODO: get queue name dynamically.
			task_id = t.get('id')
			task = AsyncResult(task_id)
			
			# Associate ID to task_state so the client end of the polling
			# mechanism can identify task one by one, like this:
			# [{task_stateN('task_idN')}]
			state = task.result or task.state
			if active_tasks:
				state.update({'id': task_id})
			task_list.append(state)
		print 'TASK_LIST'
		print task_list
	else:
		task_list = 'Not an AJAXed task list.'
			
	json_data = json.dumps(task_list, ensure_ascii=False, encoding='utf-8')
	print '\nJSON_DATA'
	print json_data
	print '\n'
	return HttpResponse(json_data, content_type='application/json')

	