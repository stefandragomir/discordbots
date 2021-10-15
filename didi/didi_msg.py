
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
        _keyword.rules       = ["baga una de suflet"]
        _keyword.clbk        = self.__msg_1
        _keyword.description = "baga una de suflet    - iti voi da o melodie de incalzit sufletul"
        self.keywords.add(_keyword)

        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["link spdp"]
        _keyword.clbk        = self.__msg_2
        _keyword.description = "link spdp    -  afisez linkul de la SPDP"
        self.keywords.add(_keyword)

        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["link ematrix"]
        _keyword.clbk        = self.__msg_3
        _keyword.description = "link ematrix    -  afisez linkul de la EMatrix"
        self.keywords.add(_keyword)

        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["link mht"]
        _keyword.clbk        = self.__msg_4
        _keyword.description = "link mht    -  afisez linkul de la Man Hour Tracking"
        self.keywords.add(_keyword)

        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["link odoo"]
        _keyword.clbk        = self.__msg_5
        _keyword.description = "link odoo    -  afisez linkul de la Odoo"
        self.keywords.add(_keyword)

        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["link it"]
        _keyword.clbk        = self.__msg_6
        _keyword.description = "link it    -  afisez linkul de la Ticket IT"
        self.keywords.add(_keyword)

        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["link gitlab"]
        _keyword.clbk        = self.__msg_7
        _keyword.description = "link gitlab    -  afisez linkul de la Gitlab"
        self.keywords.add(_keyword)

        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["link review"]
        _keyword.clbk        = self.__msg_8
        _keyword.description = "link review    -  afisez linkul de la Review"
        self.keywords.add(_keyword)

        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["link tutoriale"]
        _keyword.clbk        = self.__msg_9
        _keyword.description = "link tutoriale    -  afisez linkul de la Software Tools Tutorials"
        self.keywords.add(_keyword)

        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["link asset"]
        _keyword.clbk        = self.__msg_10
        _keyword.description = "link asset    -  afisez linkul de la Asset Management"
        self.keywords.add(_keyword)

        _keyword             = DD_Message_Keyword()
        _keyword.rules       = ["link sharepoint"]
        _keyword.clbk        = self.__msg_10
        _keyword.description = "link sharepoint    -  afisez linkul de la Software Tools Sharepoint"
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
        else:
            _match = re.match("<@%s>" % (self.parent.config.bot_id,),self.message.content.strip())
            if _match:
                _msg = ""
            else:
                _match = re.match("<@!%s>" % (self.parent.config.bot_id,),self.message.content.strip())
                if _match:
                    _msg = ""
                else:
                    if self.__is_bad_word(self.message.content.strip()):
                        _msg = "badwords"
                    else:
                        _msg = None

        return _msg

    def __is_bad_word(self,text):

        return any([_word in self.parent.config.bad_words for _word in text.split(" ")])

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

        _selections = [
                        "https://www.youtube.com/watch?v=Kg8QrGZKuuE&ab_channel=AmmaMusic%26Sound",
                        "https://www.youtube.com/watch?v=NQ4tCQcCFJY&ab_channel=NekMusicTv",
                        "https://www.youtube.com/watch?v=DEja1ZLWCMM&ab_channel=DaniMocanu%C2%A9Oficial",
                        "https://www.youtube.com/watch?v=U9gGbDEDrv0&ab_channel=FortzaManele",
                        "https://www.youtube.com/watch?v=TsUxWZeFCw8&ab_channel=DaniMocanu%C2%A9Oficial",
                        "https://www.youtube.com/watch?v=XTKKj0CX3yQ&ab_channel=AmmAMusic%26Sound",
                        "https://www.youtube.com/watch?v=ynT2aiOhjt4&t=1s&ab_channel=JeandelaCraiova",

                      ]

        _selection = randrange(0,len(_selections))

        await self.parent.send_message(_selections[_selection])

    async def __msg_2(self,match):

        await self.parent.send_message("http://intranet-eibu.yazaki-europe.com/spdp/")

    async def __msg_3(self,match):

        await self.parent.send_message("https://matrix.yazaki-europe.com/ematrix")

    async def __msg_4(self,match):

        await self.parent.send_message("https://mht.yazaki-europe.com/mht/Account/LogOn#/persons/view")

    async def __msg_5(self,match):

        await self.parent.send_message("http://10.50.4.223:8069/")

    async def __msg_6(self,match):

        await self.parent.send_message("https://yelprod.service-now.com/sp?id=ticket&is_new_order=true&table=incident&sys_id=528a5a681b950c10698ec8017e4bcbd7")

    async def __msg_7(self,match):

        await self.parent.send_message("http://10.50.4.223:11011/")

    async def __msg_8(self,match):

        await self.parent.send_message("http://10.50.4.223:22022/")

    async def __msg_9(self,match):

        await self.parent.send_message("https://web.microsoftstream.com/group/1adfb544-9161-4b83-b224-9c27606ce7bd")

    async def __msg_10(self,match):

        await self.parent.send_message("http://yctt-f01.yel.yazaki.local/trac/yct-t-assets")

    async def __msg_11(self,match):

        await self.parent.send_message("https://yazaki.sharepoint.com/sites/SoftwareTools")

