from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string

from user.managers import CustomStaffManager


def account_image(instance, filename):
    return '%s/image/%s' % (instance.url, filename)


class Account(AbstractBaseUser, PermissionsMixin):
    url = models.SlugField('url', max_length=20, unique=True)
    email = models.EmailField(
        'Адрес электронной почты', max_length=254, unique=True
    )
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    birthday = models.DateField('Дата рождения')
    image = models.ImageField(
        'Фото', upload_to=account_image, default='default.png'
    )
    objects = CustomStaffManager()
    is_staff = models.BooleanField('Персонал', default=False)
    is_superuser = models.BooleanField('Админ', default=False)
    is_close = models.BooleanField('Закрытый', default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'url', 'birthday')

    def save(self, *args, **kwargs):
        if self.url == '':
            self.url = get_random_string(6)
        super(Account, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('account', args=(self.url, ))

    class Meta:
        verbose_name = 'Учетная запись'
        verbose_name_plural = 'Учетные записи'
