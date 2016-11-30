from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.urlresolvers import reverse
from core.forms import form_button_submit, form_button_misc, build_helper
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
        
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control top', 'placeholder': "Username"}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control bottom', 'placeholder': "Password"}
        )
        
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
        
class PasswdForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswdForm, self).__init__(*args, **kwargs)
    
        self.fields['old_password'].widget.attrs.update(
            {'class': 'form-control single', 'placeholder': "Old Password"}
        )
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control top', 'placeholder': "New Password"}
        )
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control bottom', 'placeholder': "Repeat New Password"}
        )
        
        self.helper = build_helper()
        buttons = [
            form_button_submit(label='Commit'),
            form_button_misc(label='Nevermind'),
        ]
        self.helper.layout = Layout(
            Field('old_password', placeholder="Old Password"),
            Field('new_password1', placeholder="New Password"),
            Field('new_password2', placeholder="Retype New Password"),
            FormActions(*buttons)
        )