''' 人员组织树 '''
import os
import re
from datetime import datetime

import paramiko
from scp import SCPClient

class StaffTree(object):
    ''' 人员组织树 '''

    def __init__(self, host='10.160.55.7', user='aiuap', passwd='Aiuap@123', port=22, sign='org'):
        self.ssh = self.connect_host(host, user, passwd, port)
        self.sign = sign

    def connect_host(self, host='10.160.55.7', user='aiuap', passwd='Aiuap@123', port=22):
        ''' 连接esb '''
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, passwd)
        return ssh

    def list_file(self, sign=''):
        ''' 获取目录中文件 '''
        sign = sign if sign else self.sign
        now_str = datetime.now().strftime('%Y-%m-%d')
        ls_path = os.path.join('/home/aiuap/qimin/', sign)
        _, stdout, _ = self.ssh.exec_command('ls ' + ls_path)
        new_file = max(each_file.strip() for each_file in stdout.readlines())
        regex_obj = re.search(now_str, new_file)
        if regex_obj:
            return os.path.join(ls_path, new_file)

    def download_file(self, dst_path_file='', store_path_file=''):
        ''' 下载指定文件 '''
        file_name = os.path.split(dst_path_file)[1]
        current_path = os.path.dirname(__file__)
        if not current_path:
            current_path = os.getcwd()
        if not store_path_file:
            store_path_file = os.path.join(current_path, file_name)
        scpclient = SCPClient(self.ssh.get_transport(), socket_timeout=15.0)
        scpclient.get(dst_path_file, store_path_file)
        self.ssh.close()
        return store_path_file
