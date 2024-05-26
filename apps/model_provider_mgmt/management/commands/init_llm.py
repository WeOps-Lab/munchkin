from django.core.management import BaseCommand

from apps.model_provider_mgmt.models import EmbedProvider, EmbedModelChoices, LLMModel, LLMModelChoices


class Command(BaseCommand):
    help = '初始化模型数据'

    def handle(self, *args, **options):
        EmbedProvider.objects.get_or_create(
            name='FastEmbed(BAAI/bge-small-en-v1.5)',
            embed_model=EmbedModelChoices.FASTEMBED,
            embed_config={
                'model': 'BAAI/bge-small-en-v1.5',
            },
            enabled=True
        )
        EmbedProvider.objects.get_or_create(
            name='FastEmbed(BAAI/bge-small-zh-v1.5)',
            embed_model=EmbedModelChoices.FASTEMBED,
            embed_config={
                'model': 'BAAI/bge-small-zh-v1.5',
            },
            enabled=True
        )

        LLMModel.objects.get_or_create(
            name='GPT-3.5 Turbo 16K',
            llm_model=LLMModelChoices.GPT35_16K,
            llm_config={
                'openai_api_key': 'your_openai_api_key',
                'openai_base_url': 'https://api.openai.com',
                'temperature': 0.7,
            }
        )
