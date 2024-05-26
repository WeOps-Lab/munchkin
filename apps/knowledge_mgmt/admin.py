from django.contrib import admin
from django.contrib import messages
from django.forms import Media
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from unfold.admin import ModelAdmin
from unfold.decorators import action
from apps.knowledge_mgmt.models import KnowledgeBaseFolder, FileKnowledge
from apps.knowledge_mgmt.tasks.embed_task import general_parse_embed


@admin.register(FileKnowledge)
class KnowledgeAdmin(ModelAdmin):
    list_display = ['title', 'file']
    search_fields = ['title']
    list_display_links = ['title']
    ordering = ['id']
    filter_horizontal = []
    readonly_fields = ['title']


class KnowledgeStackedInline(admin.StackedInline):
    model = FileKnowledge
    readonly_fields = ['title']


@admin.register(KnowledgeBaseFolder)
class KnowledgeBaseFolderAdmin(ModelAdmin):
    list_display = ['name', 'description', 'embed_model',
                    'enable_general_parse',
                    'train_status']
    search_fields = ['name']
    list_display_links = ['name']
    ordering = ['id']
    filter_horizontal = []
    actions_row = ['train_embed']
    inlines = [KnowledgeStackedInline]
    readonly_fields = ['train_status']
    save_as = True

    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'embed_model')
        }),
        ('分块解析', {
            'fields': ('enable_general_parse', ('general_parse_chunk_size', 'general_parse_chunk_overlap'))
        })
    )

    @action(description='训练', url_path="train_embed_model")
    def train_embed(self, request: HttpRequest, object_id: int):
        general_parse_embed.delay(object_id)
        messages.success(request, '开始训练')
        return redirect(reverse('admin:knowledge_mgmt_knowledgebasefolder_changelist'))
