from dajax.core import Dajax

from django.shortcuts import render_to_response
from django.template import RequestContext



from django.template.loader import render_to_string
from django.template import Context







from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

#http://django-dajaxice.readthedocs.org/en/latest/quickstart.html

@dajaxice_register
def sayhello(request):
	#request = context.get('request')
	print('DAJAX!!!')
	#return simplejson.dumps({'message':'Hello Worldddd'})
	message2 = '333'
	dajax = Dajax()
	html = render_to_string('upload_content.html',
        {'message': message2,
		}, context_instance = RequestContext(request)
		)
	print(html)
	dajax.assign('#message','innerHTML',html)
	print('000000000')
	return dajax.json()
