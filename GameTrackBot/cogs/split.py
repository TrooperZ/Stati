#!/usr/bin/python
# -*- coding: utf-8 -*-
# split.py

# Splitgate stats for GameTrackBot.


import discord
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv
import os
import aiohttp
import asyncio
import json
from pprint import pprint
from reactionmenu import ButtonsMenu, ComponentsButton
import urllib.parse

load_dotenv()

class splitgate(commands.Cog):
    """CS:GO Stats"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=5, per=5, type=commands.BucketType.user)
    async def csgostats(self, ctx, *, user: str):
        """Fetch general stats for a CS:GO user via Steam name or Steam integer ID."""
        urllib.parse.quote(user)
        async with aiohttp.ClientSession(headers={'TRN-Api-Key': os.getenv('TRACKER_API')}) as session:
            async with session.get(f"https://public-api.tracker.gg/v2/csgo/standard/profile/steam/{user}") as response:
                data1 = await response.json()


def setup(bot):
    bot.add_cog(splitgate(bot))
