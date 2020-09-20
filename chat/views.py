from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse

from user.models import User
from chat.models import Chat, MessageImage, MessageSmile
from chat.forms import ChatForm
from friendship.models import Friend
from django.db.models import Q


@login_required(login_url='login')
def chat(request):
    chats = Chat.objects.filter(user_list=request.user)
    smiles = MessageSmile.objects.all()
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save()
            return render(request, 'chat/chat-list-item.html', {
                'chat': chat
            })
    else:
        friends = Friend.objects.filter(
            from_user=request.user
        ).values('to_user_id')
        users = User.objects.filter(Q(id=request.user.id) | Q(id__in=friends))
        form = ChatForm(initial={'user_list': request.user})
        form.fields['user_list'].queryset = users
    return render(request, 'chat/chat.html', {
        'chats': chats, 'form': form, 'smiles': smiles
    })


@login_required(login_url='login')
def upload_image(request):
    if request.method == 'POST' and request.FILES['img']:
        image = MessageImage(img=request.FILES['img'])
        image.save()
        return JsonResponse({'success': True, 'id': image.id})
    return JsonResponse({'success': False, 'message': 'no file'})
