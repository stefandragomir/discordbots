
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

    def get_all_config(self):

        return self.session.query(DD_DB_Config).all()

    def get_all_advice(self):

        return self.session.query(DD_DB_Advice).all()

    def get_all_rules(self):

        return self.session.query(DD_DB_Rule).all()

    def get_user_by_uid(self,uid):

        return self.session.query(DD_DB_User).filter_by(uid=uid).all()

    def get_user_profile_by_uid(self,uid):

        _the_profile = None

        _profiles = self.session.query(DD_DB_Profile).all()

        for _profile in _profiles:

            if _profile.user.uid == uid:

                _the_profile = _profile

        return _the_profile

    def get_rules_badwords(self):

        return self.session.query(DD_DB_Rule).filter_by(context=DD_DB_Rule_Types.RULE_BAD_WORD).all()

    def get_rules_hello(self):

        return self.session.query(DD_DB_Rule).filter_by(context=DD_DB_Rule_Types.RULE_HELLO).all()

    def get_rules_goodbye(self):

        return self.session.query(DD_DB_Rule).filter_by(context=DD_DB_Rule_Types.RULE_GOODBY).all()
        
    def add_advice(self,text,user_uid):

        _users = self.session.query(DD_DB_User).filter_by(uid=user_uid).all()

        _advice      = DD_DB_Advice()
        _advice.text = text
        _advice.user = _users[0]

        self.session.add(_advice)

        self.session.commit()

    def create_empty(self):

        _config           = DD_DB_Config()
        _config.token     = "thetoken"
        _config.guild     = "theguild"
        _config.channel   = "thechannel"
        _config.botid     = "thebotid"

        _user             = DD_DB_User()
        _user.name        = "theuser"
        _user.uid         = "theuid"

        _profile          = DD_DB_Profile()
        _profile.badwords = 0
        _profile.admin    = False
        _profile.user     = _user 

        _advice           = DD_DB_Advice()
        _advice.text      = "theadvice"
        _advice.user      = _user

        _rule             = DD_DB_Rule()
        _rule.text        = "thetext"
        _rule.context     = DD_DB_Rule_Types.RULE_BAD_WORD

        self.session.add(_config)
        self.session.add(_user)
        self.session.add(_profile)
        self.session.add(_advice)
        self.session.add(_rule)

        self.session.commit()

