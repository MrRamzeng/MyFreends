from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView

from friendship.models import Friend, FriendshipRequest, Block
from user.models import User

get_friendship_context_object_name = lambda: getattr(
    settings, 'FRIENDSHIP_CONTEXT_OBJECT_NAME', 'user'
)
get_friendship_context_object_list_name = lambda: getattr(
    settings, 'FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME', 'users'
)


@login_required(login_url='login')
def user_lists(request):
    return render(request, 'friendship/users/user_lists.html')


class ProfileDetailView(DetailView):
    template_name = 'friendship/users/profile_detail.html'

    def get_object(self):
        return User.objects.get(url=self.kwargs['url'])

    def get_context_data(self, **kwargs):
        user = User.objects.get(url=self.kwargs['url'])
        friend_list = Friend.objects.friends(user)
        try:
            sent_request = FriendshipRequest.objects.get(
                from_user=self.request.user, to_user=user
            )
        except FriendshipRequest.DoesNotExist:
            sent_request = None
        try:
            request_received = FriendshipRequest.objects.get(
                from_user=user, to_user=self.request.user
            )
        except FriendshipRequest.DoesNotExist:
            request_received = None
        friend_counter = Friend.objects.filter(from_user=user).count()
        context = {
            'user': user, 'friend_list': friend_list, 'sent_request': sent_request,
            'request_received': request_received, 'friend_counter': friend_counter,
            'userPage': 'userPage'
        }
        return context


@login_required
def add_friend(request, url):
    other_user = User.objects.get(url=url)
    Friend.objects.add_friend(request.user, other_user)
    return redirect('user_lists')


@login_required
def cancel_request(request, url):
    FriendshipRequest.objects.get(
        from_user=request.user, to_user=User.objects.get(url=url)
    ).delete()
    return redirect('user_lists')


@login_required
def accept_friend_request(request, url):
    other_user = User.objects.get(url=url)
    FriendshipRequest.objects.get(
        to_user=request.user, from_user=other_user
    ).accept()
    return redirect('user_lists')


@login_required
def reject_friend_request(request, url):
    other_user = User.objects.get(url=url)
    FriendshipRequest.objects.get(
        to_user=request.user, from_user=other_user
    ).reject()
    return redirect('user_lists')


@login_required
def remove_friend(request, url):
    other_user = User.objects.get(url=url)
    Friend.objects.remove_friend(request.user, other_user)
    return redirect('user_lists')


def add_block(request, url):
    other_user = User.objects.get(url=url)
    Block.objects.add_block(request.user, other_user)
    try:
        FriendshipRequest.objects.get(
            to_user=request.user, from_user=User.objects.get(url=url)
        ).delete()
    except FriendshipRequest.DoesNotExist:
        pass
    return redirect('user_lists')


def remove_block(request, url):
    Block.objects.remove_block(request.user, User.objects.get(url=url))
    return redirect('user_lists')
