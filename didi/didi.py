
import sys
import os
import discord
from argparse      import ArgumentParser
from didi_msg      import DD_Message_General
from didi_msg      import DD_Message_Links
from didi_logger   import DD_Logger
from didi_db       import DD_DB
from didi_db       import DD_Clean_DB
from didi_model    import *  

#pip install discord.py==1.7.3

"""*************************************************************************************************
****************************************************************************************************
*************************************************************************************************"""
class DD_Arguments(object):

    arguments = None

    def __init__(self):

        self.arg = ArgumentParser()

        self._add_arguments()

        self.arguments = self._parse_arguments()

    def _add_arguments(self):

        self.arg.add_argument('--run',        type=str,            help='run didi on specified configuration')
        self.arg.add_argument('--init',       action='store_true', help='create empty didi db')
        self.arg.add_argument('--keywords',   action='store_true', help='show all didi defined keywords')
        self.arg.add_argument('--clean',      action='store_true', help='clean the database')

    def _parse_arguments(self):

        return self.arg.parse_args()

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD():

    def __init__(self):

        self.db               = DD_DB(self.get_db_path())
        self.client           = discord.Client()
        self.log              = DD_Logger(self.get_log_path())
        self.config           = None
        self.guild            = None
        self.channel_general  = None
        self.channel_links    = None
        self.arg              = DD_Arguments()

    async def connect(self):

        self.get_guild()

        self.get_channels()

        if self.guild != None and self.channel_general != None and self.channel_links != None:

            self.log.info("didi connected to guild [%s] channel general [%s] channel links [%s]" % (self.guild.name,self.channel_general,self.channel_links))

        else:
            self.log.info("didi could not connect to guild [%s] channel general [%s] channel links [%s]" % (self.guild.name,self.channel_general,self.channel_links))

    async def disconnect(self):

        self.log.info("didi disconnected from guild [%s] channel general [%s] channel links [%s]" % (self.guild.name,self.channel_general,self.channel_links))

    def execute(self):

        if self.arg.arguments.run != None:

            self.run(self.arg.arguments.run)

        elif self.arg.arguments.init:

            self.init()

        elif self.arg.arguments.keywords:

            self.keywords()

        elif self.arg.arguments.clean:

            self.clean()

    def run(self,index):

        index = int(index)

        self.db.connect()

        _configurations = self.db.get_all_config()

        if index <= len(_configurations) - 1:
            self.config = _configurations[index]
        else:
            self.config = None
            self.log.error("configuration [%s] does not exist in db" % (index,))

        if self.config != None:

            self.log.debug("running didi with configuration [%s]" % (index,))

            self.client.run(self.config.token)

    def init(self):

        self.db.connect()

        self.db.create_empty()

    def keywords(self):

        _keywords = [_keyword for _keyword in DD_Message(self,None).keywords]

        print("KEYWORDS:")

        for _keyword in _keywords:

            print("   ",_keyword.rules)  

    def clean(self):

        _clean = DD_Clean_DB(self.get_db_path(), self.get_clean_db_path(), self.log)

        _clean.run()

    def get_guild(self):

        self.log.debug("searching for guild [%s]" % (self.config.guild,))

        for _guild in self.client.guilds:

            if _guild.name == self.config.guild:

                self.guild = _guild

                self.log.debug("found for guild [%s]" % (self.config.guild,))

    def get_channels(self):

        self.log.debug("searching for channel general [%s]" % (self.config.channel_general,))

        for _channel in self.guild.text_channels:

            if _channel.name == self.config.channel_general:

                self.channel_general = _channel

                self.log.debug("found channel [%s]" % (self.config.channel_general,))

        self.log.debug("searching for channel links [%s]" % (self.config.channel_links,))

        for _channel in self.guild.text_channels:

            if _channel.name == self.config.channel_links:

                self.channel_links = _channel

                self.log.debug("found channel [%s]" % (self.config.channel_links,))

    async def send_message_to_general(self,text):

        await self.channel_general.send(text)

    async def send_message_to_links(self,text):

        await self.channel_links.send(text)

    async def delete_message_from_links(self,message):

        await self.channel_links.delete_messages([message])

    async def on_message(self,message):

        if message.channel.name == self.channel_general.name:

            _msg = DD_Message_General(self,message)

            await _msg.reply()

        if message.channel.name == self.channel_links.name:

            _msg = DD_Message_Links(self,message)

            await _msg.reply()

    def get_settings_dir(self):

        _path = os.path.join(os.path.expanduser("~"),".didi")

        if not os.path.exists(_path):
            
            os.mkdir(_path)  
            os.mkdir(os.path.join(_path,"db"))
            os.mkdir(os.path.join(_path,"log"))

        return _path

    def get_db_path(self):

        return os.path.join(self.get_settings_dir(),"db","didi.db")

    def get_clean_db_path(self):

        return os.path.join(self.get_settings_dir(),"db","didi_clean.db")

    def get_log_path(self):

        return os.path.join(self.get_settings_dir(),"log","didi.log")

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''

didi = DD()

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
@didi.client.event
async def on_ready():

    await didi.connect()

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
@didi.client.event
async def on_disconnect():

    await didi.disconnect()

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
@didi.client.event
async def on_message(message):

    await didi.on_message(message)

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
didi.execute()