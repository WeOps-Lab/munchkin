from django.contrib import admin
from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from unfold.admin import ModelAdmin
from unfold.decorators import action
from apps.knowledge_mgmt.models import KnowledgeBaseFolder, Knowledge
from apps.knowledge_mgmt.tasks.embed_task import general_parse_embed


@admin.register(Knowledge)
class KnowledgeAdmin(ModelAdmin):
    list_display = ['title', 'file']
    search_fields = ['title']
    list_display_links = ['title']
    ordering = ['id']
    filter_horizontal = []
    readonly_fields = ['title']


class KnowledgeStackedInline(admin.StackedInline):
    model = Knowledge
    readonly_fields = ['title']


@admin.register(KnowledgeBaseFolder)
class KnowledgeBaseFolderAdmin(ModelAdmin):
    list_display = ['name', 'description', 'embed_model',
                    'enable_general_parse',
                    'train_status', 'display_train_progress']
    search_fields = ['name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
    actions_row = ['train_embed']
    inlines = [KnowledgeStackedInline]
    readonly_fields = ['train_status', 'train_progress']
    save_as = True

    def display_train_progress(self, obj):
        return f"{obj.train_progress * 100}%"

    display_train_progress.short_description = '进度'

    @action(description='训练', url_path="train_embed_model")
    def train_embed(self, request: HttpRequest, object_id: int):
        general_parse_embed.delay(object_id)
        messages.success(request, '开始训练')
        return redirect(reverse('admin:knowledge_mgmt_knowledgebasefolder_changelist'))
