from django.shortcuts import redirect, render

from user.forms import UserImageForm
from user.models import User


def user(request, url):
    if request.method == 'POST':
        form = UserImageForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect('user', url)
    else:
        form = UserImageForm()
    context = {'form': form, 'userPage': True}
    return render(request, 'user/user_detail.html', context)
