
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
class DD_Message_General():

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
        _keyword.rules       = ["greeting"]
        _keyword.clbk        = self.__msg_4
        _keyword.description = None
        self.keywords.add(_keyword)

        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["help"]
        _keyword.clbk        = self.__help
        _keyword.description = None

        self.keywords.add(_keyword)
        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["tine minte"]
        _keyword.clbk        = self.__msg_5
        _keyword.description = None
        self.keywords.add(_keyword)
        
        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["scor"]
        _keyword.clbk        = self.__msg_6
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

        _words = re.findall("[a-zA-Z/-]+",text)

        for _word in _words:

            _word = _word.strip()

            if _word != "":

                self.parent.db.add_word(_word)

    def __get_msg(self,txt):

        _msg = None

        _match = re.match("<@&%s> (.+)" % (self.parent.config.botid,),self.message.content.strip())

        if self.__is_bad_word(self.message.content.strip()):
            _msg = "badwords"
        elif _match:
            _msg = _match.group(1).strip()
        elif re.match("<@%s>" % (self.parent.config.botid,),self.message.content.strip()):
            _msg = ""
        elif re.match("<@!%s>" % (self.parent.config.botid,),self.message.content.strip()):
            _msg = ""
        elif self.__is_greeting(self.message.content.strip()):
            _msg = "greeting"
        else:
            _msg = None

        return _msg

    def __is_bad_word(self,text):

        _rules = [_rule.text for _rule in self.parent.db.get_rules_badwords()]        

        return any([None != re.search(r"%s|%s\s|\s%s" % (_rule,_rule,_rule),text.lower()) for _rule in _rules])

    def __is_greeting(self,text):

        _rules = [_rule.text for _rule in self.parent.db.get_rules_greeting()]

        return any([None != re.search(r"%s|%s\s|\s%s" % (_rule,_rule,_rule),text.lower()) for _rule in _rules])

    async def __help(self,msg):

        _commands = ""

        for _keyword in self.keywords:

            if _keyword.description != None:

                _commands += "    %s\n" % (_keyword.description, )

        _text = "#general este canalul de discutii. comenzi didi pentru #general:\n%s" % (_commands,)

        await self.parent.send_message_to_general(_text)

    async def __msg_1(self,msg):

        self.parent.db.increment_badword(self.message.author.id)

        await self.parent.send_message_to_general("<@%s> nu mai vorbi urat" % (self.message.author.id,))

    async def __msg_2(self,msg):

        await self.parent.send_message_to_general("")

    async def __msg_3(self,msg):

        _selections = [_advice.text for _advice in self.parent.db.get_all_advice()]

        _selection = randrange(0,len(_selections))
    
        await self.parent.send_message_to_general(_selections[_selection])

    async def __msg_4(self,msg):

        await self.parent.send_message_to_general(":wave:  <@%s>" % (self.message.author.id,))

    async def __msg_5(self,msg):

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

        await self.parent.send_message_to_general(_reply)

    async def __msg_6(self,msg):

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

        await self.parent.send_message_to_general(_reply)

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD_Message_Links():

    def __init__(self,parent, message):

        self.parent  = parent
        self.message = message

    async def reply(self):

        _status = self.__check_msg(self.message.content)

        if not _status:

            await self.parent.delete_message_from_links(self.message)

            self.parent.log.error("incorect message added in links: %s by %s" % (self.message.content,self.message.author.id))

    def __check_msg(self,txt):

        _msg = None

        print(self.message.content.strip())

        _match = re.match(r"^(https|http)\:\/\/.+", self.message.content.strip())

        return _match != None
