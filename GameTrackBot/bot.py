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
os.environ['JISHAKU_HIDE'] = 'True'

bot = commands.Bot(command_prefix="g/", intents=discord.Intents.all(), help_command=PrettyHelp())
bot.trackerapi = os.getenv("TRACKER_API")
ButtonsMenu.initialize(bot)
bot.help_command = PrettyHelp(color=0x220901, active=120) # specialized help command

intervals = (
    ("weeks", 604800),  # 60 * 60 * 24 * 7
    ("days", 86400),  # 60 * 60 * 24
    ("hours", 3600),  # 60 * 60
    ("minutes", 60),
    ("seconds", 1),
)


def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip("s")
            result.append("{} {}".format(value, name))
    return ", ".join(result[:granularity])

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

@bot.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        if error.retry_after < 1:
            await ctx.send(f"This command is on a `{round(error.retry_after, 2)} second` cooldown, try again later.")
            return

        fixedRetry = int(error.retry_after)
        await ctx.send(f"This command is on a `{display_time(fixedRetry)}` cooldown, try again later.")
        return

    if isinstance(error, commands.NotOwner):
        await ctx.send("You are not the bot owner.")
        return

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing arguments in your command, check g/help [command] for the arguments.")
        return

bot.run(os.getenv("DISCORD_TOKEN"), bot=True, reconnect=True)
