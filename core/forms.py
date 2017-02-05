from django.forms import ModelForm, forms
from django.forms.widgets import HiddenInput
from farproof.core.models import Client, Job, Item



class ClientAddForm(ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'desc')


class JobAddForm(ModelForm):
    class Meta:
        model = Job
        # "exclude" won't allow JobAddForm to render a 'client' field
        # in the template (because it's a FK), thus it will throw an error beacause view function 'job_add'
        # won't be able to assign the current Client object to 'client' in the processed POST.
        # The solution is using HiddenInput() widget for 'client' field. This way client name gets passed
        # to POST but is hidden in the template.
        exclude = ('active',)
        widgets = {
            'client': HiddenInput(),
        }


class ItemAddForm(ModelForm):
    class Meta:
        model = Item
        exclude = ('job', 'pages')
        widgets = {
            'job': HiddenInput(),
            'pages': HiddenInput(),
        }
