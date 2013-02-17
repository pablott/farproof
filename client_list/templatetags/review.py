from django import template

register = template.Library()


@register.inclusion_tag('widgets/affects_too.html')
def affects_too(comment, page, item, job, client):
	revisions = comment.revision.all() # Get all revisions with that associated comment
	last_rev = page.last_rev()
	revisions = revisions.exclude(pk=last_rev.pk) # Exclude revision associated to 'page'
	#revisions = revisions.exclude(pk=last_rev.pk)
	
	#affected_pages = page.revisions_set
	
	#for revisions
	#	if revision == revision.page.last_rev
	#		rev_list = rev_list + revision

	#TODO get only last revisions
	
	#for revision in revisions:
	#	affected_pages = revision.page
		
	return {
		'revisions': revisions,
		#'rev_list': rev_list,
		'item': item,
		'job': job, 
		'client': client,
	#	'affected_pages': affected_pages,
	#	'page': page
	}

	