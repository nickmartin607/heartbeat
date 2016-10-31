from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field, Fieldset, Div
from crispy_forms.bootstrap import FormActions


class Form(ModelForm):
    title = ''
    field_dict = {}
    read_only = False
    form_class, field_class, wrapper_class = None, 'form-control', 'form-group'
    button_class = 'btn-lg btn-default btn-block'
    form_show_labels = True
        
    def __init__(self, *args, **kwargs):
        self.next_url = kwargs.pop('next_url', None)
        super(Form, self).__init__(*args, **kwargs)
        self.title = self.title or self._set_title()
        self.helper = self._build_helper()
        
        
    def _set_title(self):
        if self.instance.id:
            self.title = 'Modifying the {}: {}'.format(self._modelname(), self.instance)
        else:
            self.title = 'Create a New {}'.format(self._modelname())
        
    def _build_helper(self):
        helper = FormHelper()
        helper.form_show_labels = self.form_show_labels
        if self.form_class:
            helper.form_class = self.form_class
        
        
        for field, attrs in self.field_dict.items():
            if attrs.get('widget'):
                self.fields[field].widget = attrs.get('widget')
            self.fields[field].widget.attrs = attrs.get('attributes', {})
        
        layout = [self._build_helper_field(field) for field in self.fields]
        layout.append(HTML("</br>"))
        if not self.read_only:
            layout.append(self._build_helper_buttons())
        helper.layout = Layout(*layout)
        return helper
        
    
    def _build_helper_field(self, field):
        attrs = self.field_dict.get(field, {})
        element = Field(
            field,
            wrapper_class=self.wrapper_class,
            css_class=self.field_class,
            id=attrs.get('id'),
            placeholder=attrs.get('placeholder')
        )
        if self.read_only:
            element.attrs['readonly'] = True
        return element
        
    def _build_helper_buttons(self):
        buttons = Submit(
            self.next_url,
            'Submit',
            css_class=self.button_class
        )
        return buttons
        
    @classmethod
    def _modelname(cls, capitalize=True):
        name = str(cls._meta.model.modelname)
        return name.capitalize() if capitalize else name