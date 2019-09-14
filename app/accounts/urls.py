from django.urls import path, include
from .views import LoginView, RegisterUserView

urlpatterns = [
    # path('login/', LoginView.as_view(), name="auth-login"),
    # path('register/', RegisterUserView.as_view(), name="auth-register"),
    path(r'', include('rest_auth.urls')),
    path(r'registration/', include('rest_auth.registration.urls')),
]