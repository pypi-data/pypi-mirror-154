class Configuration:

    __parameter_map = {
        "SLACK_URL": "/SLACK/WEBHOOK_URL/ALERTS",
        "ENV": "STG",
        "REGION": "us-west-2"
    }

    @staticmethod
    def set_key_value(key, value):
        Configuration.__parameter_map[key] = value

    @staticmethod
    def get_value_by_key(key):
        return Configuration.__parameter_map.get(key, None)

    @staticmethod
    def delete(key):
        del Configuration.__parameter_map[key]
