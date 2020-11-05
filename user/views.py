from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView
from django.views.generic.base import View

from user.forms import UserImageForm
from user.models import User
from chat.models import Message


class UserDetailView(DetailView):
    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)

    def get_context_data(self, **kwargs):
        unread_counter = Message.objects.filter(
            chat__user_list=self.request.user, is_read=False
        ).exclude(author=self.request.user).count()
        context = {'userPage': True, 'unread_counter': unread_counter}
        return context


class UpdateImage(View):
    def post(self, request):
        form = UserImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
