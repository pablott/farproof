from django import template
from farproof.client_list.models import Page, Revision, Comment
from farproof.client_list.models import CommentAddForm
#from django.core.context_processors import request


register = template.Library()


@register.inclusion_tag('widgets/affects_too.html')
def affects_too(comment, page, item, job, client):
	revisions = comment.revision.all() # Get all revisions with that associated comment
	last_rev = page.last_rev() # Get last revision for current page
	current_revisions = revisions.exclude(pk=last_rev.pk) # This excludes  exclude last_rev itself from list
	
	# To query current revisions we need to go through the queryset
	# and discard past revisions (those which are NOT the last_rev() of its own page)
	for revision in current_revisions:
		if revision.pk == revision.page.last_rev().pk:
			pass
		else:
			#print(revision.pk)
			current_revisions = current_revisions.exclude(pk=revision.pk)
	
	# To query past revisions we need to go through the queryset
	# and discard the last revision of each page (those which are the last_rev() of its own page)
	past_revisions = revisions
	for revision in past_revisions:
		past_revisions = past_revisions.exclude(pk=revision.page.last_rev().pk)
		
	return {
		'current_revisions': current_revisions,
		'past_revisions': past_revisions,
		'page': page,
		'item': item,
		'job': job, 
		'client': client,
	}


@register.inclusion_tag('widgets/comment_add.html')
def comment_add(request, page, item, job, client):
	if request.method == 'POST': #and 'valid'==page.number: # If the form has been retrieved...
		post = request.POST.copy()
		print(post)
		
		if int(post['page_from']) == page.number:
		# if str('from_page-'+page.number)request.POST:
			print('same')
		else:
			print('not same')
		print(page.number)
		
		# Extract variables form POST message
		comment = post['comment']
		new_status = post['status']
		# pages = dict(post)['pages']
		# Does it duplicate POST message? no
		pages = post.getlist('pages[]')
		
		# Explicitly append current page number
		# (is not enough marking the cell as 'checked' in the html template)
		# TODO: reorder (just for convenience) and sanitize (only integer numbers)
		print('pages: '+str(pages))
		# pages.append(page.number)
		
		# Create a comment and save it for later:
		new_comment = Comment(comment=comment)
		new_comment.save()
		
		# Assign comment to a revision of its own page 
		# and each page in the "affects too" list.
		# This revision can be:
		# a) if the user adding the comment belongs to providers list, the current last_rev()
		# b) if the user adding the comment belongs to clients list, a new revision (i.e.: last_rev()+1)
		print('PAGES AFFECTED:')
		print('iter: \tcurr_pg_num: \tcurr_rev: \tnew_rev:')
		c = 0
		for i in pages:
			current_page_num = int(i)
			current_page = Page.objects.get(number=current_page_num, item=item)
			current_rev = current_page.last_rev()
			
			# Add new revision only when status has been changed
			if current_rev.status != new_status:
				new_rev_num = current_rev.rev_number+1
				new_revision = Revision(rev_number=new_rev_num, page=current_page, status=new_status)
				new_revision.save()
				revision = new_revision
			else: # Do not create a new revision
				revision = current_rev
			
			print(str(c)+'\t\t'+str(current_page.number)+'\t\t'+str(current_rev.rev_number)+'\t\t'+str(revision.rev_number))
			
			# Associate new_comment to revision
			new_comment.revision.add(revision)
			c = c+1

		print("DONE\n")
		form = CommentAddForm() # Reset form after saving
	else:
		print ('Empty unbound form')
		form = CommentAddForm() # An unbound form
	return {
		'form': form,
		'page': page,
		'item': item,
		'job': job, 
		'client': client,
	}

