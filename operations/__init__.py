from utils.utility import get_mongodb

class Operations(object):
    __instance = None
    __db = None
    __table = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, tableName):
        if self.__db is None:
            self.__db = get_mongodb()

        self.__table = tableName

    def set_table_name(self, tableName):
        self.__table = tableName

    def insert(self, data):
        try:
            result = self.__db[self.__table].insert(data)
        except:
            result = False
        return result

    def insert_many(self, data_list):
        result = self.__db[self.__table].insert_many(data_list)
        return result

    def find(self, conditions=None, fields=None, sort=None, skip=None, limit=None, **kwargs):
        if not skip:
            skip = 0
        if not conditions:
            conditions = {}

        read_preference = None
        if 'read_preference' in kwargs and kwargs['read_preference']:
            read_preference = kwargs['read_preference']

        tmp_collection = self.__db[self.__table]
        if read_preference:
            tmp_collection = self.__db[self.__table].with_options(read_preference=read_preference)

        if fields:
            result = tmp_collection.find(conditions, fields)
        else:
            result = tmp_collection.find(conditions)

        if 'distinct' in kwargs:
            result = result.distinct(kwargs['distinct'])

        if sort and len(sort) == 2:
            result = result.sort(sort[0], sort[1])

        if skip:
            result = result.skip(skip)
        if limit:
            result = result.limit(limit)

        if 'count' in kwargs:
            return result.count()

        del tmp_collection

        return result

    def find_one(self, conditions=None, fields=None, **kwargs):
        if not conditions:
            conditions = {}

        read_preference = None
        if 'read_preference' in kwargs and kwargs['read_preference']:
            read_preference = kwargs['read_preference']

        tmp_collection = self.__db[self.__table]
        if read_preference:
            tmp_collection = self.__db[self.__table].with_options(read_preference=read_preference)

        if fields:
            result = tmp_collection.find_one(conditions, fields)
        else:
            result = tmp_collection.find_one(conditions)

        del tmp_collection

        return result

    def update(self, conditions=None, updatedTo=None, upsert=False, multi=False, **kwargs):
        if not conditions:
            conditions = {}

        if not updatedTo:
            return False

        result = self.__db[self.__table].update(conditions, updatedTo, upsert=upsert, multi=multi)
        return result

    def remove(self, conditions):
        if not conditions:
            return False

        result = self.__db[self.__table].remove(conditions)
        return result

    def removeAll(self, confirm):
        if not confirm:
            return False
        result = self.__db[self.__table].remove({})
        return result

    def findAndModify(self, conditions, updatedTo):
        if not conditions or not updatedTo:
            return False

        result = self.__db[self.__table].find_and_modify(conditions, updatedTo)

        return result