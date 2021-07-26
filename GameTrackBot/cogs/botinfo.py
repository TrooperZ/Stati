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
        website = "https://trooperz.github.io/Stati-Website/"
        supportlink = "https://discord.gg/c4Bg7Bw7B4"
        invitelink = "https://discord.com/oauth2/authorize?client_id=854781625236848640&permissions=379968&scope=bot"

        uptime = f"{days}d, {hours}h, {minutes}m, {seconds}s"
        embed = discord.Embed(title="Stati | By TrooperZ", description=f"**[Invite]({inviteLink}) | [Website]({website}) | [Support]({supportlink}) | [Invite]({invitelink})**")
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

    @commands.command()
    async def privacy(self, ctx):
        """View the privacy policy"""
        await ctx.send("""Stati Privacy Policy
By using Stati, you agree to the following privacy policy.

What information is stored?
Your user id is stored if you link your in game profile with Discord
Your user id is stored if you are blacklisted.
Stati's message id and the guild id of the server where the refreshing display is posted is saved.
When purchase Stati premium or donate, your user id is stored.

Why we store the information and how we use it.
We store this data to allow the features to work properly.

Who gets this data?
No one. This data is secured on our databases. 

Your in game names may be stored on other api services.

To view our api services privacy policies:
https://r6stats.com/privacy-policy - Rainbow Six Siege
https://thetrackernetwork.com/home/privacypolicy - CS:GO 

Questions and Concerns.
If you have questions and/or concerns about the data stored, please join the support server.

Some of these features aren't implemented yet but are planned to.

Note: We reserve the right to change this without notifying our users.

This policy was last updated July 25th, 2021.""")



def setup(bot):
    bot.add_cog(BotInfo(bot))
