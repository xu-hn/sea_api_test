import requests
from util.aes_util import AESUtil

"""
Http工具类封装
"""

class RequestUtil:

    def __init__(self):
        pass

    def request(self, url, method, headers=None, param=None, content_type=None):
        """
        通用请求工具类
        :param url:
        :param method:
        :param headers:
        :param param:
        :param content_type:
        :return:
        """
        try:
            if method == 'get':
                result = requests.get(url=url, params=param, headers=headers).json()
                return result
            elif method == 'post':
                if content_type == 'application/json':
                    #加密
                    print('-------加密前-------', param)
                    param=str(param)
                    param =AESUtil.seaEncryt(param)
                    print('-------加密后-------', param)
                    result = requests.post(url=url, json=param, headers=headers).json()
                    print('-------接口返回-------', result)
                    return result
                else:
                    print('-------加密前-------', param)
                    param = str(param)
                    param = AESUtil.seaEncryt(param)
                    print('-------加密后-------', param)
                    result = requests.post(url=url, data=param, headers=headers).json()
                    print('-------接口返回-------', result)

                    return result
            else:
                print("http method not allowed")


        except Exception as e:
            print("http请求报错:{0}".format(e))


if __name__ == '__main__':
    # url = "https://api.xdclass.net/pub/api/v1/web/all_category"
    # r = RequestUtil()
    # result = r.request(url, 'get')
    # print(result)

    url = "https://api.xdclass.net/pub/api/v1/web/web_login"
    r = RequestUtil()
    data = {"phone": "13113777555", "pwd": "1234567890"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    result = r.request(url, 'post', param=data, headers=headers)
    print(result)


