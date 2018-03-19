import urllib.parse
import  urllib.request
import json
class Get_Ip(object):
    '''获取用户访问来源城市'''

    def __init__(self,ip):
        self.url = "http://api.ip138.com/query/?ip="
        self.ip = ip
        self.token = "131d572415811b6a25552f1b16710955"
    def getip(self):
        obj1 = self.url + self.ip
        print(obj1)
        headers = {'token':self.token}
        req = urllib.request.Request(obj1, headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        content = json.loads(response.read().decode('utf-8'))
        return content['data']
if __name__ == '__main__':
    get_ip = Get_Ip("183.131.17.228",)
    a= "".join(get_ip.getip()).strip()
    print(a)