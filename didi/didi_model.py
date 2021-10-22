
import re
import enum
from sqlalchemy.orm import declarative_base
from sqlalchemy     import Column
from sqlalchemy     import Integer
from sqlalchemy     import String
from sqlalchemy     import Boolean
from sqlalchemy     import Enum
from sqlalchemy     import ForeignKey
from sqlalchemy.orm import relationship

DD_DB_Base    = declarative_base()

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD_DB_Rule_Types(enum.Enum):

    RULE_BAD_WORD = 1
    RULE_HELLO    = 2
    RULE_GOODBY   = 3

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD_DB_Config(DD_DB_Base):

    __tablename__ = 'configs'

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

        _txt =  "user: id[%s] token[%s] guild[%s] channel[%s] botid[%s]" % (self.id,self.token,self.guild,self.channel,self.botid)

        return _txt

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD_DB_User(DD_DB_Base):

    __tablename__ = 'users'

    id       = Column(Integer, primary_key=True)
    name     = Column(String)
    uid      = Column(Integer)


    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):

        _txt =  "user: id[%s] name[%s] uid[%s]" % (self.id,self.name,self.uid)

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
class DD_DB_Profile(DD_DB_Base):

    __tablename__ = 'profiles'

    id       = Column(Integer, primary_key=True)
    badwords = Column(Integer)
    admin    = Column(Boolean)
    user_id  = Column(Integer, ForeignKey('users.id'))
    user     = relationship("DD_DB_User")


    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):

        _txt =  "user: id[%s] badwords[%s] admin[%s] user[%s]" % (self.id,self.badwords,self.admin,self.user.name)

        return _txt

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD_DB_Rule(DD_DB_Base):

    __tablename__ = 'rules'

    id       = Column(Integer, primary_key=True)
    text     = Column(String)
    context  = Column(Enum(DD_DB_Rule_Types))


    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):

        _txt =  "user: id[%s] text[%s] context[%s] " % (self.id,self.text,self.context)

        return _txt

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD_DB_Word(DD_DB_Base):

    __tablename__ = 'words'

    id       = Column(Integer, primary_key=True)
    text     = Column(String)
    count    = Column(Integer)


    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):

        _txt =  "user: id[%s] text[%s] count[%s] " % (self.id,self.text,self.count)

        return _txt

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD_Model_Base_List():

    def __init__(self):

        self.objects = []

    def add(self,obj):

        self.objects.append(obj)  

    def remove(self,obj):

        self.objects.remove(obj)  

    def remove_by_attribute(self,attribute,value):

        _item = self.find_by_attribute(attribute,value)

        if _item != None:

            self.remove(_item)

    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):

        _txt = ""
        
        for obj in self.objects:

            _txt += str(obj)

        return _txt

    def __iter__(self):

        for obj in self.objects:

            yield obj

    def __getitem__(self,index):

        return self.objects[index]

    def __len__(self):

        return len(self.objects)

    def find_by_attribute(self,attribute,value):

        _object = None

        for _obj in self.objects:

            if getattr(_obj,attribute) == value:

                _object = _obj

        return _object

    def __add__(self,other):

        self.objects += other.objects

        return self

    def reverse(self):

        self.objects.reverse()