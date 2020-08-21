from django.shortcuts import redirect, render

from user.forms import AccountImageForm


def account(request, url):
    if request.method == 'POST':
        form = AccountImageForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect('account', url)
    else:
        form = AccountImageForm()
    context = {'form': form, 'account': 'account'}
    return render(
        request, 'user/account_detail.html', context=context
    )
