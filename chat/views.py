from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse

from chat.models import Chat, MessageImage, MessageSmile


@login_required(login_url='login')
def chat(request):
    chats = Chat.objects.filter(user_list=request.user)
    smiles = MessageSmile.objects.all()
    return render(request, 'chat/chat.html', {
        'chats': chats, 'smiles': smiles
    })


@login_required(login_url='login')
def upload_image(request):
    if request.method == 'POST' and request.FILES['img']:
        image = MessageImage(img=request.FILES['img'])
        image.save()
        return JsonResponse({'success': True, 'id': image.id})
    return JsonResponse({'success': False, 'message': 'no file'})
