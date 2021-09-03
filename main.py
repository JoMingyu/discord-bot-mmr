# bot.py
import os

import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv

from api import WhatIsMyMMRAPI

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

mmr_api = WhatIsMyMMRAPI()

bot = commands.Bot(command_prefix="/")


@bot.event
async def on_ready():
    print("Booting up your system")
    print(f"I am running on <{bot.user.name}>")
    print(f"With the ID: {bot.user.id}")


@bot.command("mmr")
async def on_message(ctx: Context):
    if ctx.author == bot.user:
        return

    message: discord.Message = ctx.message

    nickname = message.content.split("/mmr ", 1)[1]

    result = mmr_api.get_mmr_data(nickname)

    resp = result.as_message()

    channel: discord.TextChannel = ctx.channel

    await channel.send(resp)


bot.run(TOKEN)
