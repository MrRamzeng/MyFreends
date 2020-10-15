from allauth.account.decorators import verified_email_required
from django.urls import path

from user.views import UserDetailView

urlpatterns = [
    path(
        'my_profile/', verified_email_required(UserDetailView.as_view()),
        name='my_profile'
    ),
]
