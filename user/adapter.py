from allauth.account.adapter import DefaultAccountAdapter


class UserAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        path = '/my_profile/'
        return path.format(url=request.user.url)
