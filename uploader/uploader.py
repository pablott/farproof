from django.shortcuts import render_to_response # Add get_object_or_404
from farproof.client_list.models import Client, Job, Item, Page, Revision
from farproof.process.process import *

import os, subprocess


#TODO: JSON and MD5 client-side checksum verified by server-side checksum

PDF_PATH = "D:/tmp/pdf/" #TODO: unify with process.py and set in a separate conf file


def file_upload(request, client_pk, job_pk, item_pk, page_num):
	client = Client.objects.get(pk=client_pk)
	job = Job.objects.get(pk=job_pk, client=client)
	item = Item.objects.get(pk=item_pk, job=job)
	page = Page.objects.get(number=page_num, item=item)

	if request.method == 'POST':
		#form = request.FILES # bind to a form
		#if form.is_valid():
		upload_list = request.FILES.getlist('uploads') # this is a MultiValueDict 
		write_file(upload_list, client, job, item, page)
		message = "Uploaded files: "
		total_size = 0
		for file in upload_list:
			message = message +" - "+ file.name +" - "+ file.content_type +" - "+ str(round(file.size/1048576.0, 2))+"MB"
			total_size = total_size + file.size
		message = message +" / "+ str(total_size/1048576.0) + "MB"
	else:
		upload_list = "empty"
		message = "upload something"
	return render_to_response('file_upload.html', {
		'client': client,
		'job': job,
		'item': item,
		'page': page,
		'upload_list': upload_list,
		'message': message,
	})

	
def write_file(upload_list, client, job, item, page):
	#http://stackoverflow.com/questions/117250/how-do-i-get-a-decimal-value-when-using-the-division-operator-in-python
	# temp_dir = PDF_PATH + str(client.pk) +"/"+ str(job.pk) +"/"+ str(item.pk) +"/"+ str(page.pk) +"/"+ str(page.last_rev().rev_number+1) +"/"
	temp_dir = PDF_PATH + str(client.pk) +"/"+ str(job.pk) +"/"+ str(item.pk) +"/uploads/"
	
	#http://code.activestate.com/recipes/82465-a-friendly-mkdir/
	if os.path.isdir(temp_dir):
		pass
		#raise OSError("a path with the same name as the desired " \
		#"dir, '%s', already exists." % temp_dir)
	else:
		os.makedirs(temp_dir) # TODO: don't stop on OSError and jump to writing chunks
	#os.mkdir(os.path.join(PDF_PATH, temp_dir)) #TODO: remove

	for file in upload_list:
		filename = file.name
		with open(temp_dir + filename, 'wb+') as destination:
			for chunk in file.chunks():
				destination.write(chunk)
		process(150, temp_dir, filename)
		assign(temp_dir, filename, client, job, item, page)


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

	
#file.name           # Gives name
#file.content_type   # Gives Content type text/html etc
#file.size           # Gives file's size in byte
#file.read() 	
