import pymongo
import urllib

username = urllib.parse.quote_plus('admin')
password = urllib.parse.quote_plus('Weixin@1026')
host = '127.0.0.1:61111'

dbh = pymongo.MongoClient('mongodb://%s:%s@%s' % (username, password, host)).get_database('admin')
print(dbh.name)