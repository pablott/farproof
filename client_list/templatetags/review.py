from django import template

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
			print(revision.pk)
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


