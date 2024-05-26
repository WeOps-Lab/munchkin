from django.contrib import admin
from django_ace import AceWidget
from django_yaml_field import YAMLField
from unfold.admin import ModelAdmin

from apps.contentpack_mgmt.models import BotActions, BotActionRule, RasaEntity, Intent, IntentCorpus, RasaRules, \
    RasaStories, RasaResponse, RasaResponseCorpus, RasaForms, RasaSlots, ContentPack, RasaModel


@admin.register(BotActions)
class BotActionsAdmin(ModelAdmin):
    list_display = ['content_pack', 'name']
    search_fields = ['name']
    list_filter = ['content_pack', 'name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []


class BotActionsStackedInline(admin.StackedInline):
    model = BotActions


@admin.register(BotActionRule)
class BotActionRuleAdmin(ModelAdmin):
    list_display = ['name', 'bot_action']
    search_fields = ['name']
    list_filter = ['name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []


@admin.register(RasaEntity)
class RasaEntityAdmin(ModelAdmin):
    list_display = ['content_pack', 'name']
    search_fields = ['name']
    list_filter = ['content_pack', 'name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []


class RasaEntityStackedInline(admin.StackedInline):
    model = RasaEntity


@admin.register(Intent)
class IntentAdmin(ModelAdmin):
    list_display = ['content_pack', 'name']
    search_fields = ['name']
    list_filter = ['content_pack', 'name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []


class IntentStackedInline(admin.StackedInline):
    model = Intent


@admin.register(IntentCorpus)
class IntentCorpusAdmin(ModelAdmin):
    list_display = ['intent', 'corpus']
    search_fields = ['corpus']
    list_filter = ['intent']
    list_display_links = ['corpus']
    ordering = ['id']
    filter_horizontal = []


@admin.register(RasaRules)
class RasaRulesAdmin(ModelAdmin):
    list_display = ['content_pack', 'name']
    search_fields = ['name']
    list_filter = ['content_pack', 'name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
    formfield_overrides = {YAMLField: {
        "widget": AceWidget(mode="yaml", theme='chrome', width='700px')}
    }


class RasaRulesStackedInline(admin.StackedInline):
    model = RasaRules


@admin.register(RasaStories)
class RasaStoriesAdmin(ModelAdmin):
    list_display = ['content_pack', 'name']
    search_fields = ['name']
    list_filter = ['content_pack', 'name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
    formfield_overrides = {YAMLField: {
        "widget": AceWidget(mode="yaml", theme='chrome', width='700px')}
    }


class RasaStoriesStackedInline(admin.StackedInline):
    model = RasaStories
    formfield_overrides = {YAMLField: {
        "widget": AceWidget(mode="yaml", theme='chrome', width='700px')}
    }


@admin.register(RasaResponse)
class RasaResponseAdmin(ModelAdmin):
    list_display = ['content_pack', 'name']
    search_fields = ['name']
    list_filter = ['content_pack', 'name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []


class RasaResponseStackedInline(admin.StackedInline):
    model = RasaResponse


@admin.register(RasaResponseCorpus)
class RasaResponseCorpusAdmin(ModelAdmin):
    list_display = ['response', 'corpus']
    search_fields = ['corpus']
    list_filter = ['response']
    list_display_links = ['corpus']
    ordering = ['id']
    filter_horizontal = []


@admin.register(RasaForms)
class RasaFormsAdmin(ModelAdmin):
    list_display = ['content_pack', 'name']
    search_fields = ['name']
    list_filter = ['content_pack', 'name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
    formfield_overrides = {YAMLField: {
        "widget": AceWidget(mode="yaml", theme='chrome', width='700px')}
    }


class RasaFormsStackedInline(admin.StackedInline):
    model = RasaForms


@admin.register(RasaSlots)
class RasaSlotsAdmin(ModelAdmin):
    list_display = ['content_pack', 'name']
    search_fields = ['name']
    list_filter = ['content_pack', 'name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
    formfield_overrides = {YAMLField: {
        "widget": AceWidget(mode="yaml", theme='chrome', width='700px')}
    }


class RasaSlotsStackedInline(admin.StackedInline):
    model = RasaSlots


@admin.register(ContentPack)
class ContentPackAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []



@admin.register(RasaModel)
class RasaModelAdmin(ModelAdmin):
    list_display = ['name', 'model_file', 'description']
    search_fields = ['name']
    list_filter = ['name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
    formfield_overrides = {YAMLField: {
        "widget": AceWidget(mode="yaml", theme='chrome', width='700px')}
    }
