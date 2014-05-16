from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class AuthorizedMixin(object):
    def dispatch(self, *args, **kwargs):

        return super(LoggedInMixin, self).dispatch(*args, **kwargs)