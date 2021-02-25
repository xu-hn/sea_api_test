# -*- coding:utf-8 -*-
import urllib
import requests
#rypto.Cipher import AES
from Crypto.Cipher import  AES
import base64


class AESUtil:

    __BLOCK_SIZE_16 = BLOCK_SIZE_16 = AES.block_size

    @staticmethod
    def encryt(str, key, iv):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        x = AESUtil.__BLOCK_SIZE_16 - (len(str) % AESUtil.__BLOCK_SIZE_16)
        if x != 0:
            str = str + chr(x) * x
        msg = cipher.encrypt(str)
        msg = base64.b64encode(msg)
        return msg

    @staticmethod
    def seaEncryt(jsondata):
        key = '4fpStEiWr9kk069MHr2S+sEHaMh7wH9S'
        iv = '4fpStEiWr9kk069M'
        res = AESUtil.encryt(jsondata, key, iv)
        res2 = str(res, 'utf-8')
        data = urllib.parse.quote_plus(res2)
        para = 'data=' + data
        return para

if __name__ == "__main__":
    interfaceUrl = "https://test-sea-zuul.peogoo.com/user/walletUser/importWallet"
    print("interfaceUrl=" + interfaceUrl)

    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    print(headers.items())

    jsondata = '{"walletSecretKey":"01d17af28258421ca950cbfbc4f03b26","password":"Ab1234567","macAddress":"1c:15:1f:dc:7e:c2"}'
    print("jsondata=" + jsondata)
    para = AESUtil.seaEncryt(jsondata)
    print('para:' + str(para))
    response = requests.post(url=interfaceUrl, data=para, headers=headers)
    print(response.text)