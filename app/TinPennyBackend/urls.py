"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path, reverse_lazy
from django.views.generic.base import RedirectView

from rest_framework_jwt.views import (obtain_jwt_token,
                                      refresh_jwt_token,
                                      verify_jwt_token,)

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello_world', views.HelloWorld.as_view()),
    path('api-token-auth/', obtain_jwt_token, name='create-token'),
    path('api-token-refresh/', refresh_jwt_token, name='refresh-token'),
    path('api-token-verify/', verify_jwt_token, name='verify-token'),
    # API Explorer auth endpoints
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    re_path('api/(?P<version>(v1|v2))/accounts/', include('accounts.urls'))

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    # re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),
]

# Change Admin Title
admin.site.site_header = "TinPenny Backend Office"
admin.site.site_title = "TinPenny Backend Office"
