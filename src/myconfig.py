import configparser
import time

import bs4 as bs4
import requests


def con_str_to_dict(con_str):
    key_value_pairs = con_str.split(";")
    goal_dict = {pair.split("=")[0]: pair.split("=")[1] for pair in key_value_pairs}
    return goal_dict


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
        return self.config.get("User", "token")

    def get_cookies(self):
        return self.config.get("User", "cookies")

    def get_coll(self):
        return self.config.get("User", "coll")

    def get_proxy(self):
        return self.config.get("User", "proxy")

    def set_level(self):
        return self.config.get("User", "level")

    def get_user(self):
        return self.config.get("User", "user")

    def get_copy_token(self):
        return self.config.get("User", "copy_token")

    def get_copy_cookies(self):
        return self.config.get("User", "copy_cookies")


    # 获取用户登录信息的session，但是在这个网页传递视乎存在问题，不清楚具体的验证规则，所以这个session无效
    def get_mysession(self):
        mysession = requests.Session()
        res_login = mysession.post(url=self.config.get("User", "login_url"),
                                   data=con_str_to_dict(self.config.get("User", "user"))
                                   , proxies=con_str_to_dict(self.config.get("User", "proxy")))
        soup = bs4.BeautifulSoup(res_login.text, 'html.parser')
        token_input = soup.find('meta', {'name': 'csrf-token'})
        token_value = token_input['content']
        # return token_value, mysession
        return mysession,token_value


if __name__ == '__main__':
    pass
    # headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}
    # mysession_new,t = ConfigSingleton().get_mysession()
    # url = 'https://wallhaven.cc/favorites/add?wallHashid=exrqrr&collectionId=670878&_token={}'.format(t)
    #
    # res = mysession_new.post(url = url,headers = headers,proxies = con_str_to_dict(ConfigSingleton().config.get("User", "proxy")))
    # print(mysession_new.cookies,'\n',mysession_new.headers)
    # print(url)
    # print(t)
    # print(res.text)

