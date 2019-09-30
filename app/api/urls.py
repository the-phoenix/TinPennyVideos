from django.urls import include, path
from rest_framework_jwt.views import (obtain_jwt_token,
                                      refresh_jwt_token,
                                      verify_jwt_token,)

urlpatterns = [
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),

    path('token-auth/', obtain_jwt_token, name='create-token'),
    path('token-refresh/', refresh_jwt_token, name='refresh-token'),
    path('token-verify/', verify_jwt_token, name='verify-token'),

    path('accounts/', include('accounts.urls')),
    path('media/', include('media.urls')),
]
