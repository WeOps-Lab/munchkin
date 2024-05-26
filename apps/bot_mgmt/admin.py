from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.bot_mgmt.models import Bot, BotSkill, BotSkillRule


@admin.register(Bot)
class BotAdmin(ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name']
    list_filter = ['name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []


@admin.register(BotSkill)
class BotSkillAdmin(ModelAdmin):
    list_display = ['bot', 'name', 'skill_id']
    search_fields = ['name']
    list_filter = ['name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []


@admin.register(BotSkillRule)
class BotSkillRuleAdmin(ModelAdmin):
    list_display = ['name', 'bot_name', 'bot_skill']
    search_fields = ['name']
    list_filter = ['name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []

    def bot_name(self, obj):
        return obj.bot_skill.bot.name

    bot_name.short_description = '机器人'
