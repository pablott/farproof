from django import template

register = template.Library()

@register.filter
def getcomment(rev):
	comment = rev.comment.comment
	return comment