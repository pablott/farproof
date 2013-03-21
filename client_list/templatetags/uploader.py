from django import template

register = template.Library()


@register.inclusion_tag('widgets/uploader.html')
def uploader(upload_list):
	for file in upload_list:
		total_size = total_size + file.size
	message = message +" / "+ str(total_size/1048576.0) + "MB"

	return {
		'upload_list': upload_list,
	}


