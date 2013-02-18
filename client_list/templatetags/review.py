from django import template

register = template.Library()


@register.inclusion_tag('widgets/affects_too.html')
def affects_too(comment, page, item, job, client):
	revisions = comment.revision.all() # Get all revisions with that associated comment
	last_rev = page.last_rev() # Get last revision for current page
	revisions = revisions.exclude(pk=last_rev.pk) # Finally, exclude last_rev itself from list
		
	return {
		'revisions': revisions,
		'item': item,
		'job': job, 
		'client': client,
	}


