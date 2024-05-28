from django.contrib import admin
from django_yaml_field import YAMLField
from unfold.admin import ModelAdmin

from apps.bot_mgmt.models import Bot, BotConversationHistory
from django_ace import AceWidget


@admin.register(Bot)
class BotAdmin(ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name']
    list_filter = ['name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []


@admin.register(BotConversationHistory)
class BotConversationHistoryAdmin(ModelAdmin):
    list_display = ['bot', 'user', 'conversation_role', 'conversation', 'created_at']
    search_fields = ['conversation']
    list_filter = ['bot', 'user', 'conversation_role', 'created_at']
    list_display_links = ['conversation']
    ordering = ['id']
    filter_horizontal = []
