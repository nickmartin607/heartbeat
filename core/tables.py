import collections, datetime, urllib
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.utils import timezone
from core.html import get_tag, get_symbol

class Table:
    def __init__(self, *args, **kwargs):
        self.header = []
        self.body = []
        self.title = kwargs.pop('title', '')
        self.elements = kwargs.pop('elements', [])
        if not self.elements:
            self.title = "No items exist."
        
    def sort(self, order_by):
        self.elements = self.elements.order_by(Lower(order_by.strip('-')))
        if order_by.startswith('-'):
            self.elements = self.elements.reverse()
    
    def build(self, request):
        for column in self.columns:
            perm = column.get('permission', None)
            if request.user.account.has_perm(perm, self.model)[0]:
                self.header.append(self.build_header_cell(column, request.GET.copy()))
        for element in self.elements:
            row = []
            for column in self.columns:
                perm = column.get('permission', None)
                if request.user.account.has_perm(perm, self.model, id=element.pk)[0]:
                    value = self.build_body_cell(column, element)
                    row.append(value)
            if len(row):
                self.body.append(row)
                    
    def build_header_cell(self, column, request):
        field = column.get('field', None)
        common_action = column.get('common_action', None)
        if field:
            label = self.model._fieldname(field)
        elif common_action:
            field = common_action
            label = common_action.capitalize()
        if column.get('sort', True) and not common_action:
            symbol = ''
            new_sort = '-{}'.format(field)
            old_sort = request.get('order_by', None)
            if old_sort:
                if old_sort == new_sort:
                    new_sort = field
                    symbol = get_symbol('desc')
                elif old_sort.lstrip('-') == field:
                    symbol = get_symbol('asc')
            request['order_by'] = new_sort
            items = collections.OrderedDict(sorted(request.items()))
            href = '?{}'.format(urllib.parse.urlencode(items))
            label = '{}{}'.format(get_tag('a', label, href=href), symbol)
        styles = column.get('styles', [])
        if common_action:
            styles.append('narrow')
        return get_tag('th', label, css_class=' '.join(styles))
            
    def build_body_cell(self, column, element):
        field = column.get('field', None)
        common_action = column.get('common_action', None)
        action = column.get('action', common_action)
        if common_action:
            value = get_symbol(common_action)
        else:
            try:
                value = element.__getattribute__(field)
            except:
                return '-'
            if isinstance(value, bool):
                value = get_symbol('{}{}'.format('+' if value else '-', field))
            else:
                if column.get('datetime', False) and value:
                    if column.get('datetime') == 'past':
                        minutes_ago = int((timezone.now() - value).total_seconds() / 60)
                        if minutes_ago <= 120:
                            value = '{} Minute{} Ago'.format(minutes_ago, '' if minutes_ago == 1 else 's')
                        else:
                            value = value.strftime("%A, %d. %B %Y %I:%M%p")
                    else:
                        value = value.strftime("%A, %d. %B %Y %I:%M%p")
                if column.get('appended_text'):
                    value = '{}{}'.format(value, column.get('appended_text', ''))
        if action:
            href = element._url(action, args=[element.pk])
            label = get_tag('a', value, href=href)
        else:
            label = str(value)
        styles = column.get('styles', [])
        if common_action:
            styles.append('narrow')
        return get_tag('td', label, css_class=' '.join(styles))
