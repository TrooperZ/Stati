#!/usr/bin/python
# -*- coding: utf-8 -*-
# csgo.py

# CSGO stats for GameTrackBot.


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

class Valorant(commands.Cog):
    """Valorant Stats"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=5, per=5, type=commands.BucketType.user)
    async def valostats(self, ctx, *, user: str):
        """Fetch general stats for a Valorant player."""



def setup(bot):
    bot.add_cog(Valorant(bot))
