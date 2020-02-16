from django.urls import path

from . import views

urlpatterns = [
    path('train/', views.train_Model),
    path('checkStatus/', views.check_TrainingStatus),
]