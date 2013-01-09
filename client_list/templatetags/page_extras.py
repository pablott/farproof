from django import template

register = template.Library()

#@register.filter
#def lower2(value):
#	#comment = 2
#	return value.lower()

def lower2(value):
	return value.lower()
