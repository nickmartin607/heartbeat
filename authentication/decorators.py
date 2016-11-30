from django.shortcuts import redirect
from functools import wraps


def has_permission(action=None, model=None):
    def decorator(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated():
                (permitted, error_code) = request.user.account.has_perm(
                    action,
                    model or kwargs.get('model') or args[0],
                    kwargs.get('id', None)
                )
                if not permitted:
                    return redirect(str(error_code))
            else:
                return redirect('404')
            return function(request, *args, **kwargs)
        return wrapper
    return decorator
    