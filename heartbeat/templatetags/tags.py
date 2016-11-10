from django import template
from django.core.urlresolvers import reverse

register = template.Library()

OPTIONS = {
    'group': {
        'Red': {'symbol': 'empire', 'color': 'red'},
        'Blue': {'symbol': 'rebel', 'color': 'blue'},
        'White': {'symbol': 'first-order', 'color': 'grey'},
        'other': {'symbol': 'users'},
    },
    'status': {
        'true': {'symbol': 'heartbeat', 'color': 'green'},
        'false': {'symbol': 'ban', 'color': 'lightgrey'},
        'other': {},
    },
    'visible': {
        'true': {'symbol': 'check-square-o', 'color': 'blue'},
        'false': {'symbol': 'square-o', 'color': 'lightgrey'},
        'other': {},
    },
    'check-status': {
        'true': {'symbol': 'thumbs-o-up'},
        'false': {'symbol': 'thumbs-o-down'},
        'other': {},
    },
    'os': {
        'linux': {'symbol': 'linux'},
        'windows': {'symbol': 'windows'},
        'other': {'symbol': 'tv'},
    },
    'misc': {
        'delete': {'symbol': 'recycle', 'color': 'green'},
        'modify': {'symbol': 'cog', 'color': 'blue'},
        'clock': {'symbol': 'clock-o'},
        'other': {},
    },
}

@register.inclusion_tag('symbol.html')
def symbol(*args, **kwargs):
    category = kwargs.get('category', '')
    icon = kwargs.get('icon', '')
    color = kwargs.get('color', '')
    value = args[0] if len(args) else ''
    if category == 'team':
        icon = OPTIONS.get('group').get(str(value.group), 'other').get('symbol')
    else:
        value = str(value).lower()
        if value:
            if value in OPTIONS['misc']:
                category = 'misc'
            if category in OPTIONS:
                icon = OPTIONS[category].get(value, 'other').get('symbol', None)
                color = OPTIONS[category].get(value, 'other').get('color', None)
            else:
                icon = value
    extras = kwargs.get('extras', '')
    if 'no-fw' not in args:
        extras = str(extras) + ' fa-fw'
    try:
        url = reverse(kwargs.pop('url', None), args=[kwargs.pop('id', None)])
    except:
        url = ''
    data = {
        'icon': icon,
        'color': 'color:{}'.format(color),
        'extras': extras,
        'style': kwargs.pop('style', ''),
        'url': url,
    }
    return data
    
@register.filter
def append(value, arg):
    return '{}{}'.format(value, arg) if value else None
    