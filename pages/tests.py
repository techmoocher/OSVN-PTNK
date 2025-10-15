"""Tests for core site pages."""

from django.test import TestCase
from django.urls import reverse

from activities.models import Activity
from .models import TeamMember


class PageViewTests(TestCase):
    def setUp(self) -> None:
        Activity.objects.create(
            title='Sample Activity',
            summary='Summary for homepage testing.',
            location='Ho Chi Minh City',
            event_date='2025-03-20',
            body='Body content',
            status=Activity.Status.PUBLISHED,
        )
        TeamMember.objects.create(
            name='Student Leader',
            role='President',
            bio='Leads fundraising and mission coordination.',
        )

    def test_homepage_renders(self) -> None:
        response = self.client.get(reverse('pages:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Operation Smile PTNK')

    def test_about_page_renders(self) -> None:
        response = self.client.get(reverse('pages:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Our mission')

    def test_join_page_renders(self) -> None:
        response = self.client.get(reverse('pages:join'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Join Operation Smile PTNK')

    def test_team_page_lists_members(self) -> None:
        response = self.client.get(reverse('pages:team'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student Leader')


class TeamMemberModelTests(TestCase):
    def test_social_links_bundles_available_links(self) -> None:
        member = TeamMember.objects.create(
            name='Volunteer',
            role='Coordinator',
            bio='Coordinates volunteers for missions.',
            instagram_url='https://instagram.com/example',
            facebook_url='https://facebook.com/example',
        )

        labels = [label for label, _ in member.social_links()]
        self.assertEqual(labels, ['Instagram', 'Facebook'])