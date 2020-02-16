from django.urls import path
from django.conf.urls import url
from rest_framework import routers
from django.conf.urls import include
from .views import classifyImage

# router = routers.DefaultRouter()
# router.register('projects', ProjectViewSet)
# router.register('videos', VideoViewSet)
# router.register('images', ImageViewSet)

urlpatterns = [
    path('', classifyImage.as_view(), name='classifyImage'),
]