from django.db.models import Q

from apps.base.models import QuotaRule


class QuotaUtils(object):
    def __init__(self, username, teams):
        self.username = username
        self.teams = teams
        self.quota_list = self.get_quota_list()

    def get_quota_list(self):
        query = Q()
        for team_member in self.teams:
            query |= Q(target_type="team", target_list__contains=team_member)
        quota_list = QuotaRule.objects.filter(
            Q(target_type="user", target_list__contains=self.username) | query
        ).values()
        return list(quota_list)

    def get_file_quota(self):
        unit_map = {"GB": 1024, "MB": 1}
        file_size_map = {"shared": [], "private": []}
        type_map = {"shared": "shared", "uniform": "private"}
        for quota in self.quota_list:
            file_size_map[type_map[quota["rule_type"]]].append(quota["file_size"] * unit_map[quota["unit"]])
        if file_size_map["private"]:
            file_size_list = file_size_map["private"]
        else:
            file_size_list = file_size_map["shared"]
        return file_size_list

    def get_skill_quota(self):
        skill_count_map = {"shared": [], "private": []}
        type_map = {"shared": "shared", "uniform": "private"}
        for quota in self.quota_list:
            skill_count_map[type_map[quota["rule_type"]]].append(quota["skill_count"])
        if skill_count_map["private"]:
            skill_count_list = skill_count_map["private"]
        else:
            skill_count_list = skill_count_map["shared"]
        return skill_count_list

    def get_bot_quota(self):
        bot_count_map = {"shared": [], "private": []}
        type_map = {"shared": "shared", "uniform": "private"}
        for quota in self.quota_list:
            bot_count_map[type_map[quota["rule_type"]]].append(quota["bot_count"])
        if bot_count_map["private"]:
            bot_count_list = bot_count_map["private"]
        else:
            bot_count_list = bot_count_map["shared"]
        return bot_count_list
