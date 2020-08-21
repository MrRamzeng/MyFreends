from allauth.account.views import login
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('user.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include('allauth.urls')),
    path('', login, name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
