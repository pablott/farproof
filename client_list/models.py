#from datetime import datetime
from django.db import models
from django.forms import ModelForm, forms
#from django.forms.models import inlineformset_factory
#from django.forms.formsets import BaseFormSet
from django.forms.widgets import HiddenInput





class User(models.Model):
	name = models.CharField(max_length=256)
	email = models.CharField(max_length=256, default='xx@xx.com')
	admin = models.BooleanField(default=False)
	def __unicode__(self):
		return self.name
	
class Client(models.Model):
	name = models.CharField(max_length=256)
	email = models.CharField(max_length=256)
	active = models.BooleanField(default=True)
	creation = models.DateTimeField(default="", auto_now_add=True)
	modified = models.DateTimeField(default="", auto_now=True)
	def __unicode__(self):
		return self.name + " - " + str(self.creation) + " - " + str(self.modified) + " - " + str(self.id)

class ClientAddForm(ModelForm):
	class Meta:
		model = Client		
		fields = ('name', 'email')
		
		
class Job(models.Model):
	client = models.ForeignKey(Client)
	name = models.CharField(max_length=256)
	desc = models.CharField(max_length=256)
	active = models.BooleanField(default=True)
	creation = models.DateTimeField(default="", auto_now_add=True)
	modified = models.DateTimeField(default="", auto_now=True)
	
	def total_items(self):
		total_items = self.item_set.count()
		return total_items
		
	def total_pages(self):
		count = 0
		if self.item_set:
			for item in self.item_set.all():
				for page in item.page_set.all():
					count = count+1
			message = 'there are %r pages' % count 
		else:
			message = 'there are NO pages'
		return message
		
	# Return "Job name - Client - Date"
	def __unicode__(self):
		return self.name + " - " + self.client.name + " - " + str(self.creation)

		
class JobAddForm(ModelForm):
	class Meta:
		model = Job	
		# "exclude" won't allow JobAddForm to render a 'client' field
		# in the template (because it's a FK), thus it will throw an error beacause view function 'job_add'
		# won't be able to assign the current Client object to 'client' in the processed POST.
		# The solution is using HiddenInput() widget for 'client' field.
		exclude = ('active')
		widgets = {
            'client': HiddenInput(),
        }
		
		
class Item(models.Model):
	job = models.ForeignKey(Job)
	name = models.CharField(max_length=256)
	desc = models.CharField(max_length=256)
	# active = models.BooleanField(default=True)
	def __unicode__(self):
		return self.name + " - " + self.job.name + " - " + self.job.client.name

	
class ItemAddForm(ModelForm):
	class Meta:
		model = Item				
		widgets = {
           'job': HiddenInput(),
      }
# ItemAddFormSet = inlineformset_factory(JobAddForm, ItemAddForm)


#ItemAddForm = inlineformset_factory(models.Item, models.Page, extra=1)	
#class ItemAdd(ModelForm):
#	TenantFormset = inlineformset_factory(models.Building, models.Tenant, extra=1)	
#class BaseItemFormSet(BaseFormSet):
#	def add_fields(self, form, index):
#		super(BaseItemFormSet, self).add_fields(form, index)
#		form.fields["my_field"] = forms.CharField()
		#delete_box = forms.BooleanField()

	#class Meta:
	#	model = Item				
	#	widgets = {
	#		'job': HiddenInput(),
	#	}

#ItemAddForm = formset_factory(Item, form=BaseItemFormSet)		
		


		
class Page(models.Model):
	item = models.ForeignKey(Item)
	number = models.IntegerField(default="0") #.unique
	def last_rev(self):
		revisions = self.revision_set.filter(page=self).order_by('-pk')
		if revisions:
			last_rev = revisions[0]
		else:
			last_rev = '--'
		return last_rev
		
	def __unicode__(self):
		return str(self.number) + " - " + self.item.name

		
class Revision(models.Model):
	page = models.ForeignKey(Page)
	creation = models.DateTimeField(auto_now_add=True)
	rev_number = models.IntegerField()
	STATUS_CHOICES = (
		('OK', 'Ok'),
		('FAIL', 'Fail'),
		('PENDING', 'Pending'),
		('MISSING', 'Missing'),
	)
	status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='PENDING')
	def __unicode__(self):
		return str(self.rev_number) + " - " + "page: " + str(self.page.number) + " - " + self.page.item.name

		
class Comment(models.Model):
	revision = models.ManyToManyField(Revision)
	#revision = models.ForeignKey(Revision)
	comment = models.CharField(max_length=200)
	def __unicode__(self):
		return self.comment
		
		
class Curve(models.Model):
	revision = models.ForeignKey(Revision)
	curve = models.CharField(max_length=200)
	def __unicode__(self):
		return self.comment		
		
		
# PDF uploaded by the content provider to the server
class ProviderContent(models.Model):
	revision = models.ForeignKey(Revision)
	pdf_ref = models.CharField(max_length=30)
	def __unicode__(self):
		return self.pdf_ref

		
# PDF uploaded by the client as a correction
class ClientContent(models.Model):
	revision = models.ForeignKey(Revision)
	corr_ref = models.CharField(max_length=30)
	def __unicode__(self):
		return self.corr_ref
		
