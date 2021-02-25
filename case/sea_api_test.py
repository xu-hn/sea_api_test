# coding = utf-8
import datetime
import time
import json
from util.db_util import MysqlDb
from util.request_util import RequestUtil
from util.send_mail import SendMail


class SeaclassTestCase:

    def loadAllCaseByApp(self, app):
        """
        根据app加载全部测试用例
        :param app:
        :return:
        """
        print("loadAllCaseByApp")
        my_db = MysqlDb()
        sql = "select * from `case` where app='{0}'".format(app)
        results = my_db.query(sql)
        return results

    def findCaseById(self, case_id):
        """
        根据id找测试用例
        :param case_id:
        :return:
        """
        print("findCaseById")
        my_db = MysqlDb()
        sql = "select * from `case` where id='{0}'".format(case_id)
        results = my_db.query(sql, state="one")
        return results

    def loadConfigByAppAndKey(self, app, key):
        """
        根据app和key加载配置
        :param app:
        :param key:
        :return:
        """
        print("loadConfigByAppAndKey")
        my_db = MysqlDb()
        sql = "select * from `config` where app='{0}' and dict_key='{1}'".format(app, key)
        results = my_db.query(sql, state="one")
        return results

    def updateResultByCaseId(self, response, is_pass, msg, case_id):
        """
        根据测试用例id，更新响应内容和测试内容
        :param response:
        :param is_pass:
        :param msg:
        :param case_id:
        :return:
        """
        print("updateResultByCaseId")
        my_db = MysqlDb()
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(current_time)
        if is_pass:
            sql = "update `case` set response='{0}', pass='{1}', msg='{2}', update_time='{3}' where id={4}".format("",
                                                                                                                   is_pass,
                                                                                                                   msg,
                                                                                                                   current_time,
                                                                                                                   case_id)
        else:
            sql = "update `case` set response=\"{0}\", pass='{1}', msg='{2}', update_time='{3}' where id={4}".format(
                str(response), is_pass, msg, current_time, case_id)
        print(sql)
        rows = my_db.execute(sql)
        return rows

    def runAllCase(self, app):
        """
        执行全部用例的入口
        :param app:
        :return:
        """
        print("runAllCase")
        # 获取接口域名
        api_host_obj = self.loadConfigByAppAndKey(app, "host")
        # 获取全部用例
        results = self.loadAllCaseByApp(app)

        for case in results:
            print(case)
            if case['run'] == 'yes':
                try:
                    # 执行用例
                    response = self.runCase(case, api_host_obj)
                    # 断言判断
                    assert_msg = self.assertResponse(case, response)

                    # 更新结果存储数据库
                    rows = self.updateResultByCaseId(response, assert_msg['is_pass'], assert_msg['msg'], case['id'])
                    print("更新结果 rows={0}".format(str(rows)))
                except Exception as e:
                    print("用例id={0},标题:{1},执行报错:{2}".format(case['id'], case['title'], e))

        # 发送测试报告
        self.sendTestReport(app)

    def runCase(self, case, api_host_obj):
        """
        执行单个用例
        :param case:
        :param api_host_obj:
        :return:
        """
        print("runCase")
        headers = json.loads(case['headers'])
        body = json.loads(case['request_body'])
        method = case['method']
        req_url = api_host_obj['dict_value'] + case['url']

        # 是否有前置条件
        if case["pre_case_id"] > -1:
            print("是否有前置条件")
            pre_case_id = case['pre_case_id']
            pre_case = self.findCaseById(pre_case_id)
            # 递归调用
            pre_response = self.runCase(pre_case, api_host_obj)
            # 前置条件断言
            pre_assert_msg = self.assertResponse(pre_case, pre_response)
            if not pre_assert_msg['is_pass']:
                # 前置条件不通过直接返回
                pre_response['msg'] = "前置条件不通过," + pre_response['msg']
                return pre_response
            # 判断需要case的前置条件是哪个字段
            pre_fields = json.loads(case['pre_fields'])
            for pre_field in pre_fields:
                print(pre_field)
                if pre_field['scope'] == 'header':
                    # 遍历headers ,替换对应的字段值，即寻找同名的字段
                    for header in headers:
                        field_name = pre_field['field']
                        if header == field_name:
                            field_value = pre_response['data'][field_name]
                            headers[field_name] = field_value

                elif pre_field['scope'] == 'body':
                    print("替换body")

        print(headers)
        # 发起请求
        req = RequestUtil()
        response = req.request(req_url, method, headers=headers, param=body)
        return response

    def assertResponse(self, case, response):
        """
        断言响应内容，更新用例执行情况 {"is_pass":true, "msg":"code is wrong"}
        :param case:
        :param response:
        :return:
        """
        print("assertResponse")
        assert_type = case['assert_type']
        expect_result = case['expect_result']

        is_pass = False

        # 判断业务状态码
        if assert_type == 'code':
            response_code = response['code']
            if int(expect_result) == response_code:
                is_pass = True
                print("测试用例通过")
            else:
                print("测试用例不通过")
                is_pass = False

        # 判断数组长度大小
        elif assert_type == 'data_json_array':
            data_array = response['data']
            if data_array is not None and isinstance(data_array, list) and len(data_array) > int(expect_result):
                is_pass = True
                print("测试用例通过")
            else:
                print("测试用例不通过")
                is_pass = False
        elif assert_type == 'data_json':
            data = response['data']
            if data is not None and isinstance(data, dict) and len(data) > int(expect_result):
                is_pass = True
                print("测试用例通过")
            else:
                print("测试用例不通过")
                is_pass = False

        msg = "模块:{0}, 标题:{1},断言类型:{2},响应:{3}".format(case['module'], case['title'], assert_type, response['msg'])

        # 拼装信息
        assert_msg = {"is_pass": is_pass, "msg": msg}
        return assert_msg

    def sendTestReport(self, app):
        """
        发送邮件，测试报告
        :param app:
        :return:
        """
        print("sendTestReport")

        # 加载全部测试用例
        results = self.loadAllCaseByApp(app)
        title = "sea接口自动化测试报告"
        content = """
        <html><body>
            <h4>{0} 接口测试报告：</h4>
            <table border="1">
            <tr>
              <th>编号</th>
              <th>模块</th>
              <th>标题</th>
              <th>是否通过</th>
              <th>备注</th>
              <th>响应</th>
            </tr>
            {1}
            </table></body></html>  
        """
        template = ""
        for case in results:
            template += "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td></tr>".format(
                case['id'], case['module'], case['title'], case['pass'], case['msg'], case['response']
            )

        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        content = content.format(current_time, template)
        mail_host = self.loadConfigByAppAndKey(app, "mail_host")['dict_value']
        mail_sender = self.loadConfigByAppAndKey(app, "mail_sender")['dict_value']
        mail_auth_code = self.loadConfigByAppAndKey(app, "mail_auth_code")['dict_value']
        mail_receivers = self.loadConfigByAppAndKey(app, "mail_receivers")['dict_value'].split(",")
        mail = SendMail(mail_host)
        mail.send(title, content, mail_sender, mail_auth_code, mail_receivers)


if __name__ == '__main__':
    print("main")

    test = SeaclassTestCase()
    test.runAllCase("test")
