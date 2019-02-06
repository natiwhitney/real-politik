from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/<user>/', views.load_user, name='load_user'),
]
