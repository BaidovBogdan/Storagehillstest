from django.contrib import admin
from django.urls import path, include, re_path
from control.views import react_app
from django.conf.urls.static import static
from django.conf import settings
react_views_regex = r'\/|\b'.join([

    # List all your react routes here
      'login',
      'registration',
      'payment',
      'requisites',
      'currentBalance',
      'workspace',

]) + r'\/'



urlpatterns = [
    path('', react_app, name='react_app'),
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls')),
    path('api_V1/', include('control.urls')),   
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(react_views_regex, react_app),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
