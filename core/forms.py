from django.core.urlresolvers import reverse
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Field, Submit, HTML
        
BUTTON_HTML = '<input type="button" href="{}" value="{}" class="btn btn-primary">'
    
def build_helper():
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-3'
    helper.field_class = 'col-lg-9'
    helper.layout = Layout()
    return helper

def submit_button(label='Submit'):
    return Submit('submit', label)
def misc_button(url='index', label='Cancel'):
    return HTML(BUTTON_HTML.format(reverse(url), label))
    
class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        try:
            form_fields = self._meta.fields
        except:
            form_fields = self.fields
        super(BaseForm, self).__init__(*args, **kwargs)
        layout = [Field(f) for f in form_fields] + [self.build_buttons()]
        self.helper = build_helper()
        self.helper.layout = Layout(*layout)
    
    def build_buttons(self, extra_buttons=[]):
        actions = [submit_button(), misc_button(url=self.redirect_url)] + extra_buttons
        return FormActions(*actions)
        
class Form(BaseForm, forms.ModelForm):
    def build_buttons(self):
        extra_buttons = []
        try:
            delete_url = reverse('{}:delete'.format(self._meta.model._meta.model_name), args=[self.instance.id])
            extra_buttons = [misc_button(url=delete_url, label='Delete')]
        except:
            pass
        return super(Form, self).build_buttons(extra_buttons)
        