#!/usr/bin/env python3

"""
Add some documentation???
"""
import discord
from dotenv import load_dotenv
# import logging
from loguru import logger
import os
from discord.ext import commands
from nltk.chat.iesha import iesha_chatbot

load_dotenv()
logger.add('logs/chatbot-{time:YYYY-MM-DD}.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", level="INFO")

# logger = logging.getLogger('discord')
# logger.setLevel(logging.INFO)
# handler = logging.FileHandler(
#     filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter(
#     '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

TOKEN = os.getenv('TOKEN')
CHANNEL = os.getenv('CHANNEL')
SERVER = os.getenv('SERVER')

bot = commands.Bot(command_prefix="$")
channel_id = bot.get_channel(CHANNEL)


class MyClient(discord.Client):
    async def on_ready(self):
        logger.info("Logged into Discord as: {}", self.user.name)
        # print('Logged in as')
        # print(self.user.name)
        # print(self.user.id)
        # print('------')

    async def on_message(self, message):

        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            logger.info("Sent msg: {}", message.content)
            return
        else:
            logger.info("Received msg: {}", message.content)

        response = iesha_chatbot.respond(message.content)
        await message.reply(response)
        # if message.content.startswith('!hello'):
        #     logger.info("Sent msg: {}", message.content)
        #     await message.reply('Hello!', mention_author=True)


if __name__ == "__main__":
    client = MyClient()
    client.run(TOKEN)

# @bot.event
# async def on_ready():
#     print(f'We have logged in as {bot.user}')


# @bot.command()
# async def hello(ctx):
#     await ctx.send('Hello!🎉')


# @bot.command()
# async def on_message(ctx, message):
#     # we do not want the bot to reply to itself
#     if message.author.id == bot.user.id:
#         return

#     if message.content.startswith('!hello'):
#         await message.reply('Hello!', mention_author=True)

# bot.run(TOKEN)
