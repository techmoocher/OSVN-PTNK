"""Views for listing and detailing chapter activities."""

from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Activity


def activity_list(request: HttpRequest) -> HttpResponse:
	"""Show upcoming and past activities."""

	today = timezone.now().date()
	published = Activity.objects.filter(status=Activity.Status.PUBLISHED)
	upcoming = published.filter(event_date__gte=today).order_by('event_date')
	past = published.filter(event_date__lt=today).order_by('-event_date')

	context = {
		'upcoming_activities': upcoming,
		'past_activities': past,
	}
	return render(request, 'activities/activity_list.html', context)


def activity_detail(request: HttpRequest, slug: str) -> HttpResponse:
	"""Display full details for a single activity."""

	activity = get_object_or_404(
		Activity.objects.prefetch_related('media_items'),
		slug=slug,
		status=Activity.Status.PUBLISHED,
	)
	media_items = activity.media_items.all()  # type: ignore[attr-defined]
	related = (
		Activity.objects.filter(status=Activity.Status.PUBLISHED)
		.exclude(pk=activity.pk)
		.order_by('-event_date')[:3]
	)

	context = {
		'activity': activity,
		'media_items': media_items,
		'related_activities': related,
	}
	return render(request, 'activities/activity_detail.html', context)
