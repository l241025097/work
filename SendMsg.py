''' 发送消息 '''
import json
import urllib.request
from datetime import datetime
import time

class SendMsg(object):

    def __init__(self, msg_type='SMS', user_list=[], msg_subject='', msg_content=u'测试', msg_level='MINOR'):
        # SMS MAIL PERSON_SETTINGS
        # CRITICAL MAJOR MINOR
        self.post_dict = {
            "orgSystem": "JT.EMOS.MESSAGE.SEND",
            "appId": "EOM_FM",
            "msgKey": "",
            "msgType": msg_type,
            "msgSubject": None,
            "msgAddress": None,
            "msgText": msg_content,
            "msgLevel": msg_level
        }
        if msg_type != 'PERSON_SETTINGS':
            self.post_dict['msgAddress'] = user_list
            self.post_dict['msgSubject'] = msg_subject if msg_type == 'MAIL' else None
            self.send()
        else:
            self.post_dict['msgSubject'] = None
            self.send_personal_msg(user_list)

    def now_timestamp(self):
        now_time = datetime.now()
        now_time_tuple = now_time.timetuple()
        time_epoch = int(time.mktime(now_time_tuple))
        time_epoch = float(str(time_epoch) + str("%06d" % now_time.microsecond))/1000000
        return '%015.3f' % time_epoch

    def send_personal_msg(self, user_list):
        for each_id in user_list:
            self.post_dict['msgAddress'] = each_id
            self.send()

    def send(self):
        msg_id = 'ts_' + self.now_timestamp()
        self.post_dict['msgKey'] = msg_id
        url = 'http://10.160.55.15:8889/esb/JT.EMOS.MESSAGE.SEND/0?authcode=R1hfRU9NUyNAYXV0aEAjWTN1NE9VWng&msgid='+msg_id
        # url = 'http://10.160.55.1:8888/esb/JT.EMOS.MESSAGE.SEND/0?authcode=R1hfRU9NUyNAYXV0aEAjWTN1NE9VWng&msgid='+msg_id
        # url = 'http://10.245.0.222:8890/esb/JT.EMOS.MESSAGE.SEND/0?authcode=R1hfVUNJQVAjQGF1dGhAI3BjODVMUXY3&msgid='+msg_id
        headers = {'Content-Type': 'application/json'}
        post_json_str = json.dumps(self.post_dict).encode('utf8')
        req = urllib.request.Request(url, data=post_json_str, headers=headers)
        res = urllib.request.urlopen(req)
        print(json.loads(res.read().decode('utf8')))
