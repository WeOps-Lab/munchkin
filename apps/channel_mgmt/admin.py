from django.contrib import admin
from django_ace import AceWidget
from django_yaml_field import YAMLField
from unfold.admin import ModelAdmin

from apps.channel_mgmt.models import Channel, ChannelUserGroup, ChannelUser


@admin.register(Channel)
class ChannelAdmin(ModelAdmin):
    list_display = ['channel_type', 'name']
    search_fields = ['name']
    list_filter = ['channel_type', 'name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []

    formfield_overrides = {YAMLField: {
        "widget": AceWidget(mode="yaml", theme='chrome', width='700px')}
    }


@admin.register(ChannelUserGroup)
class ChannelUserGroupAdmin(ModelAdmin):
    list_display = ['channel', 'name']
    search_fields = ['name']
    list_filter = ['name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []


@admin.register(ChannelUser)
class ChannelUserAdmin(ModelAdmin):
    list_display = ['channel_user_group', 'user_id', 'name']
    search_fields = ['name']
    list_filter = ['name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
