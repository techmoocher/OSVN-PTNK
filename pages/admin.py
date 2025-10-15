"""Admin configuration for static content models."""

from django.contrib import admin

from .models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('name', 'role', 'bio')
    ordering = ('display_order', 'name')
    readonly_fields = ('created_at', 'updated_at')
