Debug = True

if not Debug:
    MONGODB_USER = 'ly'
    MONGODB_PWD = '1qaz*963.'
    MONGODB_HOST = '127.0.0.1'
    MONGODB_PORT = 27017
    MONGODB_DBNAME = 'News'


elif Debug:
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

