
import re
import asyncio
from random       import randrange
from furion_cst   import *
from furion_model import *

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class Furion_Message():

    def __init__(self,client, message):

        self.message = message
        self.client  = client
        self.guild   = None
        self.channel = None

        self.bad_words = [ "pula","pizda","ratat","ratati","muist","muisti","handicapati","masii","plm","retard","retarzi",
                            "pule","pizde","coaie","tampit","tampiti","tampita","idiot","idioata","idioti","handicapat","moara masa",
                            "tarfa", "curva", "tarfe", "curve",
                        ]

        self.__create_keywords()

        self.__get_guild()

        self.__get_channel()

    def __create_keywords(self):

        self.keywords = Furion_Message_Keywords()

        _keyword             = Furion_Message_Keyword()
        _keyword.rules       = ""
        _keyword.clbk        = self.__no_msg
        _keyword.description = None
        self.keywords.add(_keyword)

        _keyword             = Furion_Message_Keyword()
        _keyword.rules       = ["baga una de suflet"]
        _keyword.clbk        = self.__msg_1
        _keyword.description = "baga una de suflet    - iti voi da o melodie de incalzit sufletul"
        self.keywords.add(_keyword)

        # _keyword             = Furion_Message_Keyword()
        # _keyword.rules       = ["da cu furtunu"]
        # _keyword.clbk        = self.__msg_2
        # _keyword.description = "da cu furtunu            - iti arat cum sa dai cu furtunul"
        # self.keywords.add(_keyword)

        # _keyword             = Furion_Message_Keyword()
        # _keyword.rules       = [r"dota in (\d+)"]
        # _keyword.clbk        = self.__msg_3
        # _keyword.description = "dota in <minute>      - voi chema nubii la dota in cat timp imi spui"
        # self.keywords.add(_keyword)

        # _keyword             = Furion_Message_Keyword()
        # _keyword.rules       = ["badwords"]
        # _keyword.clbk        = self.__msg_4
        # _keyword.description = None
        # self.keywords.add(_keyword)

    def reply(self):

        _found = False

        _msg = self.__get_msg(self.message.content)

        if _msg != None:

            for _keyword in self.keywords:

                _match = _keyword.is_match(_msg)

                if _match != None:

                    _found = True

                    _keyword.clbk(_match)

            if not _found:

                _found = True

                self.__no_msg(None)

        return _found

    def __get_guild(self):

        for _guild in self.client.guilds:

            if _guild.name == FURION_GUILD:

                self.guild = _guild

    def __get_channel(self):

        for _channel in self.guild.text_channels:

            if _channel.name == FURION_TEXT_CHANNEL:

                self.channel = _channel

    def __get_msg(self,txt):

        _msg = None

        _match = re.match("<@%s> (.+)" % (FURION_ID,),self.message.content.strip())

        if _match:
            _msg = _match.group(1).strip()
        else:
            _match = re.match("<@%s>" % (FURION_ID,),self.message.content.strip())
            if _match:
                _msg = ""
            else:
                _match = re.match("<@!%s>" % (FURION_ID,),self.message.content.strip())
                if _match:
                    _msg = ""
                else:
                    if self.__is_bad_word(self.message.content.strip()):
                        _msg = "badwords"
                    else:
                        _msg = None

        return _msg

    def __is_bad_word(self,text):

        return any([_word in self.bad_words for _word in text.split(" ")])

    async def __no_msg(self,match):

        _selections = [
                        "ba nu ma stresa!",
                        "nu stiu ce vrei de la mine!",
                        "dute ma la somn!",
                        "boss nu te inteleg!",
                        "nu te da balena mare in apa mica!",
                        "ba tu nu ai ceva mai bun de facut?",
                        "socares mo?",
                        "ja poteca",
                      ]

        _selection = randrange(0,len(_selections))

        _commands = ""

        for _keyword in self.keywords:

            if _keyword.description != None:

                _commands += "    %s\n" % (_keyword.description, )

        await self.channel.send("%s \neu nu raspund decat la urmatoarele:\n%s" % (_selections[_selection], _commands))

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

        await self.channel.send(_selections[_selection])

    async def __msg_2(self,match):

        _selections = [
                        "https://tenor.com/view/spank-tom-and-jerry-tom-puppy-gif-5196956",
                        "https://tenor.com/view/tom-and-jerry-strong-wake-up-beat-up-gif-5963960",
                        "https://tenor.com/view/tom-and-jerry-cat-mouse-beat-funny-gif-11904883",
                        "https://tenor.com/view/kunleinho-kunleinhogifs-family-guy-beating-assault-gif-20722188",
                        "https://tenor.com/view/angry-gif-tom-and-jerry-fight-beat-gif-16739345",
                        "https://tenor.com/view/beat-wake-up-batman-stupid-slap-gif-14109387",
                      ]

        _selection = randrange(0,len(_selections))
    
        await self.channel.send(_selections[_selection])

    async def __msg_3(self,match):

        _minutes = int(match.group(1))

        for _index in range(_minutes):
            _response         = Furion_Message_Response()
            _response.text    = "@everyone %s intra la dota in %s min" % (self.author.name, _minutes - _index)
            _response.timeout = 3
            self.reply.responses.add(_response)

        _response         = Furion_Message_Response()
        _response.text    = "@everyone %s intra la dota acuma!" % (self.author.name,)
        _response.timeout = 2
        self.reply.responses.add(_response)

        self.reply.with_timer = True

        self.reply.negative_reply = "<@%s> lasa vrajeala ai zis deja in cat timp intri la dota" % (self.author.id,)

    async def __msg_4(self,match):

        await self.channel.send("<@%s> ba nu mai vorbi urat" % (self.author.id,))
