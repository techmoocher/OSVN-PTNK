"""Content models for the informational pages."""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models


class TeamMember(models.Model):
    """Represents a student leader or volunteer on the chapter team."""

    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    bio = models.TextField(help_text="Short introduction shown on the Our Team page.")
    photo = models.ImageField(upload_to='team/photos/', blank=True)
    email = models.EmailField(blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Team member'
        verbose_name_plural = 'Team members'

    def __str__(self) -> str:
        return f"{self.name} — {self.role}"

    def clean(self) -> None:
        social_fields = {
            'instagram_url': self.instagram_url,
            'facebook_url': self.facebook_url,
            'linkedin_url': self.linkedin_url,
        }
        for field, value in social_fields.items():
            if value and not value.startswith(('http://', 'https://')):
                raise ValidationError({field: 'Links must start with http:// or https://.'})

    def social_links(self) -> list[tuple[str, str]]:
        """Return a list of label/url pairs for template loops."""
        links: list[tuple[str, str]] = []
        if self.instagram_url:
            links.append(('Instagram', self.instagram_url))
        if self.facebook_url:
            links.append(('Facebook', self.facebook_url))
        if self.linkedin_url:
            links.append(('LinkedIn', self.linkedin_url))
        return links
