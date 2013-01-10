from django import template

register = template.Library()


@register.inclusion_tag('snippets/job.html')
def show_job(job, client):
	return {
		'job': job, 
		'client': client
	}
