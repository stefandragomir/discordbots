
import sys
import os
import discord

from didi_msg      import DD_Message
from didi_logger   import DD_Logger
from didi_config   import DD_Config


'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
class DD():

    def __init__(self):

        self.config    = DD_Config()
        self.client    = discord.Client()
        self.log       = DD_Logger()
        self.guild     = None
        self.channel   = None

    def connect(self):

        self.get_guild()

        self.get_channel()

        if self.guild != None and self.channel != None:

            self.log.info("didi connected tto guild [%s] channel [%s]" % (self.guild.name,self.channel))

        else:
            self.log.info("didi could not connect to guild [%s] channel [%s]" % (self.guild.name,self.channel))

    def disconnect(self):

        self.log.info("didi disconnected from guild [%s] channel [%s]" % (self.guild.name,self.channel))

    def run(self):

        self.client.run(self.config.bot_token)

    def get_guild(self):

        for _guild in self.client.guilds:

            if _guild.name == self.config.guild_name:

                self.guild = _guild

    def get_channel(self):

        for _channel in self.guild.text_channels:

            if _channel.name == self.config.channel_name:

                self.channel = _channel

    async def on_message(self,message):

        DD_Message(self,message).reply()

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''

didi = DD()

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
@didi.client.event
async def on_ready():

    didi.connect()

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
@didi.client.event
async def on_disconnect():

    didi.disconnect()

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
@didi.client.event
async def on_message(message):

    didi.on_message(message)

'''********************************************************************************************************
***********************************************************************************************************
********************************************************************************************************'''
didi.run()