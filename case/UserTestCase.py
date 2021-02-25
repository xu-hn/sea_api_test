# coding = utf-8

import unittest
from util.request_util import RequestUtil

host = "https://xxx.xxxxx.net"


class UserTestCase(unittest.TestCase):

    def testLogin(self):
        """
       用户登录
        """
        request = RequestUtil()
        url = host + "/pub/api/v1/web/web_login"

        data = {"phone": "13113777555", "pwd": "1234567890"}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = request.request(url, 'post', param=data, headers=headers)
        self.assertEqual(response['code'], 0, "登录接口测试失败")


if __name__ == '__main__':
    unittest.main(verbosity=2)

