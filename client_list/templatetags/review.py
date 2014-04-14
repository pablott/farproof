from django import template
from farproof.client_list.models import Page, Revision, Comment


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
	# This conditions also checks that POST data comes from the same page
	# where the send button was hit. Avoids accidentally adding comments 
	# from a different form and receiving POST twice from different forms 
	# (since forms share IDs in the template):
	if request.method == 'POST' and int(request.POST['from_page']) == page.rel_num:
		post = request.POST.copy()
		print(post)
		print('\nProcessing POST...')
		
		# Extract variables form POST message
		# TODO: sanitize entries
		comment = post['comment']
		new_status = post['status']
		pages = post.getlist('pages[]')
		print('\tpages: '+str(pages)+'\n\tcomment: '+str(comment)+'\n\tnew_status: '+str(new_status)+'\n\tfrom_page: '+str(post['from_page'])+'\n\tcalling_page: '+str(page.rel_num))
		
		# Create a comment and save it for later:
		new_comment = Comment(comment=comment)
		new_comment.save()
		print('\nNew Comment saved.\n')
		
		# Assign comment to a revision of its own page 
		# and also to each page in the "affects too" list.
		# This revision can be:
		# a) if the user adding the comment belongs to providers list, the current last_rev()
		# b) if the user adding the comment belongs to clients list, a new revision (i.e.: last_rev()+1)
		print('Pages affected:')
		print('count: \tpg_abs_num: \tpg_rel_num: \tcurr_rev: \tnew_rev: \tchanges rev?')
		c = 0
		for p in pages:
			current_page_num = int(p)
			current_page = Page.objects.get(rel_num=current_page_num, item=item)
			current_rev = current_page.last_rev()
			
			# Add new revision only when status has been changed
			if current_rev.status != new_status:
				new_rev_num = current_rev.rev_number+1
				new_revision = Revision(rev_number=new_rev_num, page=current_page, status=new_status)
				new_revision.save()
				revision = new_revision
				changes = 'Yes'
			else: # Do not create a new revision
				revision = current_rev
				changes = 'No'
			
			print(str(c)+'\t\t'+str(current_page.abs_num)+'\t\t'+str(current_page.rel_num)+'\t\t'+str(current_rev.rev_number)+'\t\t'+str(revision.rev_number)+'\t\t'+str(changes))
			
			# Associate new_comment to revision
			new_comment.revision.add(revision)
			c = c+1
			
		print('\nNew Comment \"'+str(new_comment.comment)+'\" added to pages '+str(pages)+' inside '+'\"'+str(job.name)+'\"/\"'+str(item.name)+'\".')
	return {
		'page': page,
		'item': item,
		'job': job, 
		'client': client,
	}

