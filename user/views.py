from allauth.account.decorators import verified_email_required
from django.shortcuts import render
from django.views.generic import DetailView

from user.models import Account


class AccountDetailView(DetailView):
    model = Account
    slug_field = 'url'
