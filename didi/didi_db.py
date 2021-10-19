
from sqlalchemy.orm import sessionmaker
from sqlalchemy     import create_engine
from didi_model     import *         

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD_DB():

    def __init__(self,path):

        self.path = "sqlite:///%s" % (path,)

    def connect(self):

        self.engine  = create_engine(self.path, echo=False)

        DD_DB_Base.metadata.create_all(self.engine)

        self.session = sessionmaker(bind=self.engine)()

    def get_all_users(self):

        return self.session.query(DD_DB_User).all()

    def get_user_by_uid(self,uid):

        return self.session.query(DD_DB_User).filter_by(uid=uid).all()

    def get_user_by_name(self,name):

        return self.session.query(DD_DB_User).filter_by(name=name).all()

    def get_all_config(self):

        return self.session.query(DD_DB_Config).all()

    def get_config_by_guild(self,guild):

        return self.session.query(DD_DB_Config).filter_by(guild=guild).all()

    def get_all_advice(self):

        return self.session.query(DD_DB_Advice).all()

    def add_advice(self,text,user_uid):

        _users = self.session.query(DD_DB_User).filter_by(uid=user_uid).all()

        _advice      = DD_DB_Advice()
        _advice.text = text
        _advice.user = _users[0]

        self.session.add(_advice)

        self.session.commit()