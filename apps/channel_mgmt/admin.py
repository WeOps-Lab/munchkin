from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.channel_mgmt.models import Channel


@admin.register(Channel)
class ChannelAdmin(ModelAdmin):
    list_display = ['channel_type', 'name']
    search_fields = ['name']
    list_filter = ['name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
