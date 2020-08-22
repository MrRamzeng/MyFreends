from allauth.account.decorators import verified_email_required
from django.urls import path
from user.views import user

urlpatterns = [
    path('<slug:url>/', verified_email_required(user), name='user'),
]
