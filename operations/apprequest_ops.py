import hashlib

from operations import Operations
from models.appitem import AppRequestItem


class AppRequestItemOperation(Operations):
    def __init__(self):
        super(AppRequestItemOperation, self).__init__(AppRequestItem.get_table_name())

    def create_app_item(self, appitem_param):
        flag, key = self._is_create_param_valid(appitem_param)
        if not flag:
            return False, 'Param "%s" is required.' % key
        appitem = AppRequestItem().get_request_item_from_param(appitem_param)
        exist = self.verify_item_exists(appitem.url)
        if exist:
            return False, 'Already exist in database.'

        result = self.insert(appitem.__dict__)
        return result, 'Succeeded!'


    @staticmethod
    def _is_create_param_valid(param):
        require = ['published_date', 'detail_html', 'app_name', 'article_title']
        for i in require:
            if i not in param or not param[i]:
                print i
                return False, i
        return True, None

    def verify_item_exists(self, key):
        conditions = AppRequestItem()
        conditions.url = key
        ret = self.find_one(conditions=conditions.__dict__,)
        if ret:
            return True
        else:
            return False
