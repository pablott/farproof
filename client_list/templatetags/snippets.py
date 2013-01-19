from django import template

register = template.Library()


@register.inclusion_tag('snippets/client.html')
def show_client(client):
	return {
		'client': client
	}

@register.inclusion_tag('snippets/job.html')
def show_job(job, client):
	return {
		'job': job, 
		'client': client
	}

@register.inclusion_tag('snippets/item.html')
def show_item(item, job, client):
	return {
		'item': item,
		'job': job, 
		'client': client
	}
	
@register.inclusion_tag('snippets/page_odd.html')
def page_odd(page, item, job, client):
	return {
		'page': page,
		'item': item,
		'job': job, 
		'client': client
	}

@register.inclusion_tag('snippets/page_even.html')
def page_even(page, item, job, client):
	return {
		'page': page,
		'item': item,
		'job': job, 
		'client': client
	}
	
@register.inclusion_tag('snippets/page_thumb_odd.html')
def page_thumb_odd(page, item, job, client):
	return {
		'page': page,
		'item': item,
		'job': job, 
		'client': client
	}

@register.inclusion_tag('snippets/page_thumb_even.html')
def page_thumb_even(page, item, job, client):
	return {
		'page': page,
		'item': item,
		'job': job, 
		'client': client
	}
	
	