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
	if request.method == 'POST': # If the form has been submitted...
		post = request.POST.copy()
		print(post)
		print('POST received')
		print(post['comment'])
		pages = dict(post)['pages']
		
		
		
		# TODO add its own page to pages dict
		# pages += u'page.number'
		
		
		
		
		print(pages[0])
		#p=pages.keys()
		#print(p)
		
		# Form comment and save it:
		t = post['comment']
		status = post['status']
		new_comment = Comment(comment=t)
		new_comment.save()
		
		# Assign comment to the revision of each page in the "affects too" list.
		# This revision can be:
		# a) if the user adding the comment belongs to providers list, the current last_rev()
		# b) if the user adding the comment belongs to clients list, a new revision (i.e.: last_rev()+1)
		# TODO: create users subsystem
		for i in pages:
			current_page_num = int(i)
			current_page = Page.objects.get(number=current_page_num, item=item)
			current_rev = current_page.last_rev()
			print('current_page: '+str(current_page))
			print(current_rev)
			
			if 1: # If user belongs to provider
				revision = current_rev
				# TODO: add new revision if previous is OK or PENDING, 
				# right now it doesn't add any new revision but it should
				
				
				
				
			else: # If user belongs to client
				new_rev_num = current_rev.rev_number+1
				print('new_rev_num: '+str(new_rev_num))
				new_revision = Revision(rev_number=new_rev_num, page=current_page, status=status)
				print(new_revision)
				new_revision.save()
				revision = new_revision
			
			# Add each new revision to the new comment
			new_comment.revision.add(revision)
			print(new_comment)

			
		form = CommentAddForm() # Reset form after saving
	else:
		print ('Empty form')
	form = CommentAddForm() # An unbound form
	return {
		'form': form,
		'page': page,
		'item': item,
		'job': job, 
		'client': client,
	}

	
@register.inclusion_tag('widgets/comment_add.html', takes_context=True)
def comment_add2(context, page, item, job, client):
	return template.RequestContext(context['request'], {
		'request': request,
		'form': form,
		'message': message,
		'page': page,
		'item': item,
		'job': job, 
		'client': client,
	})
	