
import re
import enum
from sqlalchemy.orm import declarative_base
from sqlalchemy     import Column
from sqlalchemy     import Integer
from sqlalchemy     import Float
from sqlalchemy     import String
from sqlalchemy     import Boolean
from sqlalchemy     import Enum
from sqlalchemy     import ForeignKey
from sqlalchemy.orm import relationship

DD_DB_Base    = declarative_base()

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD_DB_POS_TAGS(enum.Enum):

        ADJ   = 1  #adjective
        ADP   = 2  #adposition
        ADV   = 3  #adverb
        AUX   = 4  #auxiliary
        CCONJ = 5  #coordinating conjunction
        DET   = 6  #determiner
        INTJ  = 7  #interjection
        NOUN  = 8  #noun
        NUM   = 9  #numeral
        PART  = 10 #particle
        PRON  = 11 #pronoun
        PROPN = 12 #proper noun
        PUNCT = 13 #punctuation
        SCONJ = 14 #subordinating conjunction
        SYM   = 15 #symbol
        VERB  = 16 #verb
        X     = 17 #other

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD_DB_Rule_Types(enum.Enum):

    RULE_BAD_WORD = 1
    RULE_GREETING = 2

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD_DB_Config(DD_DB_Base):

    __tablename__ = 'configs'

    id                = Column(Integer, primary_key=True)
    token             = Column(String)
    guild             = Column(String)
    channel_general   = Column(String)
    channel_links     = Column(String)
    botid             = Column(String)


    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):

        _txt =  "user: id[%s] token[%s] guild[%s] channel_general[%s] channel_links[%s] botid[%s]" % (
                                                                                                        self.id,
                                                                                                        self.token,
                                                                                                        self.guild,
                                                                                                        self.channel_general,
                                                                                                        self.channel_links,
                                                                                                        self.botid
                                                                                                    )

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

    id                = Column(Integer, primary_key=True)
    text              = Column(String)
    count             = Column(Integer)
    tag               = Column(Enum(DD_DB_POS_TAGS))
    weight_angry      = Column(Float)
    weight_funny      = Column(Float)
    weigth_sad        = Column(Float)
    weight_tehnical   = Column(Float)
    weight_swear      = Column(Float)
    weight_neutral    = Column(Float)
    weight_greeting   = Column(Float)

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