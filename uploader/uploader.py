import os, subprocess
from django.shortcuts import render_to_response # Add get_object_or_404
from farproof.client_list.models import Client, Job, Item, Page, Revision
from farproof.process.process import process
from farproof.settings import CONTENTS_PATH


#TODO: JSON and MD5 client-side checksum verified by server-side checksum

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
		message = "Uploaded files: "
		total_size = 0
		for file in upload_list:
		# http://stackoverflow.com/questions/117250/how-do-i-get-a-decimal-value-when-using-the-division-operator-in-python
			message = message + file.name +" - "+ file.content_type +" - "+ str(round(file.size/1048576.0, 2))+"MB"
			total_size = total_size + file.size
		message = message +" / "+ str(total_size/1048576.0) + "MB"
	else:
		upload_list = "empty"
		message = "upload something"
	
	return render_to_response('file_upload.html', {
		'client': client,
		'job': job,
		'item': item,
		'upload_list': upload_list,
		'message': message,
	})

	
def write_file(upload_list, client, job, item):
	upload_dir = os.path.join(CONTENTS_PATH, str(client.pk), str(job.pk), str(item.pk), 'uploads')
	if os.path.isdir(upload_dir):
		print("upload_dir already exists: " + upload_dir)
		pass
	else:
		print("creating upload_dir... " + upload_dir)
		os.makedirs(upload_dir) # TODO: don't stop on OSError and jump to writing chunks

	for file in upload_list:
		filename = file.name
		with open(os.path.join(upload_dir, filename), 'wb+') as destination:
			for chunk in file.chunks():
				destination.write(chunk)
		process(150, upload_dir, filename, client, job, item, SEPS=False)


# add PDF to last rev of a page:
# create a temp file with pdf
# read first figure from filename (this is the starting absolute position)
# get number of pages from pdf (use pyPDF)
# construct array: number of pages = [first_page,pdf_num_pages]
# run gs and output all pages to a temp tiff (optional: run separations)
# A: run cmyk tiff to rgb jpeg
# B: run cmyk sep to rgb png
# folder structure:
# /client/job/item/page/rev/: in this folder only files related to page previews
# /client/job/item/page/rev/render/render.jpg: page previews in RGB jpg
# /client/job/item/page/rev/seps/C|M|Y|K|S(N).png: page separations in rgb png
# /client/job/item/pdf/date?/original filename.pdf: storage for uploaded pdf


# with number of pages, create a new revision assigned to each page starting from first_page
# each Revision has a FileField attached to it
# - FileField for render.jpg
# - FileField for seps png
# - FileField for uploaded PDF
# FileField is filled with path /client/job/item/page/rev/
# so assignation works like: N-result.jpg <-> N-original.pdf <-> N-seps.tiff <-> N-Page item 
# where N is the abs. page number
# there is another FileField for Revision for the uploaded pdf
# that points to /client/job/item/pdf/date?/original filename.pdf


# then user can add Comment to Revision using comment system
# create directory based on client.pk/job.pk/item.pk/page_num/rev

# FUNCTIONS:
# upload (upload_list, dirname, filename)
# upload file to temp folder 
# returns (uploaded_file)

# process (uploaded_file)
# create cmyk tiff->seps & jpg render in a temp folder
# returns (processed_files, seps)

# rename (processed_files, seps)
# copies file to real folder in /client/job/item/page/rev/render|seps
# move uploaded pdf somewhere safe
# returns (Revision with processed_file & uploaded_file attached)

# process_spots (seps)
# interface for approving which spot colors get loaded 
# returns save2item_conf (list of spot colors)

# comment (Revision)
# gets last created Revision for that page and adds Comment before publishing
# returns (Comment associated to Revision)

	

