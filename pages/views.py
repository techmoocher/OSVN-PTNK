"""Page views for the public site."""

from __future__ import annotations
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from activities.models import Activity
from .models import TeamMember

def home(request: HttpRequest) -> HttpResponse:
	"""Landing page with highlights, upcoming events, and calls to action."""

	today = timezone.now().date()
	published_activities = Activity.objects.filter(status=Activity.Status.PUBLISHED)
	featured_activities = published_activities.filter(is_featured=True)[:3]
	upcoming_activities = published_activities.filter(event_date__gte=today).order_by('event_date')[:3]
	recent_activities = published_activities.filter(event_date__lt=today).order_by('-event_date')[:3]
	spotlight_members = TeamMember.objects.filter(is_active=True)[:4]
	context = {
		'featured_activities': featured_activities,
		'upcoming_activities': upcoming_activities,
		'recent_activities': recent_activities,
		'spotlight_members': spotlight_members,
	}
	return render(request, 'pages/home.html', context)

def about(request: HttpRequest) -> HttpResponse:
	"""Share the chapter's story, mission, and impact metrics."""

	total_members = TeamMember.objects.filter(is_active=True).count()
	total_activities = Activity.objects.filter(status=Activity.Status.PUBLISHED).count()
	context = {
		'total_members': total_members,
		'total_activities': total_activities,
	}
	return render(request, 'pages/about.html', context)
def donate(request: HttpRequest) -> HttpResponse:
	"""Placeholder page until online donations launch."""

	return render(request, 'pages/donate.html')
def join_us(request: HttpRequest) -> HttpResponse:
	"""Recruit new volunteers and route them to the Google Form."""

	context = {
		'join_form_url': settings.JOIN_US_GOOGLE_FORM_URL,
	}
	return render(request, 'pages/join.html', context)
def team(request: HttpRequest) -> HttpResponse:
	"""Introduce the members supporting Operation Smile PTNK."""

	members = TeamMember.objects.filter(is_active=True)
	return render(request, 'pages/team.html', {'members': members})

def custom_404(request: HttpRequest, exception: Exception) -> HttpResponse:  # pragma: no cover
	"""Custom 404 view that keeps branding consistent when pages are missing."""

	return render(request, '404.html', status=404)
