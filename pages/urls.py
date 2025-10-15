"""URL patterns for the core site pages."""

from django.urls import path

from . import views


app_name = 'pages'

urlpatterns = [
	path('', views.home, name='home'),
	path('about/', views.about, name='about'),
	path('donate/', views.donate, name='donate'),
	path('join/', views.join_us, name='join'),
	path('team/', views.team, name='team'),
]
