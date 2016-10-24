from django import template
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def is_active(request, current_url):
    return 'active' if request.path == reverse(current_url) else ''
    
@register.simple_tag
def user_group(id):
    try:
        group = User.objects.get(pk=id).groups.all()[0].name
    except:
        group = ''
    return group