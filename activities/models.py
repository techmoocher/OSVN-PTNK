"""Models for Operation Smile PTNK activities."""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class ActivityQuerySet(models.QuerySet):
    """Custom queryset helpers for activities."""

    def published(self) -> 'ActivityQuerySet':
        return self.filter(status=Activity.Status.PUBLISHED)

    def upcoming(self) -> 'ActivityQuerySet':
        today = timezone.now().date()
        return self.published().filter(event_date__gte=today).order_by('event_date')

    def past(self) -> 'ActivityQuerySet':
        today = timezone.now().date()
        return self.published().filter(event_date__lt=today).order_by('-event_date')


class Activity(models.Model):
    """A charity trip or event organised by the chapter."""

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    title = models.CharField(max_length=200)
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text="Auto-generated from the title if left blank.",
    )
    summary = models.CharField(
        max_length=300,
        help_text="Short teaser shown on cards and social previews.",
    )
    location = models.CharField(max_length=150)
    event_date = models.DateField()
    cover_image = models.ImageField(upload_to='activities/covers/', blank=True)
    cover_image_alt = models.CharField(
        max_length=160,
        blank=True,
        help_text="Accessible description for the cover image.",
    )
    body = models.TextField(help_text="Full recap or plan for the activity.")
    donation_url = models.URLField(blank=True)
    registration_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.PUBLISHED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ActivityQuerySet.as_manager()

    class Meta:
        ordering = ['-event_date', '-created_at']
        verbose_name_plural = 'Activities'

    def __str__(self) -> str:
        return self.title

    def clean(self) -> None:
        if self.registration_url and not self.registration_url.startswith(('http://', 'https://')):
            raise ValidationError({'registration_url': 'Registration URL must start with http:// or https://.'})
        if self.donation_url and not self.donation_url.startswith(('http://', 'https://')):
            raise ValidationError({'donation_url': 'Donation URL must start with http:// or https://.'})

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            base_slug = slugify(self.title) or 'activity'
            unique_slug = base_slug
            counter = 1
            model = self.__class__
            while model.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('activities:detail', args=[self.slug])

    @property
    def is_published(self) -> bool:
        return self.status == self.Status.PUBLISHED


class ActivityMedia(models.Model):
    """Supplementary media (photos, videos, docs) for an activity."""

    class MediaType(models.TextChoices):
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Video'
        DOCUMENT = 'document', 'Document'

    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='media_items',
    )
    media_type = models.CharField(max_length=10, choices=MediaType.choices)
    title = models.CharField(max_length=150, blank=True)
    caption = models.TextField(blank=True)
    file = models.FileField(upload_to='activities/media/', blank=True)
    embed_url = models.URLField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = 'Activity media item'
        verbose_name_plural = 'Activity media items'

    def __str__(self) -> str:
        display = self.get_media_type_display()  # type: ignore[attr-defined]
        return f"{display} - {self.title or self.activity.title}"

    def clean(self) -> None:
        if not self.file and not self.embed_url:
            raise ValidationError('Provide either a file upload or an external embed URL.')
        if self.file and self.embed_url:
            raise ValidationError('Choose a file upload or an embed URL, not both.')