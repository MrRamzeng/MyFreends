from allauth.account.decorators import verified_email_required
from django.urls import path

from user.views import UserDetailView, UpdateImage

urlpatterns = [
    path(
        'my_profile/', verified_email_required(UserDetailView.as_view()),
        name='my_profile'
    ),
    path(
        'update_image/', verified_email_required(UpdateImage.as_view()),
        name='update_image'
    )
]
