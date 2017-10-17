''' main '''
import SendMsg
import StaffTree
from get_order_excel import process, deal_excel

# SendMsg.SendMsg(msg_type='PERSON_SETTINGS', user_list=['luoyl25'])
# sf = StaffTree.StaffTree(sign='user')
# sf.download_file(sf.list_file())
deal_excel(process(start_time=None, end_time=None, condition=u'总计@@0@@ALL'), 'all')
# deal_excel(process(start_time=None, end_time=None, condition=u'总计@@0@@NOACCEPT'), 'receive')
# deal_excel(process(start_time=None, end_time=None, item=u'省份故障分析', condition=None), 'analysis')
