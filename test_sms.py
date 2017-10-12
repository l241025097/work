#!usr/bin/python
#coding: utf8

import sys
import json
import urllib
import urllib2
from datetime import datetime
import time
reload(sys)
sys.setdefaultencoding('utf8')

def datetime_to_timestamp(datetime_obj):
    if not isinstance(datetime_obj, datetime):
        raise TypeError('need datetime type')
    now_time = datetime_obj
    now_time_tuple = now_time.timetuple()
    time_epoch = int(time.mktime(now_time_tuple))
    time_epoch = float(str(time_epoch) + str("%06d" % now_time.microsecond))/1000000
    return '%015.3f' % time_epoch

now_time_obj = datetime.now()
msg_id = datetime_to_timestamp(now_time_obj)
msg_dict = {
    "orgSystem":"JT.EMOS.MESSAGE.SEND",
    "appId":"EOM_FM",
    "msgKey": msg_id,
    "msgType":"PERSON_SETTINGS",
    "msgSubject":"test",
    "msgText":u"消息内容",
    # "msgAddress":[
    #     "luoyl25"
    # ],
    "msgAddress":"luoyl25",
    "msgLevel":"MINOR",
    # 'update': now_time_obj
}
# dbh = pymongo.MongoClient(host='192.168.1.104').get_database('un_source')

# return_dict = {
#     "orgSystem":"JT.EMOS.MESSAGE.SEND",
#     "msgKey": msg_id,
#     "msgType":"SMS",
#     "msgText":u"消息内容",
#     "msgAddress":[
#         "15676192675"
#     ],
#     "msgLevel":"MINOR",
#     "msgResult":u"成功",
#     "msgResultDes":""
# }
url = 'http://10.160.55.15:8889/esb/JT.EMOS.MESSAGE.SEND/0?authcode=R1hfRU9NUyNAYXV0aEAjWTN1NE9VWng&msgid='+msg_id
# url = 'http://10.160.55.1:8888/esb/JT.EMOS.MESSAGE.SEND/0?authcode=R1hfRU9NUyNAYXV0aEAjWTN1NE9VWng&msgid='+msg_id
# url = 'http://10.245.0.222:8890/esb/JT.EMOS.MESSAGE.SEND/0?authcode=R1hfVUNJQVAjQGF1dGhAI3BjODVMUXY3&msgid='+msg_id
headers = {'Content-Type': 'application/json'}
# param_dict = {
#     "orgSystem":"JT.EMOS.MESSAGE.SEND",
#     "msgKey":241025097,
#     "msgType":"SMS",
#     "msgText":u"消息内容",
#     "msgAddress":[
#         "15676192675"
#     ],
#     "msgLevel":"MINOR"
# }
msg_json_str = json.dumps(msg_dict)
req = urllib2.Request(url, data=msg_json_str, headers=headers)
res = urllib2.urlopen(req)
print json.loads(res.read())