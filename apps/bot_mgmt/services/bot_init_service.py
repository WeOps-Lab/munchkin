from apps.bot_mgmt.models import RasaModel


class BotInitService:
    def __init__(self, owner):
        self.owner = owner.username

    def init(self):
        rasa_model, created = RasaModel.objects.get_or_create(
            name="Core Model", defaults={"description": "核心模型", "created_by": self.owner}
        )
        if created:
            with open("support-files/data/ops-pilot.tar.gz", "rb") as f:
                rasa_model.model_file.save("core_model.tar.gz", f)
            rasa_model.save()

        # Bot.objects.get_or_create(
        #     name="OpsPilot",
        #     defaults={
        #         "created_by": self.owner,
        #         "rasa_model": rasa_model,
        #         "introduction": "Intelligent Operations Assistant",
        #     },
        # )
