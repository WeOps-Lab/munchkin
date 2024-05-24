from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.embed_mgmt.models import EmbedProvider


@admin.register(EmbedProvider)
class EmbedProviderAdmin(ModelAdmin):
    list_display = ['name', 'embed_model', 'enabled']
    search_fields = ['name']
    list_filter = ['embed_model']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
