from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.llm_mgmt.models import EmbedProvider, LLMModel


@admin.register(EmbedProvider)
class EmbedProviderAdmin(ModelAdmin):
    list_display = ['name', 'embed_model', 'enabled']
    search_fields = ['name']
    list_filter = ['embed_model']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []


@admin.register(LLMModel)
class LLMModelAdmin(ModelAdmin):
    list_display = ['name', 'llm_model']
    search_fields = ['name']
    list_filter = ['llm_model']
    list_display_links = ['name']

    ordering = ['id']
    filter_horizontal = []
