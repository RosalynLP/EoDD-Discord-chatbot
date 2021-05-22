#!/usr/bin/env python3

"""
Example of how to incorporate NLTK chat into Discord bot
"""
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from loguru import logger
from nltk.chat.iesha import iesha_chatbot

load_dotenv()
logger.add('logs/chatbot-{time:YYYY-MM-DD}.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", level="INFO")

TOKEN = os.getenv('TOKEN')
# CHANNEL = os.getenv('CHANNEL')
# SERVER = os.getenv('SERVER')

# channel_id = bot.get_channel(CHANNEL)


class MyClient(discord.Client):
    async def on_ready(self):
        logger.info("Logged into Discord as: {}", self.user.name)

    async def on_message(self, message):

        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            logger.info("Sent msg: {}", message.content)
            return
        else:
            logger.info("Received msg from {}: {}",
                        message.author, message.content)

        response = iesha_chatbot.respond(message.content)
        await message.reply(response)


if __name__ == "__main__":
    client = MyClient()
    client.run(TOKEN)
