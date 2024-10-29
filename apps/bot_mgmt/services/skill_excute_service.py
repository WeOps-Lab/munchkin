from apps.bot_mgmt.models import Bot
from apps.core.logger import logger
from apps.model_provider_mgmt.models import LLMSkill
from apps.model_provider_mgmt.services.llm_service import llm_service


class SkillExecuteService:
    @staticmethod
    def execute_skill(bot_id, action_name, user_message, chat_history, sender_id):
        logger.info(f"执行[{bot_id}]的[{action_name}]动作,发送者ID:[{sender_id}],消息: {user_message}")

        bot = Bot.objects.get(id=bot_id)
        llm_skill: LLMSkill = bot.llm_skills.first()
        params = {
            "user_message": user_message,  # 用户消息
            "llm_model": llm_skill.llm_model_id,  # 大模型ID
            "skill_prompt": llm_skill.skill_prompt,  # Prompt
            "enable_rag": llm_skill.enable_rag,  # 是否启用RAG
            "enable_rag_knowledge_source": llm_skill.enable_rag_knowledge_source,  # 是否显示RAG知识来源
            "rag_score_threshold": [
                {"knowledge_base": int(key), "score": float(value)}
                for key, value in llm_skill.rag_score_threshold_map.items()
            ],  # RAG分数阈值
            "chat_history": chat_history,  # 对话历史
            "conversation_window_size": 10,  # 对话窗口大小
        }
        result = llm_service.chat(params)
        result = result["content"]
        if llm_skill.enable_rag_knowledge_source:
            knowledge_titles = {x["knowledge_title"] for x in result["citing_knowledge"]}
            result += "\n"
            result += f'引用知识: {", ".join(knowledge_titles)}\n'
        return result
