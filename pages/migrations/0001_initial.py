# Generated manually: initial migration for pages app
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('role', models.CharField(max_length=120)),
                (
                    'bio',
                    models.TextField(help_text='Short introduction shown on the Our Team page.'),
                ),
                ('photo', models.ImageField(blank=True, upload_to='team/photos/')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('instagram_url', models.URLField(blank=True)),
                ('facebook_url', models.URLField(blank=True)),
                ('linkedin_url', models.URLField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('display_order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Team member',
                'verbose_name_plural': 'Team members',
                'ordering': ['display_order', 'name'],
            },
        ),
    ]