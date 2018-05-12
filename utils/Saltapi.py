import urllib,json
import urllib.request
import urllib.parse
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class SaltAPI(object):
    __token_id = ''

    # def __init__(self,url,user,password):
    #     self.__url = url
    #     self.__user = user
    #     self.__password = password

    def __init__(self):
        self.__url = 'https://118.25.39.84:8000'
        self.__user = 'saltapi'
        self.__password = 'saltapi123'

    def token_id(self):
        """
        获取用户登录token
        """
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        encode = urllib.parse.urlencode(params)
        obj = urllib.parse.unquote(encode).encode('utf-8')
        content = self.postRequest(obj, prefix='/login')
        try:
            self.__token_id = content['return'][0]['token']
        except KeyError:
            raise KeyError

    def postRequest(self,obj,prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token': self.__token_id}
        req = urllib.request.Request(url, obj, headers)
        opener = urllib.request.urlopen(req)
        content = json.loads(opener.read().decode('utf-8'))
        return content

    def list_all_key(self):
        """
            获取包括认证、未认证的salt主机
        """

        params = {'client': 'wheel', 'fun': 'key.list_all'}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        return minions, minions_pre

    def delete_key(self, node_name):
        '''
            拒绝salt主机
        '''

        params = {'client': 'wheel', 'fun': 'key.delete', 'match': node_name}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def accept_key(self,node_name):
        '''
            接受salt主机
        '''

        params = {'client': 'wheel', 'fun': 'key.accept', 'match': node_name}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def grains(self,tgt,args):
        params={'client':'local','tgt': tgt, 'fun': 'grains.item','arg': args}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def pillarall(self,tgt):
        '''
              获取全部pillar
          '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'pillar.items'}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def salt_get_jid_ret(self,jid):
        """
            通过jid获取执行结果
        :param jid: jobid
        :return: 结果
        ret =salt.salt_get_jid_ret('20180331182123363164')
        """
        params = {'client':'runner', 'fun':'jobs.lookup_jid', 'jid': jid}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        print(content)
        ret = content['return'][0]
        return ret

    def salt_running_jobs(self):
        """
            获取运行中的任务
        :return: 任务结果
        """
        params = {'client':'runner', 'fun': 'jobs.active'}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def remote_noarg_execution_sigle(self, tgt, fun):
        """
            单台minin执行命令没有参数
        :param tgt: 目标主机
        :param fun:  执行模块
        :return: 执行结果

        """
        params = {'client': 'local', 'tgt': tgt, 'fun': fun}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        # print(content)
        # {'return': [{'salt-master': True}]}
        ret = content['return'][0]
        return ret
    def remote_grains_execution_sigle(self, tgt):
        """
            单台minin执行命令没有参数
        :param tgt: 目标主机
        :param fun:  执行模块
        :return: 执行结果
        """
        params = {'client': 'local', 'tgt': tgt, 'fun': 'grains.items'}
        # params = {'client': 'local', 'tgt': tgt, 'fun': fun,'--return':'mysql'}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        # print(content)
        # print(content)
        # {'return': [{'salt-master': True}]}
        ret = content['return'][0]
        return ret


    def remote_execution_single(self, tgt, fun, arg):
        """
            单台minion远程执行，有参数
        :param tgt: minion
        :param fun: 模块
        :param arg: 参数
        :return: 执行结果
         ret = salt.remote_execution_single('*','cmd.run','uptime')
        """
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'list'}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        # print(content)
        # {'return': [{'salt-master': 'root'}]}
        ret = content['return']
        return ret

    def remote_async_execution_module(self, tgt, arg):
        """
            远程异步执行模块，有参数
        :param tgt: minion list
        :param fun: 模块
        :param arg: 参数
        :return: jobid
        salt.remote_async_execution_module('node82','uptime')
        """
        params = {'client': 'local_async', 'tgt': tgt, 'fun':'cmd.run', 'arg': arg, 'expr_form': 'list'}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        print(content)
        # print(content)
        # {'return': [{'jid': '20180131173846594347', 'minions': ['salt-master', 'salt-minion']}]}
        jid = content['return'][0]['jid']
        return jid

    def remote_execution_module(self, tgt, fun, arg):
        """
            远程执行模块，有参数
        :param tgt: minion list
        :param fun: 模块
        :param arg: 参数
        :return: dict, {'minion1': 'ret', 'minion2': 'ret'}
        ret =salt.remote_execution_module('node82','cmd.run','uptime')
        """
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'list'}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        # print(content)
        # {'return': [{'salt-master': 'root', 'salt-minion': 'root'}]}
        #return 20180306200439423091
        ret = content['return'][0]
        return ret

    def salt_state(self, tgt, arg, expr_form):
        '''
        sls文件
        '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': expr_form}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def salt_alive(self, tgt):
        '''
        salt主机存活检测
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'test.ping'}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def file_copy(self, tgt, fun, arg1, arg2, expr_form):
        '''
        文件上传、备份到minion、项目管理
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg1, 'expr_form': expr_form}
        # params2 = {'arg': arg2}
        # obj = urllib.parse.urlencode(params)
        #
        # self.token_id()
        # content = self.postRequest(obj)
        # ret = content['return'][0]
        # return ret
        params2 = {'arg': arg2}
        arg_add = urllib.parse.urlencode(params2)
        print(type(arg_add))
        obj = urllib.parse.urlencode(params)
        obj = obj + '&' + arg_add
        # obj = obj.encode('utf-8')
        self.token_id()
        content = self.postRequest(obj.encode())
        print(type(content))
        ret = content['return'][0]
        return ret

    def file_bak(self,tgt,fun,arg,expr_form):
        '''
        文件备份到master
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': expr_form}
        obj = urllib.parse.urlencode(params)
        self.token_id()
        content = self.postRequest(obj.encode())
        ret = content['return'][0]
        return ret
    def salt_runne(self,jid):
        params = {'client':'runner', 'fun':'jobs.lookup_jid', 'jid': jid}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    #获取JOB ID的详细执行结果
    def runner(self,arg):
        ''' Return minion status '''
        params = {'client': 'runner', 'fun': arg }
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret



if __name__ == '__main__':
        # salt = SaltAPI(url="https://192.168.104.76:8000",user="salt-api",password="salt-api")
        # salt=SaltAPI(url="https://118.25.39.84:8000",user="saltapi",password="saltapi123")

        # minions, minions_pre = salt.list_all_key()
        # 说明如果'expr_form': 'list',表示minion是以主机列表形式执行时，需要把list拼接成字符串，如下所示
        # minions = ['salt-master', 'salt-minion']
        # hosts = map(str, minions)
        # hosts = ",".join(hosts)
        # ret1 = salt.remote_execution_single('node76','jobs.lookup_jid' ,'20180306200439423091')
        # ret = salt.remote_async_execution_module('node76', 'cmd.run', 'uptime')
        # ret = salt.remote_execution_single('*','cmd.run','uptime')
        # ret = salt.salt_get_jid_ret('20180306200753958163')
        # ret = salt.remote_grains_execution_sigle('node82','os')
        # ret =salt.remote_noarg_execution_sigle('*','cmd.run')

        # ret = salt.list_all_key()
        # ret =salt.remote_async_execution_module('10.105.75.82','uptime')
        # ret = salt.salt_get_jid_ret('20180425234518517698')
        # # for k,v in ret.items():
        # #
        # #     print(k,v['Target'])
        # print(ret)
        salt = SaltAPI()
        # abc = ['10.105.75.82','192.168.0.3']
        # for i in abc:
        #     ret = salt.remote_async_execution_module(i, 'pwd')
        #     print(ret)


        a = ['192.168.0.3','10.105.75.82']
        a=','.join(a)

        # b = salt.remote_execution_module(a,'cmd.run','uptime')
        # print(b)

        # ret = salt.remote_execution_module('10.105.75.82','cp.get_file', 'salt://top.sls ', '/tmp/requirements.sls')
        # print(ret)
        # expr_form = 'list'
        # local_path = 'salt://zookeeper/files/jdk-8u152-linux-x64.rpm'
        # remote_path = '/tmp/jdk-8u152-linux-x64.rpm'
        # #从master上拷贝文件到minion上
        # aa = salt.file_copy(a,'cp.get_file',local_path,remote_path,expr_form)
        # print(aa)
        # aa = salt.salt_get_jid_ret('20180430131528300293')
        # # for i,v in aa.items():
        # #     print(i,v)
        # print(aa)
        # jid = salt.remote_async_execution_module(a,'ls'+ ';echo ":::"$?')
        # nn = salt.salt_get_jid_ret(jid)
        # print(nn)

        w = salt.salt_state('10.105.75.82','aa','list')
        print(w)
        # s = salt.salt_running_jobs()
        # print('执行中的任务', s)
        # for k in w.items():
        #     # print(k,v)
        print(w['jid'])


        # import pymysql
        #
        # db = pymysql.connect(host="118.25.39.84", user="root", passwd="Niejc123#", db="dtops")
        # db.autocommit(True)
        # cur = db.cursor()
        #
        # w = salt.salt_state('10.105.75.82', 'chushihua', 'list')
        # jid = w['jid']
        # print(jid)
        # tt = 0
        # nie = False
        # arr = []
        # while (tt < 10):
        #     sql = "select * from salt_returns WHERE jid='%s'" % (w['jid'])
        #     cur.execute(sql)
        #     for i in cur.fetchall():
        #
        #         if i[4] == '1' or i[4] == '0':
        #             arr=[]
        #             nie = True
        #             arr.append([i[0],i[1],i[2], i[3], i[4],i[5] ,i[6]])
        #
        #             break
        #     tt += 1
        # b = []
        # for s in arr:
        #     b.append(s[1]  + '\n' + s[3]+ '\n' + s[4] + '\n' + s[5] + '\n' + str(s[6]))
        #     # print(s[1]  + '\n' + s[3]+ '\n' + s[4] + '\n' + s[5] + '\n' + str(s[6]))
        # # print(arr)
        # print(b)

        # print(a)
        # data = []
        # nn = salt.salt_get_jid_ret('20180430205737417108')
        #
        # for k, v in nn.items():
        #     print(k, v)
        #     print('主机',k)
        #     print('结果',)
        #     data.append({'hostname': k, 'data': v})
        # print(data)
        # print(nn)
        # for k,v in nn.items():
        #     print(k,v)
        #     for j,i in
        #     # print(nn)

        # bb=[]
        # for i in a:
        #     ret =salt.remote_execution_single(i,'cmd.run','ls /var')
        #     for aaa in ret:
        #         for k,v in aaa.items():
        #             bb.append({'hostname':k,'data':v})
        #
        #
        # print(bb)


        #取salt返回的结果
        # import pymysql
        #
        # db = pymysql.connect(host="118.25.39.84", user="root", passwd="Niejc123#", db="dtops")
        # db.autocommit(True)
        # cur = db.cursor()
        #
        # w = salt.salt_state('10.105.75.82', 'chushihua', 'list')
        # jid = w['jid']
        # print(jid)
        # tt = 0
        # nie = False
        # arr = []
        # while (tt < 10):
        #     sql = "select * from salt_returns WHERE jid='%s'" % (w['jid'])
        #     cur.execute(sql)
        #     for i in cur.fetchall():
        #
        #         if i[4] == '1' or i[4] == '0':
        #             arr=[]
        #             nie = True
        #             arr.append([i[0],i[1],i[2], i[3], i[4],i[5] ,i[6]])
        #
        #             break
        #     tt += 1
        # b = []
        # for s in arr:
        #     b.append(s[1]  + '\n' + s[3]+ '\n' + s[4] + '\n' + s[5] + '\n' + str(s[6]))
        #     # print(s[1]  + '\n' + s[3]+ '\n' + s[4] + '\n' + s[5] + '\n' + str(s[6]))
        # # print(arr)
        # print(b)
        #结果：
        #20180501195955228442
        #['20180501195955228442\n10.105.75.82\n1\n{"fun_args": ["chushihua"], "jid": "20180501195955228442", "return": {"file_|-/etc/security/limits.conf_|-/etc/security/limits.conf_|-append": {"comment": "File /etc/security/limits.conf is in correct state", "pchanges": {}, "name": "/etc/security/limits.conf", "start_time": "19:59:55.385203", "result": true, "duration": 7.923, "__run_num__": 0, "__sls__": "chushihua", "changes": {}, "__id__": "/etc/security/limits.conf"}, "file_|-/etc/profile_|-/etc/profile_|-append": {"comment": "File /etc/profile is in correct state", "pchanges": {}, "name": "/etc/profile", "start_time": "19:59:55.393248", "result": true, "duration": 1.27, "__run_num__": 1, "__sls__": "chushihua", "changes": {}, "__id__": "/etc/profile"}, "file_|-~/.bashrc_|-~/.bashrc_|-append": {"comment": "File /root/.bashrc is in correct state", "pchanges": {}, "name": "~/.bashrc", "start_time": "19:59:55.394624", "result": true, "duration": 1.35, "__run_num__": 2, "__sls__": "chushihua", "changes": {}, "__id__": "~/.bashrc"}}, "retcode": 0, "success": true, "cmd": "_return", "_stamp": "2018-05-01T11:59:55.399752", "fun": "state.sls", "id": "10.105.75.82", "out": "highstate"}\n2018-05-01 19:59:55']


