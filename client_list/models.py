from django.db import models



class Client(models.Model):
	name = models.CharField(max_length=256)
	email = models.CharField(max_length=256)
	active = models.BooleanField(default=True)
	creation = models.DateTimeField(default="", auto_now_add=True)
	modified = models.DateTimeField(default="", auto_now=True)
	def __unicode__(self):
		return self.name + " " + str(self.creation) + " " + str(self.modified)

class Job(models.Model):
	client = models.ForeignKey(Client)
	name = models.CharField(max_length=256)
	active = models.BooleanField(default=True)
	# Return "Job name - Client"
	def __unicode__(self):
		return self.name + " - " + str(self.client)

class Item(models.Model):
	job = models.ForeignKey(Job)
	#pages = models.IntegerField()
	desc = models.CharField(max_length=256)
	name = models.CharField(max_length=256)
	def __unicode__(self):
		return self.name + " - " + self.job.name + " - " + str(self.job.client)

class Page(models.Model):
	item = models.ForeignKey(Item)
	number = models.IntegerField() #.unique
#	page_status = models.List()     accepted, rejected, pending (i.e. not yet evaluated), Here or in Revision?
	def __unicode__(self):
		return str(self.number)

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
		
