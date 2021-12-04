
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

    def get_all_users(self):

        return self.session.query(DD_DB_User).all()

    def get_all_advice(self):

        return self.session.query(DD_DB_Advice).all()

    def get_all_profiles(self):

        return self.session.query(DD_DB_Profile).all()

    def get_all_rules(self):

        return self.session.query(DD_DB_Rule).all()

    def get_all_words(self):

        return self.session.query(DD_DB_Word).all()

    def get_user_by_uid(self,uid):

        return self.session.query(DD_DB_User).filter_by(uid=uid).all()

    def get_user_by_name(self,name):

        return self.session.query(DD_DB_User).filter_by(name=name).all()

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

        _users = self.get_user_by_uid(user_uid)

        _advice      = DD_DB_Advice()
        _advice.text = text
        _advice.user = _users[0]

        self.session.add(_advice)

        self.session.commit()

    def add_word(self,text):

        text = str(text).lower()

        _words = self.session.query(DD_DB_Word).filter_by(text=text).all()

        if len(_words) > 0:
            for _word in _words:

                _word.count += 1
        else:
            _word       = DD_DB_Word()
            _word.text  = text
            _word.count = 1
            _word.tag   = DD_DB_POS_TAGS.X

        self.session.add(_word)

        self.session.commit()

    def get_word(self,text):

        return self.session.query(DD_DB_Word).filter_by(text=text).all()

    def increment_badword(self,user_uid):

        _profile = self.get_user_profile_by_uid(user_uid)

        if _profile != None:

            _profile.badwords += 1

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

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD_Clean_DB():

    def __init__(self,original_path,clean_path,log):

        self.db       = DD_DB(original_path)
        self.db_clean = DD_DB(clean_path)
        self.log      = log

    def run(self):

        self.log.debug("connecting to db [%s]" % (self.db.path,))
        self.db.connect()

        self.log.debug("connecting to db [%s]" % (self.db_clean.path,))
        self.db_clean.connect()

        self.clean_configs()

        self.clean_users()

        self.clean_advice()

        self.clean_profiles()

        self.clean_rules()

        self.clean_words()

        self.log.debug("saving")
        self.db_clean.session.commit()

        self.log.debug("done")

    def clean_configs(self):

        self.log.debug("cleaning config table")

        _configs  = self.db.get_all_config()

        for _config in _configs:

            _new         = DD_DB_Config()
            _new.token   = _config.token
            _new.guild   = _config.guild
            _new.channel = _config.channel
            _new.botid   = _config.botid

            self.db_clean.session.add(_new)

    def clean_users(self):

        self.log.debug("cleaning user table")

        _users    = self.db.get_all_users()

        for _user in _users:

            _new      = DD_DB_User()
            _new.name = _user.name
            _new.uid  = _user.uid

            self.db_clean.session.add(_new)

    def clean_advice(self):

        self.log.debug("cleaning advice table")

        _advice   = self.db.get_all_advice()

        for _ad in _advice:

            _users = self.db_clean.get_user_by_name(_ad.user.name)

            _new         = DD_DB_Advice()
            _new.text    = _ad.text
            _new.user    = _users[0]

            self.db_clean.session.add(_new)

    def clean_profiles(self):

        self.log.debug("cleaning profile table")

        _profiles = self.db.get_all_profiles()

        for _profile in _profiles:

            _users = self.db_clean.get_user_by_name(_profile.user.name)

            _new          = DD_DB_Profile()
            _new.badwords = _profile.badwords
            _new.admin    = _profile.admin
            _new.user     = _users[0]


            self.db_clean.session.add(_new)

    def clean_rules(self):

        self.log.debug("cleaning rule table")

        _rules    = self.db.get_all_rules()

        for _rule in _rules:

            _new         = DD_DB_Rule()
            _new.text    = _rule.text
            _new.context = _rule.context

            self.db_clean.session.add(_new)

    def clean_words(self):

        self.log.debug("cleaning word table")

        _words    = self.db.get_all_words()

        for _word in _words:

            _all_words = self.db_clean.get_word(_word.text)

            if len(_all_words) == 0:

                _new = DD_DB_Word()

                _new.text            = _word.text
                _new.tag             = _word.tag
                _new.count           = _word.count
                _new.weight_angry    = _word.weight_angry
                _new.weight_funny    = _word.weight_funny
                _new.weigth_sad      = _word.weigth_sad
                _new.weight_tehnical = _word.weight_tehnical
                _new.weight_swear    = _word.weight_swear
                _new.weight_neutral  = _word.weight_neutral
                _new.weight_greeting = _word.weight_greeting

                self.db_clean.session.add(_new)

            else:
                _all_words[0].count += _word.count