from django.urls import path, re_path
from chat.views import chat, upload_image

urlpatterns = [
    path('chat/', chat, name='chat'),
    path('chat/up_image/', upload_image, name='upload'),
]
