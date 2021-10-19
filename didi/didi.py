
import sys
import os
import discord
from argparse      import ArgumentParser
from didi_msg      import DD_Message
from didi_logger   import DD_Logger
from didi_db       import DD_DB


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

        self.arg.add_argument('--run',          action='store_true',  help='run didi on default configuration')
        self.arg.add_argument('--debug',        action='store_true',  help='option to run on debug guild')
        self.arg.add_argument('--log',          action='store_true',  help='option to log everything that happens')

    def _parse_arguments(self):

        return self.arg.parse_args()

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD():

    def __init__(self):

        self.db        = DD_DB(r"c:\temp\didi.db")
        self.client    = discord.Client()
        self.log       = DD_Logger()
        self.guild     = None
        self.channel   = None
        self.arg       = DD_Arguments()

    async def connect(self):

        self.get_guild()

        self.get_channel()

        if self.guild != None and self.channel != None:

            self.log.info("didi connected to guild [%s] channel [%s]" % (self.guild.name,self.channel))

        else:
            self.log.info("didi could not connect to guild [%s] channel [%s]" % (self.guild.name,self.channel))

    async def disconnect(self):

        self.log.info("didi disconnected from guild [%s] channel [%s]" % (self.guild.name,self.channel))

    def execute(self):

        if self.arg.arguments.run:

            self.run(self.arg.arguments.debug,self.arg.arguments.log)

    def run(self,debug,log):

        self.db.connect()

        # self.client.run(self.config.bot_token)

    def get_guild(self):

        for _guild in self.client.guilds:

            if _guild.name == self.config.guild_name:

                self.guild = _guild

    def get_channel(self):

        for _channel in self.guild.text_channels:

            if _channel.name == self.config.channel_name:

                self.channel = _channel

    async def send_message(self,text):

        await self.channel.send(text)

    async def on_message(self,message):

        _msg = DD_Message(self,message)

        await _msg.reply()

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