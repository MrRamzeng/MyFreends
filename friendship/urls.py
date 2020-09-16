from django.urls import path
from friendship.views import (
    user_lists, add_friend, cancel_request, accept_friend_request,
    reject_friend_request, remove_friend, add_block, remove_block, view_profile
)

urlpatterns = [
    path('users/', user_lists, name='user_lists'),
    path('add_friend/<str:url>/', add_friend, name='add_friend'),
    path('cancel_request/<str:url>/', cancel_request, name='cancel_request'),
    path(
        'accept_friend_request/<str:url>/', accept_friend_request,
        name='accept_friend_request'
    ),
    path(
        'reject_friend_request/<str:url>/', reject_friend_request,
        name='reject_friend_request'
    ),
    path('remove_friend/<str:url>/', remove_friend, name='remove_friend'),
    path('add_block/<str:url>/', add_block, name='add_block'),
    path('remove_block/<str:url>/', remove_block, name='remove_block'),
    path('profile/<str:url>/', view_profile, name='view_profile'),
]
