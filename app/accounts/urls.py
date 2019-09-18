from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.UserListView.as_view()),
    # path('login/', LoginView.as_view(), name="auth-login"),
    # path('register/', RegisterUserView.as_view(), name="auth-register"),
    # path(r'', include('rest_auth.urls')),
    # path(r'registration/', include('rest_auth.registration.urls')),
]