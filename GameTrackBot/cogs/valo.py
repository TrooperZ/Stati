#!/usr/bin/python
# -*- coding: utf-8 -*-
# valo.py

# Valorant stats for GameTrackBot.


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
    async def valogunskin(self, ctx, *, gun: str):
        """Fetch gun skin data for a Valorant weapon"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://valorant-api.com/v1/weapons/skins") as response:
                data1 = await response.json()
                for i in data1["data"]:
                    if i["displayName"].lower() == gun.lower():
                        embed = discord.Embed(title=i["displayName"], value="** **")
                        embed.set_image(url=i["displayIcon"])
                        return await ctx.send(embed=embed)
                    else:
                        continue


def setup(bot):
    bot.add_cog(Valorant(bot))
