''' main '''
import SendMsg
import StaffTree
from get_order_excel import process, deal_excel, connect_mongo_source
from pandas import DataFrame, read_csv, merge
import pymongo

def query_root(begin_org_id, dst_deepth):
    dbh = connect_mongo_source(db='oss')
    org_dict = dbh.org.find_one({'组织ID': begin_org_id})
    if int(org_dict['组织级别']) == dst_deepth:
        return org_dict
    return query_root(org_dict['父组织ID'], dst_deepth)

def get_user_df(sign='city'):
    substr_num, org_id = (5, '部门编码二级') if sign == 'city' else (7, '部门编码三级')
    dbh = connect_mongo_source(db='oss')
    match_dict = {
        '$match': {
            '部门编码': {'$regex': '^216'}
        }
    }
    project_dict = {
        '$project': {
            '_id': 0,
            '人员账号': 1,
            '工号': 1,
            '专业': 1,
            '办公电话': 1,
            '是否代维人员': 1,
            '人员ID' : 1,
            org_id: {'$substr': ['$部门编码', 0, substr_num]},
            '传真': 1,
            '职务': 1,
            '电子邮件': 1,
            '备注': 1,
            '真实姓名': 1,
            '组织ID': 1,
            '移动电话': 1,
            '人员类别': 1,
            '地址': 1
        }
    }
    return DataFrame(cursor for cursor in dbh.user.aggregate([match_dict, project_dict]))

def get_org_df(sign='city'):
    if sign == 'city':
        level, org_name, org_id = (2, '组织名称二级', '部门编码二级')
    else:
        level, org_name, org_id = (3, '组织名称三级', '部门编码三级')
    dbh = connect_mongo_source(db='oss')    
    match_dict = {
        '$match': {'省分编码': 216, '组织级别': {'$lte': level}}
    }
    project_dict = {
        '$project': {'_id': 0, org_name: '$组织名称', org_id: '$组织编码'}
    }
    return DataFrame(cursor for cursor in dbh.org.aggregate([match_dict, project_dict]))

def merge_user_org():
    user_df = get_user_df('city')    
    org_df = get_org_df('city')
    user_org_city_df = merge(user_df, org_df, how='inner', on='部门编码二级')
    user_df = get_user_df('distinct')
    org_df = get_org_df('distinct')
    user_id_df = user_df[['人员ID', '部门编码三级']]
    user_org_city_df = merge(user_org_city_df, user_id_df, how='inner', on='人员ID')
    user_org_city_distinct_df = merge(user_org_city_df, org_df, how='inner', on='部门编码三级')
    return user_org_city_distinct_df


# for tree_type in ('org', 'user'):
#     sf = StaffTree.StaffTree(sign=tree_type)
#     file_path = sf.download_file(sf.list_file())
#     deal_excel(file_path, tree_type)
#     dbh = connect_mongo_source(db='oss')
#     index = '组织编码' if tree_type == 'org' else '部门编码'
#     dbh.get_collection(tree_type).create_index([(index, pymongo.DESCENDING)])

# deal_excel(process(start_time=None, end_time=None, condition=u'总计@@0@@ALL'), 'all')
# deal_excel(process(start_time=None, end_time=None, condition=u'总计@@0@@NOACCEPT'), 'receive')
# deal_excel(process(start_time=None, end_time=None, item=u'省份故障分析', condition=None), 'analysis')
# SendMsg.SendMsg(msg_type='PERSON_SETTINGS', user_list=['luoyl25'])

# org_df = DataFrame(cursor for cursor in dbh.org.find({'省分编码': 216}))
# user_df = DataFrame(cursor for cursor in dbh.user.find({'部门编码': {'$regex': '^216'}}))
# print(user_df)
# org_id = 58787
# xx = (query_root(org_id, 3) for xx in range(58787, 58797))
# for yy in xx:
#     print(yy)
merge_user_org().to_csv('test.csv', encoding='GB18030')

