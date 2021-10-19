
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy     import create_engine
from sqlalchemy     import Column
from sqlalchemy     import Integer
from sqlalchemy     import String
from sqlalchemy     import Boolean
from sqlalchemy     import ForeignKey
from sqlalchemy.orm import relationship

DD_DB_Base    = declarative_base()


'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD_DB_Config(DD_DB_Base):

    __tablename__ = 'config'

    id        = Column(Integer, primary_key=True)
    token     = Column(String)
    guild     = Column(String)
    channel   = Column(String)
    botid     = Column(String)


    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):

        _txt =  "user: token[%s] guild[%s] channel[%s] botid[%s]" % (self.token,self.guild,self.channel,self.botid)

        return _txt

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD_DB_User(DD_DB_Base):

    __tablename__ = 'users'

    id       = Column(Integer, primary_key=True)
    name     = Column(String)
    uid      = Column(Integer)
    profile  = 


    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):

        _txt =  "user: id[%s] name[%s] admin[%s] uid[%s]" % (self.id,self.name,self.admin,self.uid)

        return _txt

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD_DB_Advice(DD_DB_Base):

    __tablename__ = 'advice'

    id       = Column(Integer, primary_key=True)
    text     = Column(String)
    user_id  = Column(Integer, ForeignKey('users.id'))
    user     = relationship("DD_DB_User")

    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):

        _txt =  "advice: id[%s] text[%s] user[%s]" % (self.id,self.text,self.user.name)

        return _txt

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD_DB_User_Profile(DD_DB_Base):

    __tablename__ = 'users'

    id       = Column(Integer, primary_key=True)
    badwords = Column(Integer)
    admin    = Column(Boolean)
    user_id  = Column(Integer, ForeignKey('users.id'))
    user     = relationship("DD_DB_User",back_populates="profile")


    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):

        _txt =  "user: id[%s] name[%s] admin[%s] uid[%s]" % (self.id,self.name,self.admin,self.uid)

        return _txt


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

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
_db = DD_DB(r"c:\temp\dbg.db")

_db.connect()

