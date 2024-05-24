from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.embed_mgmt.models import EmbedProvider


@admin.register(EmbedProvider)
class EmbedProviderAdmin(ModelAdmin):
    list_display = ['id', 'name', 'enbed_model', 'enabled']
    search_fields = ['name']
    list_filter = ['enbed_model']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
