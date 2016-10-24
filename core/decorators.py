import functools
from django.shortcuts import render, redirect

def has_permission(action=None, _model=None):
    def _has_permission(function):
        @functools.wraps(function)
        def _check_perms(request, *args, **kwargs):
            model = _model or kwargs.get('model') or args[0]
            perm = '{}.{}_{}'.format(model._appname(), action, model._modelname())
            print("Permission Requested by {}[{}]: {}".format(request.user, request.user.account._team(), perm))
            
            print("  Authenticated?")
            if not request.user.is_authenticated:
                print("    Nope...")
                return redirect('login')
            print("    Yes!")
            
            print("  Has Permission?")
            if not request.user.has_perm(perm):
                print("  Nope...")
                return redirect('401')
            print("    Yes!")
            
            try:
                instance = model.objects.get(pk=kwargs.get('id'))
                print("  Can View?")
                can_view = instance.can_view(request.user)
                is_staff = request.user.is_staff
                if not can_view and not is_staff:
                    print("  Nope...")
                    return redirect('404')
            except:
                pass
            print("    Yes!")
            
            print("  Granted!")
            return function(request, *args, **kwargs)
        return _check_perms
    return _has_permission
    