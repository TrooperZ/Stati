#!/usr/bin/python
# -*- coding: utf-8 -*-
# Botinfo
import asyncio
import datetime
import os
import sys
import time

import discord
import psutil
from discord.ext import commands

bot_launch_time = datetime.datetime.now()  # bot launch time for uptime command


class BotInfo(commands.Cog):
    """Bot information"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def botinfo(self, ctx):
        """General bot info"""
        delta_uptime = datetime.datetime.now() - bot_launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        memory = psutil.virtual_memory()

        inviteLink = "https://discord.com/api/oauth2/authorize?client_id=854781625236848640&permissions=379968&scope=bot"

        uptime = f"{days}d, {hours}h, {minutes}m, {seconds}s"
        embed = discord.Embed(title="Stati | By TrooperZ", description=f"[Invite]({inviteLink}) Website Support Premium/Donate")
        embed.add_field(name="Uptime:", value=uptime, inline=True)
        embed.add_field(name="CPU", value=f"{psutil.cpu_percent(percpu=False)}%", inline=True)
        embed.add_field(name="Memory", value=f"{round(memory.used/1024**2)}/{round(memory.total/1024**2)} MiB", inline=True)
        embed.add_field(name="Total Users", value=str(len(set(self.bot.users))), inline=True)
        embed.add_field(name="Total Servers", value=str(len(self.bot.guilds)), inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def vote(self, ctx):
        """Vote for Stati!"""
        embed = discord.Embed(title="Vote!", description="Vote on these sites")
        embed.add_field(name="Top.GG", value="[Coming soon]")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BotInfo(bot))
