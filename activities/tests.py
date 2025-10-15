"""Tests for activities models and views."""

from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from .models import Activity


class ActivityModelTests(TestCase):
    def test_slug_auto_generated_and_unique(self) -> None:
        first = Activity.objects.create(
            title='Operation Smile Mission',
            summary='Supporting cleft surgeries in central Vietnam.',
            location='Da Nang',
            event_date=date.today(),
            body='A day full of impactful surgeries and family support.',
            status=Activity.Status.PUBLISHED,
        )
        second = Activity.objects.create(
            title='Operation Smile Mission',
            summary='A follow-up outreach trip.',
            location='Da Nang',
            event_date=date.today() + timedelta(days=30),
            body='Continuing patient care with alumni volunteers.',
            status=Activity.Status.PUBLISHED,
        )

        self.assertEqual(first.slug, 'operation-smile-mission')
        self.assertNotEqual(first.slug, second.slug)
        self.assertTrue(second.slug.startswith('operation-smile-mission'))


class ActivityViewsTests(TestCase):
    def setUp(self) -> None:
        today = date.today()
        self.upcoming = Activity.objects.create(
            title='Upcoming Mission',
            summary='We are recruiting volunteers for the next trip.',
            location='Hue',
            event_date=today + timedelta(days=10),
            body='Details about the upcoming mission.',
            status=Activity.Status.PUBLISHED,
        )
        self.past = Activity.objects.create(
            title='Past Mission',
            summary='Celebrating successful surgeries.',
            location='Ho Chi Minh City',
            event_date=today - timedelta(days=20),
            body='Reflection on the impact we delivered.',
            status=Activity.Status.PUBLISHED,
        )

    def test_activity_list_renders_published_items(self) -> None:
        response = self.client.get(reverse('activities:list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.upcoming.title)
        self.assertContains(response, self.past.title)

    def test_activity_detail_renders_content(self) -> None:
        response = self.client.get(self.upcoming.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.upcoming.title)
        self.assertContains(response, self.upcoming.location)