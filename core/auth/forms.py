from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse as url_reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field, Fieldset, Div
from crispy_forms.bootstrap import FormActions
        
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.title = "Let Me In!"
        super(LoginForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({'class': 'form-control top', 'placeholder': "Username"})
        self.fields['password'].widget.attrs.update({'class': 'form-control bottom', 'placeholder': "Password"})
        
        self.helper = FormHelper()
        self.helper.form_class = 'form-signin'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(Fieldset('Login',
            Field('username', id='top', placeholder='Username'),
            Field('password', id='bottom', placeholder='Password')),
            FormActions(Submit(url_reverse('login'), 'Open Sesame!', css_class='btn btn-lg btn-default btn-block'), css_class="action-center")
        )
    
        
class PasswdForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        title = "Change our Password!"
        super(PasswdForm, self).__init__(*args, **kwargs)
        
        self.fields['old_password'].widget.attrs.update({'class': 'form-control single', 'placeholder': "Old Password"})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control top', 'placeholder': "New Password"})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control bottom', 'placeholder': "Repeat New Password"})
        
        self.helper = FormHelper()
        self.helper.form_class = 'form-signin'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('old_password', id='single', placeholder="Old Password"),
            Field('new_password1', id='top', placeholder="New Password"),
            Field('new_password2', id='bottom', placeholder="Retype New Password"),
            Div(Submit(url_reverse('passwd'), 'Change The Password!', css_class='btn btn-default btn-block'), css_class='action-center'),
            Div(Submit(url_reverse('index'), 'Nevermind', css_class='btn btn-default btn-block'), css_class='action-center')
        )