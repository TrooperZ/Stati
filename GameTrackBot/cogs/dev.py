import discord
from discord.ext import commands
from discord.ext import tasks

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def getguilds(self, ctx):
        for i in self.bot.guilds:
            await ctx.send(i.name)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def say(self, ctx, msg):
        await ctx.send(msg)

    @tasks.loop(seconds=360)
    async def statusLoop(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"gameplay in {len(self.bot.guilds)} servers"))

    @statusLoop.before_loop
    async def before_statusLoop(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.statusLoop.start()


def setup(bot):
    bot.add_cog(Dev(bot))
