import os.path
import tempfile

from celery import shared_task
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_elasticsearch import ElasticsearchStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger
from tqdm import tqdm

from apps.embed_mgmt.models import EmbedModelChoices
from apps.knowledge_mgmt.models import KnowledgeBaseFolder, Knowledge
from apps.knowledge_mgmt.utils import get_index_name
from munchkin.components.elasticsearch import ELASTICSEARCH_URL

load_dotenv()


@shared_task
def general_parse_embed(knowledge_base_folder_id):
    """
    常规方法解析知识库
    :param knowledge_base_folder_id:
    :return:
    """
    logger.info(f'开始训练知识库:[{knowledge_base_folder_id}]')

    # 1. 获取目标知识库
    knowledge_base_folder = KnowledgeBaseFolder.objects.get(id=knowledge_base_folder_id)
    index_name = get_index_name(knowledge_base_folder_id)

    es = Elasticsearch(ELASTICSEARCH_URL)

    # 检查索引是否存在
    if es.indices.exists(index=index_name):
        # 如果存在，删除索引
        es.indices.delete(index=index_name)

    try:
        # Set train_status to 1 (处理中) and train_progress to 0 at the start of the task
        knowledge_base_folder.train_status = 1
        knowledge_base_folder.train_progress = 0
        knowledge_base_folder.save()

        # 2. 初始化Embed实例
        if knowledge_base_folder.embed_model.embed_model == EmbedModelChoices.FASTEMBED:
            from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
            model_configs = knowledge_base_folder.embed_model.embed_config
            embedding = FastEmbedEmbeddings(model_name=model_configs['model'], cache_dir='models')

            logger.info(f'初始化FastEmbed模型成功')

            knowledges = Knowledge.objects.filter(knowledge_base_folder=knowledge_base_folder).all()

            total_knowledges = len(knowledges)

            for index, knowledge in enumerate(tqdm(knowledges)):
                logger.info(f'训练知识:[{knowledge.title}]')
                with tempfile.NamedTemporaryFile(delete=False) as f:
                    content = knowledge.file.read()
                    f.write(content)

                    file_type = os.path.splitext(knowledge.file.name)[1]
                    if file_type == '.md':
                        loader = UnstructuredMarkdownLoader(f.name)
                        text_splitter = RecursiveCharacterTextSplitter(
                            chunk_size=knowledge_base_folder.chunk_size,
                            chunk_overlap=knowledge_base_folder.chunk_overlap
                        )
                        knowledge_docs = text_splitter.split_documents(loader.load())
                    else:
                        loader = UnstructuredFileLoader(f.name, mode="elements")
                        text_splitter = RecursiveCharacterTextSplitter(
                            chunk_size=knowledge_base_folder.chunk_size,
                            chunk_overlap=knowledge_base_folder.chunk_overlap
                        )
                        knowledge_docs = text_splitter.split_documents(loader.load())
                    db = ElasticsearchStore.from_documents(
                        knowledge_docs,
                        es_url=ELASTICSEARCH_URL,
                        index_name=index_name,
                        embedding=embedding,
                    )
                    db.client.indices.refresh(index=index_name)

                    knowledge_base_folder.train_progress = (index + 1) / total_knowledges
                    knowledge_base_folder.save()

            knowledge_base_folder.train_status = 2
            knowledge_base_folder.train_progress = 1
            knowledge_base_folder.save()

    except Exception as e:
        logger.error(f'Training failed with error: {e}')

        # If the task fails, set train_status to 3 (失败) and train_progress to 100
        knowledge_base_folder.train_status = 3
        knowledge_base_folder.train_progress = 1
        knowledge_base_folder.save()
