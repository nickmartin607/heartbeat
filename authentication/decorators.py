from django.http import Http404
from django.shortcuts import redirect
from functools import wraps

def has_permission(action=None, model=False):
    def decorator(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated():
                raise Http404("User is not authenticated")
            else:
                permitted = request.user.account.has_perm(
                    action,
                    model or kwargs.get('model') or args[0],
                    kwargs.get('id', None)
                )
                if not permitted:
                    raise Http404("User is not authorized")
            return function(request, *args, **kwargs)
        return wrapper
    return decorator
    