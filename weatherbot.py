"""
Demo version of Discord weather bot

Sprint 2 of Emporium of Digital Delights, June 2021

Team: Boop Fire Storm

Authors:        Zain
                Yousef
                Rory

Contributions:  Rosalyn Pearson
                Helen Williams
                Andrew
                Ewan Klein

 
Last edited: 11 Jun 2021
"""
import json

from aiohttp import ClientSession
from discord.ext import commands
from os import getenv
from random import choice
#from loguru import logger

# required for running locally
from dotenv import load_dotenv
load_dotenv()

TOKEN = getenv('TOKEN')
WEATHER_ID = getenv('WEATHER_ID')

class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aiohttpsession = None

    async def login(self, *args, **kwargs):
        self.aiohttpsession = ClientSession()
        await super().login(*args, **kwargs)

    async def close(self):
        await super().close()
        if self.aiohttpsession:
            await self.aiohttpsession.close()


bot = Bot(command_prefix="$")

with open("exchanges.json", "r") as f:
    exchanges = json.load(f)
sessions = []
conversations = {}

# TODO: access the weather API and return information
# Docs for weather API: https://openweathermap.org/current
async def weather(appid, msg):
    async with msg.channel.typing():
        ans = "Accessing weather API"
    return ans


def new_topic():
    """
    Start talking about a random topic.
    """
    topics = ["wasps", "ice cream", "school", "Fortnite",
              "burgers", "hotels", "getting a suntan"]
    topic = choice(topics)  # choose a topic at random
    phrases = [f"So what do you think about {topic}?",
               f"Anyway, I really like {topic}!", f"That's really interesing but what about {topic}???"]
    phrase = choice(phrases)
    return phrase


async def respond(msg):
    """
    Generate a response to the user input.
    """
    user_input = msg.content.lower()
    words = user_input.split()
    response = responsecopy = new_topic()
    for word in words:
        if word in exchanges:
            responses = exchanges[word]
            response = choice(responses)
            break
    if response == responsecopy:
        try:
            response = await weather(WEATHER_ID, msg)
        except ValueError:
            pass
    return response


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command()
async def hello(ctx):
    """Starts a new chatbot session"""
    if ctx.author.id not in sessions:
        sessions.append(ctx.author.id)
        await ctx.reply("Hello, nice to meet you!")
    else:
        await ctx.reply("There is already an ongoing bot session!")


@bot.command()
async def bye(ctx):
    """Exits the chatbot session"""
    if ctx.author.id in sessions:
        sessions.remove(ctx.author.id)
        await ctx.reply("It was nice chatting to you!")
    else:
        await ctx.reply("There is no active bot session!")


@bot.event
async def on_message(msg):
    if (await bot.get_context(msg)).valid:
        await bot.process_commands(msg)
        return  # Exit if the message invokes another command

    if msg.author.id in sessions:
        await msg.reply(await respond(msg))


bot.run(TOKEN)

