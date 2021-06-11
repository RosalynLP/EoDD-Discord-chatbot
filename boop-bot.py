"""
Test version of Discord chatbot.
Contributions:  Ewan Klein
                Rosalyn Pearson
                Helen Williams
                Andrew
                Yousef
May 2021
"""

import json
import os
import random

import discord
from dotenv import load_dotenv  # required for running locally
load_dotenv()

with open("exchanges.json", "r") as f:
    exchanges = json.load(f)

TOKEN = os.getenv('TOKEN')

client = discord.Client()


def new_topic():
    """
    Start talking about a random topic.
    """
    topics = ["wasps", "ice cream", "school", "Minecraft",
              "burgers", "hotels", "getting a suntan","books",
              "trapeze","scooters"]
    choice = random.choice(topics)  # choose a topic at random
    phrases = [f"So what do you think about {choice}?",
               f"Anyway, I really like {choice}!", f"That's really interesing but what about {choice}???"]
    phrase = choice = random.choice(phrases)
    return phrase


def respond(user_input):
    """
    Generate a response to the user input.
    """
    user_input.lower()
    words = user_input.split()
    response = new_topic()
    for word in words:
        if word in exchanges:
            responses = exchanges[word]
            response = random.choice(responses)
            break
    return response

response = await weather(WEATHER_ID, msg)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_input = message.content
    response = respond(user_input)
    await message.reply(response)


client.run(TOKEN)
