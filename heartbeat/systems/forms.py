from django import forms
from core.forms import Form
from .models import Host, Service, Credential


class HostForm(Form):
    field_dict = {
        'notes': {'attributes': {'rows': 5, 'style': 'resize:vertical'}}
    }
        
    class Meta:
        fields = ['team', 'ip', 'name', 'hostname', 'os', 'notes']
        model = Host
        
        
class ServiceForm(Form):
    field_dict = {
        'expected_result': {'attributes': {'rows': 3, 'style': 'resize:vertical'}}
    }
    
    class Meta:
        fields = ['host', 'protocol', 'port', 'expected_result', 'point_value']
        model = Service


class CredentialForm(Form):
    old_password = forms.CharField()
    new_password = forms.CharField()
    
    title = 'Change Service Credentials'
    form_class, wrapper_class = 'form-signin', ''
    form_show_labels = False
    field_dict = {
        'username': {'placeholder': 'Username', 'id': 'single'},
        'old_password': {'widget': forms.PasswordInput(), 'placeholder': 'Enter the Old Password', 'id': 'single'},
        'password': {'widget': forms.PasswordInput(), 'placeholder': 'Enter the New Password', 'id': 'top'},
        'new_password': {'widget': forms.PasswordInput(), 'placeholder': 'Retype the New Password', 'id': 'bottom'},
    }
    
    class Meta:
        fields = ['username', 'old_password', 'password', 'new_password']
        model = Credential
