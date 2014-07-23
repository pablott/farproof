from django import template

register = template.Library()


@register.inclusion_tag('widgets/client.html')
def show_client(client):
	return {
		'client': client
	}
	
@register.inclusion_tag('widgets/client_unactive.html')
def show_client_unactive(client):
	return {
		'client': client
	}

@register.inclusion_tag('widgets/job.html')
def show_job(job, client):
	return {
		'job': job, 
		'client': client
	}

@register.inclusion_tag('widgets/job_thumb.html')
def show_job_thumb(job, client):
	return {
		'job': job, 
		'client': client
	}

@register.inclusion_tag('widgets/job_unactive.html')
def show_job_unactive(job, client):
	return {
		'job': job, 
		'client': client
	}
	
@register.inclusion_tag('widgets/item.html')
def show_item(item, job, client):
	return {
		'item': item,
		'job': job, 
		'client': client
	}
	
@register.inclusion_tag('widgets/item_thumb.html')
def show_item_thumb(item, job, client):
	return {
		'item': item,
		'job': job, 
		'client': client
	}

@register.inclusion_tag('widgets/item_list.html')
def item_list(item, job, client):
	return {
		'item': item,
		'job': job, 
		'client': client
	}
	
# Context has to be passed explicitly to tags that depend on page_odd 
# like comment_add() template tag. I suspect this is caused by linking two 
# template tags, one inside the other, and calling them from a parent view 
@register.inclusion_tag('widgets/page_odd.html', takes_context=True)
def page_odd(context, page, item, job, client):
	context = context['request']
	return {
		'context': context,
		'page': page,
		'item': item,
		'job': job, 
		'client': client
	}

@register.inclusion_tag('widgets/page_even.html', takes_context=True)
def page_even(context, page, item, job, client):
	context = context['request']
	return {
		'context': context,
		'page': page,
		'item': item,
		'job': job, 
		'client': client
	}
	
@register.inclusion_tag('widgets/page_thumb_odd.html')
def page_thumb_odd(page, item, job, client):
	return {
		'page': page,
		'item': item,
		'job': job, 
		'client': client
	}

@register.inclusion_tag('widgets/page_thumb_even.html')
def page_thumb_even(page, item, job, client):
	return {
		'page': page,
		'item': item,
		'job': job, 
		'client': client
	}
	
@register.inclusion_tag('widgets/comment.html')
def show_comment(comment, page, item, job, client):
	return {
		'comment': comment,
		'page': page,
		'item': item,
		'job': job, 
		'client': client,
	}