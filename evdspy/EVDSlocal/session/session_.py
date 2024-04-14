from evdspy.EVDSlocal.utils.utils_general import *


class Session:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Session, cls).__new__(cls)
            cls.start(cls)

        return cls.instance

    def start(cls):
        cls.hash = get_random_hash(5)

    def attach_logger(cls, logger_):
        cls.logger = logger_

    def __repr__(self):
        return f"session:{self.hash}"

    # def __new__(cls, sObj = None , DB = None , *args, **kwargs):
    #     if not hasattr(cls, 'instance'):
    #         cls.db = DB(cls)
    #         cls.annoying = False
    #         if sObj is not None :
    #             cls.start(cls, sObj)
    #         cls.instance = super(Session, cls).__new__(cls)


def get_session():
    return Session()