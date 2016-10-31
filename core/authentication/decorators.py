import functools
from django.shortcuts import render, redirect

def has_permission(action=None, model=None):                                    # removed underscore before model
    def decorator(function):
        @functools.wraps(function)
        def wrapper(request, *args, **kwargs):
            (permitted, error) = request.user.account.has_perm(
                action,
                model = model or kwargs.get('model') or args[0],                # removed underscore before model
                id = kwargs.get('id', None)
            )
            if not permitted:
                return redirect(error)
            return function(request, *args, **kwargs)
        return wrapper
    return decorator
    