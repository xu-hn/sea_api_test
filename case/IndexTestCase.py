# coding = utf-8

import unittest
from util.request_util import RequestUtil

host = "https://xxx.xxx.net"


class IndexTestCase(unittest.TestCase):

    def testIndexCategoryList(self):
        """
        首页分类列表
        """
        request = RequestUtil()
        url = host + "/pub/api/v1/web/all_category"
        response = request.request(url, 'get')

        self.assertEqual(response['code'], 0, "业务状态不正常")

        self.assertTrue(len(response['data']) > 0, "分类列表为空")

    def testIndexVideoCard(self):
        """
        首页视频卡片
        """
        request = RequestUtil()
        url = host + "/pub/api/v1/web/index_card"
        response = request.request(url, 'get')
        self.assertEqual(response['code'], 0, "业务状态不正常")
        self.assertTrue(len(response['data']) > 0, "视频卡片为空")

        video_card_list = response['data']
        for card in video_card_list:
            self.assertTrue(len(card['title']) > 0, "卡片标题为空 id=" + str(card['id']))


if __name__ == '__main__':
    unittest.main(verbosity=2)
