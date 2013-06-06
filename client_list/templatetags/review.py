from django import template
from farproof.client_list.models import Comment
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
def comment_add(contx, page, item, job, client):
# TODO this takes 'request' as a string when called when it should be the POST data
	# print(contx)
	# if contx:
		# request = contx['request']   
	# else:
		# request = 'rrr'
	if contx.method == 'POST': # If the form has been submitted...
		form = CommentAddForm(contx.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			# Process the data in form.cleaned_data
			form.save()
			message = 'You added Comment: %r' % str(request.POST['comment']) #+ ' - %r' % str(request.POST['email'])
			form = CommentAddForm() # Reset form after saving
	else:
		message = ''
	form = CommentAddForm() # An unbound form
	return {
		#'request': request,
		'form': form,
		#'message': message,
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
	