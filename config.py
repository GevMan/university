class Configuration(object):
    DEBUG=True
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:''@localhost/diplom'
    SQLALCHEMY_POOL_RECYCLE = 60


