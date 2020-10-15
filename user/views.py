from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import DetailView

from user.forms import UserImageForm
from user.models import User


class UserDetailView(DetailView):
    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)

    def get_context_data(self, **kwargs):
        if self.request.method == 'POST':
            form = UserImageForm(
                self.request.POST, self.request.FILES,
                instance=self.request.user
            )
            if form.is_valid():
                form.save()
                return redirect('my_profile')
        else:
            form = UserImageForm()
        context = {'form': form, 'userPage': True}
        return context
