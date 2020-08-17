from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from user.models import Account


class EmailInlines(admin.TabularInline):
    model = EmailAddress
    readonly_fields = ('email', 'verified', 'primary')

    def has_delete_permission(self, request, obj):
        return False

    def has_add_permission(self, request, obj):
        return False


@admin.register(Account)
class CustomAdmin(UserAdmin):
    model = Account
    list_display = (
        'get_image', 'first_name', 'last_name', 'birthday', 'email', 'url',
        'is_staff'
    )
    list_editable = ('url', 'is_staff')
    readonly_fields = ('get_image', 'first_name', 'last_name', 'birthday')
    ordering = ('is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    inlines = [EmailInlines]
    # list_display_links = None
    fieldsets = (
        (
            'Об учетной записи', {
                'fields': (
                    ('get_image',),
                    ('first_name', 'email', 'last_name', 'birthday')
                )
            }
        ),
        (
            None, {
                'fields': ('url',)
            }
        ),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="250" height="auto">')

    get_image.short_description = 'Изображение профиля'
