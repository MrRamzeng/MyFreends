from django import forms 
from chat.models import Chat
from account.models import Account
from django.forms import ModelMultipleChoiceField


class AccountsChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        img = '<img src="{url}" class="circle">'.format(url=obj.photo.url)
        full_name = '<span>{first_name} {last_name}</span>'.format(first_name=obj.first_name, last_name=obj.last_name)
        return "{photo} {full_name}".format(full_name=full_name, photo=img)


class ChatForm(forms.ModelForm):
    name = forms.CharField(max_length=20, label='chat name')
    user_list = AccountsChoiceField(widget=forms.CheckboxSelectMultiple, required=True, queryset=Account.objects.all())
    class Meta:
        model = Chat
        exclude = ()
