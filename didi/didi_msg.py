
import re
import asyncio
from random       import randrange
from didi_model   import DD_Model_Base_List

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD_Message_Keyword():

    def __init__(self):

        self.rules       = []
        self.clbk        = None
        self.description = None

    def is_match(self,text):

        _status = False

        for _rule in self.rules:

            _match = re.match(_rule,text)

            if _match != None:

                _status = True

        return _status

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD_Message_Keywords(DD_Model_Base_List):

    def __init__(self):

        DD_Model_Base_List.__init__(self)

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD_Message():

    def __init__(self,parent, message):

        self.parent  = parent
        self.message = message

        self.__create_keywords()

    def __create_keywords(self):

        self.keywords = DD_Message_Keywords()
        
        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["badwords"]
        _keyword.clbk        = self.__msg_1
        _keyword.description = None
        self.keywords.add(_keyword)

        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["link"]
        _keyword.clbk        = self.__msg_2
        _keyword.description = "link -  afisez linkul pentru saracii din Yazaki"
        self.keywords.add(_keyword)

        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["sfat"]
        _keyword.clbk        = self.__msg_3
        _keyword.description = "sfat -  dau un sfat de viata"
        self.keywords.add(_keyword)

        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["hello"]
        _keyword.clbk        = self.__msg_4
        _keyword.description = None
        self.keywords.add(_keyword)

        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["goodbye"]
        _keyword.clbk        = self.__msg_5
        _keyword.description = None
        self.keywords.add(_keyword)

        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["help"]
        _keyword.clbk        = self.__help
        _keyword.description = None

        self.keywords.add(_keyword)
        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["tine minte"]
        _keyword.clbk        = self.__msg_6
        _keyword.description = None
        self.keywords.add(_keyword)
        
        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["scor"]
        _keyword.clbk        = self.__msg_7
        _keyword.description = "scor -  cat de des s-a injurat"
        self.keywords.add(_keyword)

    async def reply(self):

        self.__record(self.message.content)

        _msg = self.__get_msg(self.message.content)

        if _msg != None:

            for _keyword in self.keywords:

                if _keyword.is_match(_msg):

                    await _keyword.clbk(_msg)

    def __record(self,text):

        _words = text.split(" ")

        for _word in _words:

            _word = _word.strip()

            if _word != "":

                self.parent.db.add_word(_word)



    def __get_msg(self,txt):

        _msg = None

        _match = re.match("<@%s> (.+)" % (self.parent.config.botid,),self.message.content.strip())

        if self.__is_bad_word(self.message.content.strip()):
            _msg = "badwords"
        elif _match:
            _msg = _match.group(1).strip()
        elif re.match("<@%s>" % (self.parent.config.botid,),self.message.content.strip()):
            _msg = ""
        elif re.match("<@!%s>" % (self.parent.config.botid,),self.message.content.strip()):
            _msg = ""
        elif self.__is_hello(self.message.content.strip()):
            _msg = "hello"
        elif self.__is_goodbye(self.message.content.strip()):
            _msg = "goodbye"
        else:
            _msg = None

        return _msg

    def __is_bad_word(self,text):

        _rules = [_rule.text for _rule in self.parent.db.get_rules_badwords()]        

        return any([None != re.search(r"%s|%s\s|\s%s" % (_rule,_rule,_rule),text.lower()) for _rule in _rules])

    def __is_hello(self,text):

        _rules = [_rule.text for _rule in self.parent.db.get_rules_hello()]

        return any([None != re.search(r"%s|%s\s|\s%s" % (_rule,_rule,_rule),text.lower()) for _rule in _rules])

    def __is_goodbye(self,text):

        _rules = [_rule.text for _rule in self.parent.db.get_rules_goodbye()]

        return any([None != re.search(r"%s|%s\s|\s%s" % (_rule,_rule,_rule),text.lower()) for _rule in _rules])

    async def __help(self,msg):

        _commands = ""

        for _keyword in self.keywords:

            if _keyword.description != None:

                _commands += "    %s\n" % (_keyword.description, )

        await self.parent.send_message("eu raspund decat la urmatoarele:\n%s" % (_commands,))

    async def __msg_1(self,msg):

        self.parent.db.increment_badword(self.message.author.id)

        await self.parent.send_message("<@%s> ba nu mai vorbi urat" % (self.message.author.id,))

    async def __msg_2(self,msg):

        _links = """
        SPDP - http://intranet-eibu.yazaki-europe.com/spdp/
        EMATRIX - https://matrix.yazaki-europe.com/ematrix
        MHT - https://mht.yazaki-europe.com/mht/Account/LogOn#/persons/view
        ODOO - http://10.50.4.223:8069/
        IT TICKET - https://yelprod.service-now.com/sp?id=ticket&is_new_order=true&table=incident&sys_id=528a5a681b950c10698ec8017e4bcbd7
        GITLAB - http://10.50.4.223:11011/
        REVIEW TOOL - http://10.50.4.223:22022/
        VIDEO TUTORIALS - https://web.microsoftstream.com/group/1adfb544-9161-4b83-b224-9c27606ce7bd
        ASSET MANAGEMENT - http://yctt-f01.yel.yazaki.local/trac/yct-t-assets
        SW TOOLS SHARE POINT - https://yazaki.sharepoint.com/sites/SoftwareTools
        """

        await self.parent.send_message(_links)

    async def __msg_3(self,msg):

        _selections = [_advice.text for _advice in self.parent.db.get_all_advice()]

        _selection = randrange(0,len(_selections))
    
        await self.parent.send_message(_selections[_selection])

    async def __msg_4(self,msg):

        await self.parent.send_message(":wave:  <@%s>" % (self.message.author.id,))

    async def __msg_5(self,msg):

        await self.parent.send_message(":wave:  <@%s>" % (self.message.author.id,))

    async def __msg_6(self,msg):

        _match = re.match("tine minte (.+)",msg)

        if _match != None:

            _advice = _match.group(1)

            _profile = self.parent.db.get_user_profile_by_uid(self.message.author.id)

            if _profile != None:

                if _profile.admin:

                    self.parent.db.add_advice(_advice,self.message.author.id)

                    _reply = "am sa tin minte asta <@%s>" % (self.message.author.id,)
                else:
                    _reply = "nu iau sfaturi de la tine <@%s>" % (self.message.author.id,)
            else:
                _reply = "nu iau sfaturi de la tine <@%s>" % (self.message.author.id,)
        else:
            _reply = "sa tin minte ce? ca nu mi-ai spus nimic <@%s>" % (self.message.author.id,)

        await self.parent.send_message(_reply)

    async def __msg_7(self,msg):

        _reply = ""

        _profiles = self.parent.db.get_all_profiles()

        _profiles.sort(reverse=False,key=lambda profile: profile.badwords)

        _count = 1

        for _profile in _profiles:

            if _count == 1:
                _emoji = ":first_place:"
            elif _count == 2:
                _emoji = ":second_place:"
            elif _count == 3:
                _emoji = ":third_place:"
            elif _count == len(_profiles):
                _emoji = ":angry:"
            else:
                _emoji = ":confused:"

            _reply += "%s %s - %s injuraturi\n\n" % (_emoji, _profile.user.name, _profile.badwords)

            _count += 1

        await self.parent.send_message(_reply)