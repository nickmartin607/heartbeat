from core.forms import Form
from .models import Inject
from datetimewidget import widgets


class InjectForm(Form):
    field_dict = {
        'available': {'widget': widgets.DateTimeWidget(
            attrs={'id': 'available_id'}, options={'format': 'mm/dd/yyyy HH:ii:ss'}, usel10n=True, bootstrap_version=3
        ), 'id': 'available_id'},
        'deadline': {'widget': widgets.DateTimeWidget(
            attrs={'id': 'available_id'}, options={'format': 'mm/dd/yyyy HH:ii:ss'}, usel10n=True, bootstrap_version=3
        ), 'id': 'deadline_id'},
        'details': {'attributes': {'rows': 3, 'style': 'resize:vertical'}},
    }

    class Meta:
        fields = ['team', 'subject', 'details', 'point_value', 'available', 'deadline']
        model = Inject


class InjectViewForm(Form):
    read_only = True
    field_dict = {
        'details': {'attributes': {"rows": '20',}},
    }
    
    class Meta:
        fields = ['details', 'point_value', 'available', 'deadline']
        model = Inject
