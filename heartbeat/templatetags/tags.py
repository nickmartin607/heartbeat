from django import template
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def is_active(request, current_url):
    return 'active' if request.path == reverse(current_url) else ''
    
@register.simple_tag
def team_color(group):
    group = str(group).lower()
    return group if group in ['red', 'blue'] else 'grey'
        
@register.simple_tag
def team_icon(group):
    group = str(group).lower()
    if 'red' in group:
        return 'empire'
    elif 'blue' in group:
        return 'rebel'
    else:
        return 'first-order'