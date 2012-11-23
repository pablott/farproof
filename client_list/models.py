from django.db import models

# Create your models here.

#class Poll(models.Model):
#    question = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')

#class Choice(models.Model):
#    poll = models.ForeignKey(Poll)
#    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField()

class Client(models.Model):
	client_name = models.CharField(max_length=256)
	email = models.CharField(max_length=256)
	email = models.CharField(max_length=256)
	active = models.BooleanField(default=True)
	creation = models.DateTimeField(default="", auto_now_add=True)
	modified = models.DateTimeField(default="", auto_now=True)
	def __unicode__(self):
		return self.client_name + " " + str(self.creation) + " " + str(self.modified)

class Job(models.Model):
	client = models.ForeignKey(Client)
	job_name = models.CharField(max_length=256)
	active = models.BooleanField(default=True)
	# Return "Job name - Client"
	def __unicode__(self):
		return self.job_name + " - " + str(self.client)

class Item(models.Model):
	job = models.ForeignKey(Job)
	pages = models.IntegerField()
	item_name = models.CharField(max_length=256)
	def __unicode__(self):
		return self.item_name + " - " + self.job.job_name + " - " + str(self.job.client)

class Page(models.Model):
	item = models.ForeignKey(Item)
	page_number = models.IntegerField() #.unique
#	page_status = models.List()     accepted, rejected, pending (i.e. not yet evaluated), Here or in Revision?
	def __unicode__(self):
		return str(self.page_number)

class Revision(models.Model):
	rev_number = models.IntegerField()
	page = models.ForeignKey(Page)
	STATUS_CHOICES = (
        ('OK', 'Ok'),
        ('FAIL', 'Fail'),
        ('PENDING', 'Pending'),
    )
	status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='PENDING')
	def __unicode__(self):
		return str(self.rev_number)

class Comment(models.Model):
	revision = models.ForeignKey(Revision)
	comment = models.CharField(max_length=200)
	def __unicode__(self):
		return self.comment

# PDF uploaded by the content provider to the server
class PDF(models.Model):
	revision = models.ForeignKey(Revision)
	pdf_ref = models.CharField(max_length=30)
	def __unicode__(self):
		return self.pdf_ref

# PDF uploaded by the client as a correction
class Correction(models.Model):
	revision = models.ForeignKey(Revision)
	corr_ref = models.CharField(max_length=30)
	def __unicode__(self):
		return self.corr_ref
		
