from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        if request.user.is_staff or request.user.is_superuser:
            path = '/admin/'
        else:
            path = '/account/{url}/'
            path = path.format(url=request.user.url)
        return path
