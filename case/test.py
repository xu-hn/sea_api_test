import unittest

class test():
    def test1(self):
        str1 ='hello1'

        str2 = 'helloworld'
        try:
            self.assertIn(str1,str2,msg=None)
        except Exception as e:
            print(e)
        #print('结果'+bl)

    def assert_equal(str1,str2):
        if str1 in str2:
            return  'true'
        else :
            return  'false'

#{"walletSecretKey":"01d17af28258421ca950cbfbc4f03b26","password":"Ab1234567","macAddress":"1c:15:1f:dc:7e:c2"}
#{"items":"[{'commodityId':'144554548514123445','count':'1'},{'commodityId':'145565474112224447','count':'1'}]","password":"Ab1234567","discountCode":"P55a88cwCltK7R21No","activityType":"2"}
#{"items":\"[{'commodityId':'144554548514123445','count':'1'},{'commodityId':'145565474112224447','count':'1'}]\","password":"Ab1234567","discountCode":"P55a88cwCltK7R21No","activityType":"2"}
if __name__ == "__main__":
    a=test.assert_equal('abc','abddabc')
    print(a)