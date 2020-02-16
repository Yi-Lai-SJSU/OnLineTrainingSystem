from django.urls import path
from django.conf.urls import url
from rest_framework import routers
from django.conf.urls import include
from videoToFrames.views import videoToFrames
from .views import ProjectViewSet
from .views import VideoViewSet
from .views import ImageViewSet

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet)
router.register('videos', VideoViewSet)
router.register('images', ImageViewSet)

urlpatterns = [
    path('', videoToFrames.as_view(), name='videoToFrames'),
    path('testing/', include(router.urls)),
]