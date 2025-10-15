"""URL routes for activity content."""

from django.urls import path

from . import views


app_name = 'activities'

urlpatterns = [
    path('', views.activity_list, name='list'),
    path('<slug:slug>/', views.activity_detail, name='detail'),
]