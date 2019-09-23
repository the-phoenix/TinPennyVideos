from django.urls import include, path
from rest_framework import routers

from .views import VideoViewSet

router = routers.DefaultRouter()

router.register(r'', VideoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
