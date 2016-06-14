Debug = False

if Debug:
    MONGODB_USER = 'ly'
    MONGODB_PWD = '1qaz*963.'
    MONGODB_HOST = '120.27.162.110'
    MONGODB_PORT = 27017
    MONGODB_DBNAME = 'News'
    POSTGRE_USER = 'postgres'
    POSTGRE_PWD = 'ly@postgres&2015'
    POSTGRE_HOST = '120.27.163.25'
    POSTGRE_DBNAME = 'BDP'
    POSTGRES = "postgresql://postgres:ly@postgres&2015@120.27.163.25/BDP"

elif not Debug:
    MONGODB_USER = 'ly'
    MONGODB_PWD = '1qaz*963.'
    MONGODB_HOST = '127.0.0.1'
    MONGODB_PORT = 27017
    MONGODB_DBNAME = 'News'
    POSTGRE_USER = 'postgres'
    POSTGRE_PWD = 'ly@postgres&2015'
    POSTGRE_HOST = '120.27.163.25'
    POSTGRE_DBNAME = 'BDP'
    POSTGRES = "postgresql://postgres:ly@postgres&2015@120.27.163.25/BDP"

REDIS_URL = 'redis://ccd827d637514872:LYcache2015@ccd827d637514872.m.cnhza.kvstore.aliyuncs.com:6379'
NEWS_STORE_API = "http://api.deeporiginalx.com/bdp/spider/pipeline/task/{key}"
NEWS_STORE_API_V2 = 'http://bdp.deeporiginalx.com/v2/sps/ns/{key}'

