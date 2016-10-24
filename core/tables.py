import collections, datetime, urllib
from django.contrib.auth.models import User
from django.utils import timezone
from core.html import get_tag, get_symbol

        
class Table:
    common_actions = ['passwd', 'modify', 'delete', 'enabled']
    booleans = ['status', 'enabled']
    
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name', '')
        self.model = kwargs.pop('model', None)
        self.elements = kwargs.pop('elements', [])
        if not len(self.elements):
            self.name = "No items exist"
        super(Table, self).__init__(*args, **kwargs)
    
    def sort(self, order_by):
        self.elements = self.elements.order_by(order_by)
        
    def build(self, request):
        is_staff = User.objects.get(id=request.user.id).is_staff
        table = self.table_header(request, is_staff) + self.table_body(request, is_staff)
        if self.elements:
            h2_tag = get_tag('h2', self.name, css_class='sub-header')
            table_tag = get_tag('table', table, css_class='table table-striped')
            html = h2_tag + get_tag('table', table_tag, css_class='table-responsive')
        else:
            label = "No {}s currently available!".format(self.model._modelname().capitalize())
            html = get_tag('h2', label, css_class='sub-header')
        return html

    def table_header(self, request, is_staff):
        th_tags = ''
        for column in self.columns:
            if column.get('staff-only') and not is_staff:
                pass
            elif column.get('blue-only') and 'blue' not in str(request.user.account._team()):
                pass
            else:
                req = request.GET.copy()
                value = self.table_header_cell(column, req)
                css_class = ' '.join(column.get('styles', []))
                th_tags += get_tag('th', value, css_class=css_class)
        return get_tag('thead', get_tag('tr', th_tags))
    
    def table_header_cell(self, column, request):
        field = column.get('field', '')
        if field:
            label = self.model._fieldname(field)
        else:
            field = column.get('action', '')
            label = field.capitalize()
        if not column.get('no-sort', False) and field not in self.common_actions:
            symbol = ""
            new_sort = '-' + field
            old_sort = request.get('order_by', '')
            if 'order_by' in request.keys():
                old_sort = request.get('order_by', '')
                if old_sort.startswith('-') and old_sort.lstrip('-') == field:
                    new_sort = field
                    symbol = get_symbol('desc')
                elif old_sort.lstrip('-') == field:
                    symbol = get_symbol('asc')
            request['order_by'] = new_sort
            items = collections.OrderedDict(sorted(request.items()))
            href = '?{}'.format(urllib.parse.urlencode(items))
            value = '{}{}'.format(get_tag('a', label, href=href), symbol)
        else:
            value = label
        return value
    
    def table_body(self, request, is_staff):
        tr_tags = ''
        for element in self.elements:
            td_tags = ''
            for column in self.columns:
                if column.get('staff-only') and not is_staff:
                    pass
                elif column.get('blue-only') and 'blue' not in str(request.user.account._team()).lower():
                    pass
                else:
                    cell = self.table_body_cell(element, column, is_staff)
                    td_tags += get_tag('td', cell, css_class=' '.join(column.get('styles', [])))
            tr_tags += get_tag('tr', td_tags)
        return get_tag('tbody', tr_tags)

    def table_body_cell(self, element, column, is_staff):
        field = column.get('field', None)
        try:
            value = element.__getattribute__(field)
        except:
            value = ''
        action = column.get('action', None)
        if action in self.common_actions:
            value = get_symbol(action)
        elif field in self.booleans:
            value = get_symbol('{}{}'.format('+' if value else '-', field))
        elif value:
            if column.get('datetime'):
                value = self._format_date(column, value)
            if column.get('appended_text'):
                value = self._append_text(column, value)
            value = self._append_text(column, value)
        if not (column.get('staff-only-action', False) and not is_staff) and action:
            value = get_tag('a', value, href=element._url(action, args=[element.pk]))
        return value if value else '-'
    
    def _format_date(self, column, value):
        if column.get('datetime') == 'past':
            minutes_ago = int((timezone.now() - value).total_seconds() / 60)
            if minutes_ago <= 120:
                return '{} Minute{} Ago'.format(minutes_ago, '' if minutes_ago == 1 else 's')
        return value.strftime("%A, %d. %B %Y %I:%M%p")
        
    def _append_text(self, column, value):
        return '{}{}'.format(value, column.get('appended_text', ''))