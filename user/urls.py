from allauth.account.decorators import verified_email_required
from django.urls import path
from user.views import AccountDetailView

urlpatterns = [
    path(
        '<slug:slug>/', verified_email_required(AccountDetailView.as_view()),
        name='account'
    ),
]
