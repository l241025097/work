import pymongo

pymongo.MongoClient('mongodb://%s:%s@127.0.0.1:61111' % ('luoyl25', 'S198641cn')).get_database('oss')