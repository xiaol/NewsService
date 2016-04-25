import platform

from pymongo.database import Database

from settings import MONGODB_HOST, MONGODB_PORT, MONGODB_PWD, MONGODB_DBNAME, MONGODB_USER

def get_python_version():
    """
    get python version info
    :return:
    """
    ver = platform.python_version()
    arr_version = ver.split('.')
    l = len(arr_version)
    ver = 0
    for item in arr_version:
        ver += int(item) * (10 ** l)
        l -= 1
    ver /= 10 ** (len(arr_version) - 1)

    return ver

version = get_python_version()
if version > 26:
    from pymongo import MongoClient as Connection
else:
    from pymongo import Connection


class MongoDB(object):
    __instance = None
    __db_connection = None

    def __new__(cls, *args, **kwargs):
        if MongoDB.__instance is None:
            MongoDB.__instance = object.__new__(cls, *args, **kwargs)
        return MongoDB.__instance

    def __init__(self, **kwargs):
        if 'host' not in kwargs or not kwargs['host']:
            self.host = MONGODB_HOST
        else:
            self.host = kwargs['host']

        if 'port' not in kwargs or not kwargs['port']:
            self.port = MONGODB_PORT
        else:
            self.port = kwargs['port']

        if 'db' not in kwargs or not kwargs['db']:
            self.db = MONGODB_DBNAME
        else:
            self.db = kwargs['db']

        # if 'rs' not in kwargs or not kwargs['rs']:
        #     self.rs = settings.MONGODB_RS
        # else:
        #     self.rs = kwargs['rs']
        #
        if 'user' not in kwargs or not kwargs['user']:
            self.user = MONGODB_USER
        else:
            self.user = kwargs['user']
        #
        if 'pwd' not in kwargs or not kwargs['pwd']:
            self.pwd = MONGODB_PWD
        else:
            self.pwd = kwargs['pwd']

    def get_database(self):
        if self.__db_connection is None:
            from pymongo.read_preferences import ReadPreference
            # self.__db_connection = Database(Connection(self.host, self.port), self.db)
            self.__db_connection = Database(Connection(self.host, self.port), self.db)#replicaSet='', read_preference=ReadPreference.SECONDARY_PREFERRED), self.db)
            self.__db_connection.authenticate(self.db, self.pwd)

        return self.__db_connection