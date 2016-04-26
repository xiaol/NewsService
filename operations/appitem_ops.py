from operations import Operations
from models.appitem import AppItem


class AppItemOperation(Operations):
    def __init__(self):
        super(AppItemOperation, self).__init__(AppItem.get_table_name())

    def create_app_item(self, appitem_param):
        flag, key = self._is_create_param_valid(appitem_param)
        if not flag:
            return False, 'Param "%s" is required.' % key
        appitem = AppItem().get_item_from_request_param(appitem_param)
        exist = self.verify_item_exists(appitem.publish_time)
        if exist:
            return True, 'Already exist in database.'

        result = self.insert(appitem.__dict__)
        return result, 'Succeeded!'


    @staticmethod
    def _is_create_param_valid(param):
        require = ['published_date', 'detail_html', 'app_name', 'app_icon']
        for i in require:
            if i not in param or not param[i]:
                print i
                return False, i
        return True, None

    def verify_item_exists(self, publish_time):
        conditions = AppItem()
        conditions.publish_time = publish_time
        ret = self.find_one(conditions=conditions.__dict__,)
        if ret:
            return True
        else:
            return False


