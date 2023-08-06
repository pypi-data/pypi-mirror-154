class Constants:

    def __init__(self):
        self.__parameter_map = {
            "SLACK_URL": "/SLACK/WEBHOOK_URL/ALERTS",
            "ENV": "STG",
            "REGION": "us-west-2"
        }

    def set_key_value(self, key, value):
        self.__parameter_map[key] = value

    def get_value_by_key(self, key):
        self.__parameter_map.get(key, None)
