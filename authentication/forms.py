from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.urlresolvers import reverse
from core.forms import BaseForm, form_button_submit, form_button_misc, build_helper
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Fieldset
        
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.title = "Let Me In!"
        self.helper = FormHelper()
        self.helper.form_class = 'form-signin'
        self.helper.form_show_labels = False
        
        super(LoginForm, self).__init__(*args, **kwargs)
        
        self.helper.layout = Layout(
            Fieldset('Login',
                Field('username', id='top', placeholder='Username'),
                Field('password', id='bottom', placeholder='Password')
            ),
            FormActions(
                Submit(
                    reverse('login'),
                    'Open Sesame!',
                    css_class='btn btn-lg btn-default btn-block'
                ),
                css_class="action-center"
            )
        )
class PasswdForm(PasswordChangeForm, BaseForm):
    fields = ['old_password', 'new_password1', 'new_password2']
    redirect_url = 'index'