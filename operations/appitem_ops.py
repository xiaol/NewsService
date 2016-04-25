from operations import Operations
from models.appitem import AppItem


class AppItemOperation(Operations):
    def __init__(self):
        super(AppItemOperation, self).__init__(AppItem.get_table_name())

    def create_app_item(self, appitem_param):
        if not self._is_param_valid(appitem_param):
            return False
        appitem = AppItem().get_item_from_request_param(appitem_param)
        exist = self.verify_item_exists(appitem.title)
        if not exist:
            result = self.insert(appitem_param)
            return result
        else:
            return 'Already exist in database.'

    @staticmethod
    def _is_param_valid(param):
        require = ['article_title', 'published_date', 'detail_html', 'app_name', 'app_icon']
        for i in require:
            if i not in param or param[i] is None:
                print i
                return False
        return True

    def verify_item_exists(self, title):
        conditions = AppItem()
        conditions.title = title
        ret = self.find_one(conditions=conditions.__dict__,)
        if ret:
            return True
        else:
            return False


