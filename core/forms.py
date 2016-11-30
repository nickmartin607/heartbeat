from django.core.urlresolvers import reverse
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Field, Submit, HTML
    
    
def build_helper():
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-3'
    helper.field_class = 'col-lg-9'
    helper.layout = Layout()
    return helper

def form_button_submit(label='Submit'):
    return Submit('submit', label)
    
def form_button_misc(url=None, label='Cancel'):
    html = '<a type="button" href="{}" class="btn btn-primary">{}</a> '
    return HTML(html.format(url or reverse('index'), label))
    
class BaseForm(forms.Form):
    hidden_fields = []
    def __init__(self, *args, **kwargs):
        try:
            form_fields = self._meta.fields
        except:
            form_fields = self.fields
        super(BaseForm, self).__init__(*args, **kwargs)
        layout = [Field(f) for f in form_fields if f not in self.hidden_fields]
        layout += [Field(f, type='hidden') for f in form_fields if f in self.hidden_fields]
        layout += [self.build_buttons()]
        self.helper = build_helper()
        self.helper.layout = Layout(*layout)
    
    def build_buttons(self, extra_buttons=[]):
        actions = [
            form_button_submit(),
            form_button_misc(url=reverse(self.redirect_url))
        ] + extra_buttons
        return FormActions(*actions)
        
class Form(BaseForm, forms.ModelForm):
    def build_buttons(self):
        extra_buttons = []
        try:
            delete_url = reverse(
                '{}:delete'.format(self._meta.model._meta.model_name),
                args=[self.instance.id]
            )
            extra_buttons = [form_button_misc(url=delete_url, label='Delete')]
        except:
            pass
        return super(Form, self).build_buttons(extra_buttons)
        