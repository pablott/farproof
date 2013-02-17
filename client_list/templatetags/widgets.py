﻿from django import template

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
	
@register.inclusion_tag('widgets/page_odd.html')
def page_odd(page, item, job, client):
	return {
		'page': page,
		'item': item,
		'job': job, 
		'client': client
	}

@register.inclusion_tag('widgets/page_even.html')
def page_even(page, item, job, client):
	return {
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
	
	