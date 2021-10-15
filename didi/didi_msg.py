
import re
import asyncio
from random       import randrange
from didi_model   import *

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
        _keyword.rules       = ""
        _keyword.clbk        = self.__no_msg
        _keyword.description = None
        self.keywords.add(_keyword)
        
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

    async def reply(self):

        _found = False

        _msg = self.__get_msg(self.message.content)

        if _msg != None:

            for _keyword in self.keywords:

                _match = _keyword.is_match(_msg)

                if _match != None:

                    _found = True

                    await _keyword.clbk(_match)

            if not _found:

                _found = True

                await self.__no_msg(None)

        return _found

    def __get_msg(self,txt):

        _msg = None

        _match = re.match("<@%s> (.+)" % (self.parent.config.bot_id,),self.message.content.strip())

        if _match:
            _msg = _match.group(1).strip()
        elif re.match("<@%s>" % (self.parent.config.bot_id,),self.message.content.strip()):
            _msg = ""
        elif re.match("<@!%s>" % (self.parent.config.bot_id,),self.message.content.strip()):
            _msg = ""
        elif self.__is_bad_word(self.message.content.strip()):
            _msg = "badwords"
        elif self.__is_hello(self.message.content.strip()):
            _msg = "hello"
        elif self.__is_goodbye(self.message.content.strip()):
            _msg = "goodbye"
        else:
            _msg = None

        return _msg

    def __is_bad_word(self,text):

        return any([None != re.search(r"%s|%s\s|\s%s" % (_rule,_rule,_rule),text.lower()) for _rule in self.parent.config.rule_bad_words])

    def __is_hello(self,text):

        return any([None != re.search(r"%s|%s\s|\s%s" % (_rule,_rule,_rule),text.lower()) for _rule in self.parent.config.rule_hello])

    def __is_goodbye(self,text):

        return any([None != re.search(r"%s|%s\s|\s%s" % (_rule,_rule,_rule),text.lower()) for _rule in self.parent.config.rule_goodbye])

    async def __no_msg(self,match):

        _selections = [
                        "ba nu ma stresa!",
                        "nu stiu ce vrei de la mine!",
                        "boss nu te inteleg!",
                        "ba tu nu ai ceva mai bun de facut?",
                        "socares mo?",
                        "ja poteca",
                      ]

        _selection = randrange(0,len(_selections))

        _commands = ""

        for _keyword in self.keywords:

            if _keyword.description != None:

                _commands += "    %s\n" % (_keyword.description, )

        await self.parent.send_message("%s \neu nu raspund decat la urmatoarele:\n%s" % (_selections[_selection], _commands))

    async def __msg_1(self,match):

        await self.parent.send_message("<@%s> ba nu mai vorbi urat" % (self.message.author.id,))

    async def __msg_2(self,match):

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

    async def __msg_3(self,match):

        _selections = [
                        "nu da cu piatra in geam ca nu e bicicleta ta",
                        "daca nu faci nimic, nu strici nimic",
                        "daca ceva merge, nu il repara",
                        "cine sapara groapa altuia, departe ajunge",
                        "daca nu ai enervat pe nimeni, inseamna ca nu ai facut nimic",
                        "orice cacat faci, sa il ambalezi frumos",
                        "nu te certa cu prostii, ca au mai multa experienta",
                        "nu uita ca e ilegal sa omori alti oameni",
                      ]

        _selection = randrange(0,len(_selections))
    
        await self.parent.send_message(_selections[_selection])

    async def __msg_4(self,match):

        await self.parent.send_message(":wave:  <@%s>" % (self.message.author.id,))

    async def __msg_5(self,match):

        await self.parent.send_message(":wave:  <@%s>" % (self.message.author.id,))
