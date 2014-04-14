from django.core.files.storage import FileSystemStorage
from django.db import models
from django.forms import ModelForm, forms
from django.forms.widgets import HiddenInput
#from datetime import datetime
#from django.forms.models import inlineformset_factory
#from django.forms.formsets import BaseFormSet
from farproof.settings import CONTENTS_PATH
	
	
class Client(models.Model):
	name = models.CharField(max_length=256)
	desc = models.CharField(max_length=256, blank=True, null=True)
	active = models.BooleanField(default=True)
	creation = models.DateTimeField(default="", auto_now_add=True)
	modified = models.DateTimeField(default="", auto_now=True)
	def __unicode__(self):
		return  str(self.pk)+":"+self.name + " - " + str(self.modified)
		
class User(models.Model):
	client = models.ManyToManyField(Client)
	name = models.CharField(max_length=256, unique=True)
	email = models.EmailField(max_length=254, default='xx@xx.com')
	desc = models.CharField(max_length=256)
	admin = models.BooleanField(default=False)
	def __unicode__(self):
		return self.name + self.email		

class ClientAddForm(ModelForm):
	class Meta:
		model = Client
		fields = ('name','desc')
		
		
class Job(models.Model):
	client = models.ForeignKey(Client)
	name = models.CharField(max_length=256)
	desc = models.CharField(max_length=256, blank=True, null=True)
	active = models.BooleanField(default=True)
	creation = models.DateTimeField(default="", auto_now_add=True)
	modified = models.DateTimeField(default="", auto_now=True)
	def total_pages(self):
		count = 0
		for item in self.item_set.all():
			for page in item.page_set.all():
				count = count+1
		return count
	
	def is_ready(self):
		total_items = 0
		approved_items = 0
		for item in self.item_set.all():
			total_items = total_items+1
			if item.is_ready():
				approved_items=approved_items+1
		if total_items == approved_items:
			return True
		else:
			return False
		
	def __unicode__(self):
		return str(self.pk)+":"+self.name + " - " + self.client.name + " - " + str(self.modified)
		
	class Meta(object):
		unique_together = ("name", "client")

		
class JobAddForm(ModelForm):
	class Meta:
		model = Job	
		# "exclude" won't allow JobAddForm to render a 'client' field
		# in the template (because it's a FK), thus it will throw an error beacause view function 'job_add'
		# won't be able to assign the current Client object to 'client' in the processed POST.
		# The solution is using HiddenInput() widget for 'client' field. This way client name gets passed
		# to POST but is hidden in the template.
		exclude = ('active',)
		widgets = {
            'client': HiddenInput(),
        }
		
		
class Item(models.Model):
	job = models.ForeignKey(Job)
	name = models.CharField(max_length=256)
	desc = models.CharField(max_length=256, blank=True, null=True)
	creation = models.DateTimeField(default="", auto_now_add=True)
	modified = models.DateTimeField(default="", auto_now=True)
	
	def is_ready(self):
		total_pages = 0
		approved_pages = 0
		for page in self.page_set.all():
			total_pages = total_pages+1
			last_rev = page.last_rev()
			if last_rev.status == 'OK':
				approved_pages = approved_pages+1
		if total_pages == approved_pages and total_pages > 1 :
			return True
		else:
			return False
	
	def __unicode__(self):
		return str(self.pk)+":"+self.name + " - " + self.job.name + " - " + self.job.client.name + " - " + str(self.modified)
		
	class Meta(object):
		unique_together = ("name", "job")


class ItemAddForm(ModelForm):
	class Meta:
		model = Item				
		widgets = {
           'job': HiddenInput(),
		}
	  
		
class Page(models.Model):
	item = models.ForeignKey(Item)
	abs_num = models.IntegerField(default="1")
	rel_num = models.IntegerField(default="1")
	def last_rev(self):
		revisions = self.revision_set.filter(page=self).order_by('-creation')
		if revisions:
			last_rev = revisions[0]
		else:
			last_rev = 0
		return last_rev
		
	def __unicode__(self):
		return "page:"+str(self.abs_num) + "/pk:"+str(self.pk) + " - " + self.item.name + " - " + self.item.job.name + " - " + self.item.job.client.name

	class Meta(object):
		unique_together = ("abs_num", "item")

	
class Revision(models.Model):
	page = models.ForeignKey(Page)
	rev_number = models.IntegerField()
	creation = models.DateTimeField(auto_now_add=True)
	STATUS_CHOICES = (
		('OK', 'Ok'), # Page has been approved by Client
		('REJECTED', 'Rejected'), # Page has been rejected (by Client or automatically after adding a Comment by Provider)
		('PENDING', 'Pending'), # Page is awaiting Client's review
		('MISSING', 'Missing'), # No file uploaded for this page
	)
	status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='PENDING')
	def __unicode__(self):
		return "rev:"+str(self.rev_number)+"/pk:"+str(self.pk) + " - " + "page:"+ str(self.page.abs_num) + " - " + self.page.item.name + " - " + self.page.item.job.name + " - " + self.page.item.job.client.name

	class Meta(object):
		unique_together = ("rev_number", "page")		
		
		
class Comment(models.Model):
	revision = models.ManyToManyField(Revision)
	comment = models.CharField(max_length=256)
	def __unicode__(self):
		return self.comment + " - " + str(self.revision.all())

	
class CommonFile(models.Model):
	fs = FileSystemStorage(location=CONTENTS_PATH, base_url='/user')
	# fs.file_permissions_mode = 0644
	f = models.FileField(upload_to='uploads', storage=fs, default="")
	
	class Meta:
		abstract = True	


class PDFFile(CommonFile):
	# item = models.ForeignKey(Item)
	# TODO: implement
	# inks = pdfinfo.inks
	# pages = pdfinfo.pages
	# hash = sha256 string
	def __unicode__(self):
		return "pk:"+str(self.pk) + " file:"+str(self.f.name)
	
		
class RenderFile(CommonFile):
	# revision = models.ForeignKey(Revision)
	# TODO: implement
	# Set these options when processing file
	# color_space = RGB or CMYK
	# channel = RGB or CMYK or seps C|M|Y|K|named_color
	# options = {
				# in_profile,
				# rgb_outprofile,
				# cmyk_outprofile,
				# render_intent,
				# overprint,
				# bpc,
				# preserve_k,
	# }
	def __unicode__(self):
		return "pk:"+str(self.pk) + " file:"+str(self.f.name)

		
# class Curve(models.Model):
	# revision = models.ForeignKey(Revision)
	# curve = models.CharField(max_length=200)
	# def __unicode__(self):
		# return self.comment	+ " - " + self.page.item.client.name + "rev pk:"+str(self.revision.pk)
