#!/usr/bin/python
# -*- coding: utf-8 -*-
# bot.py

# Main bot file for GameTrackBot.


# Python imports
import asyncio
import os

# External libs
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from pretty_help import PrettyHelp
from reactionmenu import ButtonsMenu, ComponentsButton

load_dotenv() # get tokens stored in .env

bot = commands.Bot(command_prefix="g/", intents=discord.Intents.all(), help_command=PrettyHelp())
bot.trackerapi = os.getenv("TRACKER_API")
bot.developer = bot.fetch_user(390841378277425153)
ButtonsMenu.initialize(bot)
bot.help_command = PrettyHelp(color=0x220901, active=120) # specialized help command

# seperate game cogs (only doing r6 for now, will do others)
if __name__ == "__main__":
    for extension in [
        "cogs.dev",
        "cogs.botinfo",
        "cogs.siege",
        "cogs.csgo",
        "jishaku"
    ]:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print("Bot is online.")


bot.run(os.getenv("DISCORD_TOKEN"), bot=True, reconnect=True)
