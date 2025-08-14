from django.http import HttpResponseRedirect


def login_required(function):
    def wrap(request, *args, **kwargs):
        user = request.session.get("user")
        if user is not None:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(f"/login/?next={request.get_full_path()}")

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
