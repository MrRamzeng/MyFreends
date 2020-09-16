from django import template
from django.db.models import Q

from friendship.models import Friend, Block
from user.models import User

register = template.Library()


@register.simple_tag(takes_context=True)
def get_by_name(context, name):
    return context[name]


@register.inclusion_tag('templatetags/friend_list.html')
def friends(user):
    return {'friend_list': Friend.objects.friends(user)}


@register.inclusion_tag('templatetags/sent_requests.html')
def user_sent_requests(user):
    return {'sent_requests': Friend.objects.sent_requests(user)}


@register.inclusion_tag('templatetags/requests_received.html')
def user_requests_received(user):
    return {'requests_received': Friend.objects.requests_received(user)}


@register.inclusion_tag('templatetags/user_list.html')
def users(user):
    friend_list = Friend.objects.friends(user)
    sent_requests = [u.to_user.id for u in Friend.objects.sent_requests(user)]
    requests_received = [
        u.from_user.id for u in Friend.objects.requests_received(user)
    ]
    blocking = [u.blocked.id for u in Block.objects.filter(blocker=user)]
    user_list = User.objects.exclude(
        Q(id=user.id) | Q(email__in=friend_list) | Q(id__in=sent_requests) |
        Q(id__in=requests_received) | Q(id__in=blocking)
    )
    return {
        'user_list': user_list
    }
