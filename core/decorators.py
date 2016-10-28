import functools
from django.shortcuts import render, redirect

def has_permission(action=None, _model=None):
    def _has_permission(function):
        @functools.wraps(function)
        def _check_perms(request, *args, **kwargs):
            (permitted, error) = request.user.account.has_perm(
                action,
                model = _model or kwargs.get('model') or args[0],
                id = kwargs.get('id', None)
            )
            if not permitted:
                return redirect(error)
            return function(request, *args, **kwargs)
        return _check_perms
    return _has_permission
    