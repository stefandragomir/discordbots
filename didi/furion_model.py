
import re

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class Furion_Model_Base_List():

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

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class Furion_Message_Keyword():

    def __init__(self):

        self.rules       = []
        self.clbk        = None
        self.description = None

    def is_match(self,text):

        _rule_match = None

        for _rule in self.rules:

            _match = re.match(_rule,text)

            if _match != None:

                _rule_match = _match

        return _rule_match

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class Furion_Message_Keywords(Furion_Model_Base_List):

    def __init__(self):

        Furion_Model_Base_List.__init__(self)

