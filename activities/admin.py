"""Admin configuration for activities."""

from django.contrib import admin

from .models import Activity, ActivityMedia


class ActivityMediaInline(admin.TabularInline):
	model = ActivityMedia
	extra = 1
	fields = ('media_type', 'title', 'file', 'embed_url', 'caption', 'display_order')
	ordering = ('display_order',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
	list_display = ('title', 'event_date', 'location', 'status', 'is_featured')
	list_filter = ('status', 'is_featured', 'event_date', 'location')
	search_fields = ('title', 'location', 'summary')
	prepopulated_fields = {'slug': ('title',)}
	ordering = ('-event_date',)
	date_hierarchy = 'event_date'
	inlines = (ActivityMediaInline,)
