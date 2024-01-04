import configparser

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
        return self.config.get("User","token")

    def get_cookies(self):
        return self.config.get("User","cookies")

    def get_coll(self):
        return self.config.get("User","coll")

    def get_proxy(self):
        return self.config.get("User","proxy")

    def set_level(self):
        return self.config.get("User","level")

    def get_user(self):
        return self.config.get("User","user")


    def get_live_cookie(self):
        res_arr = []
        res = requests.request('GET',url = self.config.get("User","token_url"),proxies=con_str_to_dict(self.config.get("User","proxy")))
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        token_input = soup.find('input', {'name': '_token'})
        token_value = token_input['value']
        res_login=requests.request('POST', url=self.config.get("User","login_url"), data=con_str_to_dict(self.config.get("User","user"))
                                , proxies=con_str_to_dict(self.config.get("User","proxy")))
        res_arr.append(res_login.cookies)
        res_arr.append(token_value)
        return res_arr

if __name__ == '__main__':
    con = ConfigSingleton()
    cookies = con.get_live_cookie()[0]
    token = con.get_live_cookie()[1]
    print(cookies)
    print(token)
    url = f"https://wallhaven.cc/favorites/add?wallHashid=qz5r6q&collectionId=1664450&_token={token}"
    print(url)
    res =  requests.request('POST',url=url,cookies=cookies,proxies=con_str_to_dict(con.config.get("User","proxy")) )
    print(res.status_code)



