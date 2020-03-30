from django.urls import include, path
from rest_framework import routers

from .views import VideoViewSet, CategoryViewSet, StreamViewSet

router = routers.DefaultRouter()

router.register(r'videos', VideoViewSet, basename='video')
router.register(r'categories', CategoryViewSet)
router.register(r'streams', StreamViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
