import configparser


class ConfigSingleton:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.config = configparser.ConfigParser()
            cls.__instance.config.read('../config.ini')
        return cls.__instance

    def get_config(self, section, option):
        return self.config.get(section, option)

    def api_key(self):
        return self.config.get("User", "api_key")

    def get_token(self):
        return self.config.get("User","token")

    def get_cookies(self):
        return self.config.get("User","cookies")

    def get_coll(self):
        return self.config.get("User","coll")
