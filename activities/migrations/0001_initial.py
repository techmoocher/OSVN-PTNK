# Generated manually: initial migration for activities app
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                (
                    'slug',
                    models.SlugField(
                        blank=True,
                        help_text='Auto-generated from the title if left blank.',
                        unique=True,
                    ),
                ),
                (
                    'summary',
                    models.CharField(
                        help_text='Short teaser shown on cards and social previews.',
                        max_length=300,
                    ),
                ),
                ('location', models.CharField(max_length=150)),
                ('event_date', models.DateField()),
                ('cover_image', models.ImageField(blank=True, upload_to='activities/covers/')),
                (
                    'cover_image_alt',
                    models.CharField(
                        blank=True,
                        help_text='Accessible description for the cover image.',
                        max_length=160,
                    ),
                ),
                ('body', models.TextField(help_text='Full recap or plan for the activity.')),
                ('donation_url', models.URLField(blank=True)),
                ('registration_url', models.URLField(blank=True)),
                ('is_featured', models.BooleanField(default=False)),
                (
                    'status',
                    models.CharField(
                        choices=[('draft', 'Draft'), ('published', 'Published')],
                        default='published',
                        max_length=12,
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Activities',
                'ordering': ['-event_date', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ActivityMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'media_type',
                    models.CharField(
                        choices=[('image', 'Image'), ('video', 'Video'), ('document', 'Document')],
                        max_length=10,
                    ),
                ),
                ('title', models.CharField(blank=True, max_length=150)),
                ('caption', models.TextField(blank=True)),
                ('file', models.FileField(blank=True, upload_to='activities/media/')),
                ('embed_url', models.URLField(blank=True)),
                ('display_order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'activity',
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name='media_items',
                        to='activities.activity',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Activity media item',
                'verbose_name_plural': 'Activity media items',
                'ordering': ['display_order', 'id'],
            },
        ),
    ]
