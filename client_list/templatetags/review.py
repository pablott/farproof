from django import template

register = template.Library()


@register.inclusion_tag('widgets/affects_too.html')
def affects_too(comment, page, item, job, client):
	revisions = comment.revision.all() # Get all revisions with that associated comment
	last_rev = page.last_rev() # Get last revision for current page
	current_revisions = revisions.exclude(pk=last_rev.pk) # Finally, exclude last_rev itself from list
	
	# To query past revisions we need to go throught the queryset
	# and discard those revisions which are the last_rev() of its own page
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


