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

class CSGO(commands.Cog):
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
                pprint(data1)
                try:
                    if data1['errors'][0]['code'] == "CollectorResultStatus::NotFound":
                        return await ctx.send('User not found. Try using your numerical SteamID or legacy name and Check that the profile is public and has played CS:GO. If the name has spaces, put it in quotes `"like this"`')
                    elif data1['errors'][0]['code'] == "CollectorResultStatus::Private":
                        return await ctx.send('User not found. Try using your numerical SteamID or legacy name and Check that the profile is public and has played CS:GO. If the name has spaces, put it in quotes `"like this"`')
                except:
                    pass

                username = data1['data']['platformInfo']['platformUserHandle']
                userid = data1['data']['platformInfo']['platformUserIdentifier']
                pfp = data1['data']['platformInfo']['avatarUrl']

        async with aiohttp.ClientSession(headers={'TRN-Api-Key': os.getenv('TRACKER_API')}) as session:
            async with session.get(f"https://public-api.tracker.gg/v2/csgo/standard/profile/steam/{user}") as response:
                data = await response.json()

                username = data['data']['platformInfo']['platformUserHandle']
                playtime = data['data']['segments'][0]['stats']['timePlayed']['displayValue']
                kills = data['data']['segments'][0]['stats']['kills']['displayValue']
                deaths = data['data']['segments'][0]['stats']['deaths']['displayValue']
                kd = data['data']['segments'][0]['stats']['kd']['displayValue']
                wins = data['data']['segments'][0]['stats']['wins']['displayValue']
                losses = data['data']['segments'][0]['stats']['losses']['displayValue']
                wl = data['data']['segments'][0]['stats']['wlPercentage']['displayValue']
                headshots = data['data']['segments'][0]['stats']['headshots']['displayValue']
                hdpct = data['data']['segments'][0]['stats']['headshotPct']['displayValue']
                shotfire = data['data']['segments'][0]['stats']['shotsFired']['displayValue']
                shothit = data['data']['segments'][0]['stats']['shotsHit']['displayValue']
                accur = data['data']['segments'][0]['stats']['shotsAccuracy']['displayValue']
                bplant = data['data']['segments'][0]['stats']['bombsPlanted']['displayValue']
                bdefuse = data['data']['segments'][0]['stats']['bombsDefused']['displayValue']
                damage = data['data']['segments'][0]['stats']['damage']['displayValue']
                matches = data['data']['segments'][0]['stats']['matchesPlayed']['displayValue']
                mvp = data['data']['segments'][0]['stats']['mvp']['displayValue']
                money = data['data']['segments'][0]['stats']['moneyEarned']['displayValue']
                roundsw = data['data']['segments'][0]['stats']['roundsWon']['displayValue']
                rounds = data['data']['segments'][0]['stats']['roundsPlayed']['displayValue']
                score = data['data']['segments'][0]['stats']['score']['displayValue']
                doms = data['data']['segments'][0]['stats']['dominations']['displayValue']

                embed = discord.Embed(title=f"<:steam:857648825433587753> {username} | <:csgo:857649117068918795> Counter Strike Global Offensive", description=f"Played For: {playtime} | Total Score: {score} | MVPs: {mvp}", color=0xde9b35)
                embed.set_thumbnail(url=data['data']['platformInfo']['avatarUrl'])
                embed.add_field(name=":crossed_swords: KD", value=f"{kills} Kills / {deaths} Deaths ({kd} KD)", inline=False)
                embed.add_field(name=":trophy: WL", value=f"{wins} Wins / {losses} Losses ({wl} WL, Total: {matches})", inline=False)
                #embed.add_field(name=":joystick: Rounds", value=f"{roundsw} Won / Total: {rounds}", inline=False) - not correct data
                embed.add_field(name="<:headshot:858777135186313267> Headshots", value=f"{headshots} Headshots ({hdpct})", inline=False) 
                embed.add_field(name="<:accur:858730716732063746> Accuracy", value=f"{shothit} Shots Hit / {shotfire} Shots Fired ({accur})", inline=False)
                embed.add_field(name=":bomb: Bombs", value=f"{bplant} Planted | {bdefuse} Defused", inline=False)
                embed.add_field(name=":drop_of_blood: Damage", value=f"{damage} HP", inline=True)
                embed.add_field(name=":moneybag: Money Earned", value=f"${money}", inline=True)
                embed.add_field(name=":boxing_glove: Dominations", value=f"{doms}", inline=True)


                embed.set_footer(text=f"Your Steam ID is: {userid}")
                await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=5, per=5, type=commands.BucketType.user)
    async def csgoguns(self, ctx, user: str, category="all"):
        """Fetch detailed gun statistics for a CS:GO user via Steam name or Steam integer ID. Specific categories include: all/pistol/rifle/smg/heavy. 
        The API puts USP-S/P2000, MP7/MP5SD, M4A4/M4A1-S, Desert Eagle/R8 Revolver, TEC-9/CZ75 Auto, and Five Seven/CZ75 Auto stats together."""
        category = category.lower()
        urllib.parse.quote(user)
        if category not in ["all", "pistol", "rifle", "smg", "heavy"]:
            return await ctx.send("Invalid gun category. Valid categories are `all/pistol/rifle/smg/heavy` ")
        emojiDict = {
            "ak47": "<:ak47csgo:858555675383037992>",
            "m4a1": "<:m4a1csgo:858555675029143573>",
            "deagle": "<:deagcsgo:858555675004370946>",
            "awp": "<:awpcsgo:858555675398504458>",
            "mp7": "<:mp7csgo:858555675458011166>",
            "p250": "<:p250csgo:858555675373338624>",
            "ump45": "<:ump45csgo:858555675264811059>",
            "zeus": "<:zeuscsgo:858555649269039124>",
            "galilar": "<:galilcsgo:858555649280311296>",
            "nova": "<:novacsgo:858555649351876628>",
            "hkp2000": "<:p2000csgo:858555649340604456>",
            "glock": "<:glockcsgo:858555649326448671>",
            "aug": "<:augcsgo:858555649397620776>",
            "m249": "<:m249csgo:858555649288962058>",
            "p90": "<:p90csgo:858555649276772382>",
            "bizon": "<:bizoncsgo:858555649318584331>",
            "mac10": "<:mac10csgo:858555675389984788>",
            "sawedoff": "<:sawedoffcsgo:858555649334837258>",
            "sg556": "<:sg556csgo:858555649284505630>",
            "mag7": "<:mag7csgo:858555675130462269>",
            "elite": "<:dualcsgo:858555649285160980>",
            "famas": "<:famascsgo:858555649419640872>",
            "xm1014": "<:xm1014csgo:858555649381892106>",
            "mp9": "<:mp9csgo:858555675403616266>",
            "fiveseven": "<:fivesevencsgo:858555675385790475>",
            "g3sg1": "<:g3sg1csgo:858555649292763156>",
            "negev": "<:negevcsgo:858555649297088542>",
            "ssg08": "<:ssg08csgo:858700851640270858>",
            "tec9": "<:tec9csgo:858700851261866015>",
            "scar20": "<:scar20csgo:858700851488227359>",
            "zeus": "<:csgozeus:858555649269039124>"
            }

        async with aiohttp.ClientSession(headers={'TRN-Api-Key': os.getenv('TRACKER_API')}) as session:
            async with session.get(f"https://public-api.tracker.gg/v2/csgo/standard/profile/steam/{user}") as response:
                data1 = await response.json()
                try:
                    if data1['errors'][0]['code'] == "CollectorResultStatus::NotFound":
                        return await ctx.send('User not found. Try using your numerical SteamID or legacy name and Check that the profile is public and has played CS:GO. If the name has spaces, put it in quotes `"like this"`')
                    elif data1['errors'][0]['code'] == "CollectorResultStatus::Private":
                        return await ctx.send('User not found. Try using your numerical SteamID or legacy name and Check that the profile is public and has played CS:GO. If the name has spaces, put it in quotes `"like this"`')
                except:
                    pass
                username = data1['data']['platformInfo']['platformUserHandle']
                userid = data1['data']['platformInfo']['platformUserIdentifier']
                pfp = data1['data']['platformInfo']['avatarUrl']

        async with aiohttp.ClientSession(headers={'TRN-Api-Key': os.getenv('TRACKER_API')}) as session:
            async with session.get(f"https://public-api.tracker.gg/v2/csgo/standard/profile/steam/{userid}/segments/weapon") as response:
                data = await response.json()

                data_sort = {
                    "data": [
                        entry
                        for entry in sorted(
                            data["data"],
                            key=lambda x: x["stats"]["kills"]["value"],
                            reverse=True
                        )
                    ]
                }

                guns1 = discord.Embed(title=f"<:steam:857648825433587753> {username} | <:csgo:857649117068918795> Counter Strike Global Offensive", description="**Weapon Statistics**", color=0xde9b35)
                guns2 = discord.Embed(title=f"<:steam:857648825433587753> {username} | <:csgo:857649117068918795> Counter Strike Global Offensive", description="**Weapon Statistics**", color=0xde9b35)
                guns3 = discord.Embed(title=f"<:steam:857648825433587753> {username} | <:csgo:857649117068918795> Counter Strike Global Offensive", description="**Weapon Statistics**", color=0xde9b35)
                
                guns1.set_thumbnail(url=pfp)
                guns2.set_thumbnail(url=pfp)
                guns3.set_thumbnail(url=pfp)

                guns1.set_footer(text=f"Your Steam ID is: {userid}")
                guns2.set_footer(text=f"Your Steam ID is: {userid}")
                guns3.set_footer(text=f"Your Steam ID is: {userid}")

                n = 0
                for i in data_sort['data']:

                    if category != 'all':
                        if category != i['metadata']['category']['value']:
                            continue

                    try:
                        emoji = emojiDict[i['attributes']['key']]
                    except:
                        emoji = "*MISSING EMOJI*"

                    kills = i["stats"]["kills"]["displayValue"]
                    accur = i["stats"]["shotsAccuracy"]["displayValue"]
                    fire = i["stats"]["shotsFired"]["displayValue"]
                    hit = i["stats"]["shotsHit"]["displayValue"]

                    if i['attributes']['key'] == 'hkp2000':
                        gunname = "P2000/USP-S"
                    
                    elif i['attributes']['key'] == 'm4a1':
                        gunname = "M4A4/M4A1-S"

                    elif i['attributes']['key'] == 'mp7':
                        gunname = "MP7/MP5SD"

                    elif i['attributes']['key'] == 'deagle':
                        gunname = "Desert Eagle/R8 Revolver"

                    elif i['attributes']['key'] == 'tec9':
                        gunname = "Tec-9/CZ75 Auto"

                    elif i['attributes']['key'] == 'fiveseven':
                        gunname = "Five Seven/CZ75 Auto"

                    else:
                        gunname = i['metadata']['name']

                    if n < 10:
                        guns1.add_field(name=f"{emoji} {gunname}", value=f"Kills: {kills} **|** Accuracy: {accur}% **|** Shots Fired: {fire} **|** Shots Hit: {hit}", inline=False)
                    elif n >= 11 and n < 20:    
                        guns2.add_field(name=f"{emoji} {gunname}", value=f"Kills: {kills} **|** Accuracy: {accur}% **|** Shots Fired: {fire} **|** Shots Hit: {hit}", inline=False)
                    elif n > 21:    
                        guns3.add_field(name=f"{emoji} {gunname}", value=f"Kills: {kills} **|** Accuracy: {accur}% **|** Shots Fired: {fire} **|** Shots Hit: {hit}", inline=False)
                    n = n + 1

                menu = menu = ButtonsMenu(ctx, menu_type=ButtonsMenu.TypeEmbed)

                back_button = ComponentsButton(style=ComponentsButton.style.secondary, label='◀️', custom_id=ComponentsButton.ID_PREVIOUS_PAGE)
                next_button = ComponentsButton(style=ComponentsButton.style.secondary, label='▶️', custom_id=ComponentsButton.ID_NEXT_PAGE)
                delete_button = ComponentsButton(style=ComponentsButton.style.red, label='❌', custom_id=ComponentsButton.ID_END_SESSION)

                menu.add_page(guns1)
                if category == "all":

                    menu.add_page(guns2)
                    menu.add_page(guns3)

                menu.add_button(back_button)
                menu.add_button(next_button)
                menu.add_button(delete_button)
                await menu.start()

    @commands.command()
    @commands.cooldown(rate=5, per=5, type=commands.BucketType.user)
    async def csgomaps(self, ctx, *, user: str):
        """Fetch map stats for a CS:GO user via Steam name or Steam integer ID."""
        async with aiohttp.ClientSession(headers={'TRN-Api-Key': os.getenv('TRACKER_API')}) as session:
            async with session.get(f"https://public-api.tracker.gg/v2/csgo/standard/profile/steam/{user}") as response:
                data1 = await response.json()
                try:
                    if data1['errors'][0]['code'] == "CollectorResultStatus::NotFound":
                        return await ctx.send('User not found. Try using your numerical SteamID or legacy name and Check that the profile is public and has played CS:GO. If the name has spaces, put it in quotes `"like this"`')
                    elif data1['errors'][0]['code'] == "CollectorResultStatus::Private":
                        return await ctx.send('User not found. Try using your numerical SteamID or legacy name and Check that the profile is public and has played CS:GO. If the name has spaces, put it in quotes `"like this"`')
                except:
                    pass
                username = data1['data']['platformInfo']['platformUserHandle']
                userid = data1['data']['platformInfo']['platformUserIdentifier']
                pfp = data1['data']['platformInfo']['avatarUrl']

        async with aiohttp.ClientSession(headers={'TRN-Api-Key': os.getenv('TRACKER_API')}) as session:
            async with session.get(f"https://public-api.tracker.gg/v2/csgo/standard/profile/steam/{userid}/segments/map") as response:
                data = await response.json()
                pprint(data)
                data_sort = {
                    "data": [
                        entry
                        for entry in sorted(
                            data["data"],
                            key=lambda x: x["stats"]["rounds"]["value"],
                            reverse=True)]}

                menu = menu = ButtonsMenu(ctx, menu_type=ButtonsMenu.TypeEmbed)

                back_button = ComponentsButton(style=ComponentsButton.style.secondary, label='◀️', custom_id=ComponentsButton.ID_PREVIOUS_PAGE)
                next_button = ComponentsButton(style=ComponentsButton.style.secondary, label='▶️', custom_id=ComponentsButton.ID_NEXT_PAGE)
                delete_button = ComponentsButton(style=ComponentsButton.style.red, label='❌', custom_id=ComponentsButton.ID_END_SESSION)

                for i in data_sort['data']:
                    embed = discord.Embed(title=f"<:steam:857648825433587753> {username} | <:csgo:857649117068918795> Counter Strike Global Offensive", description=f"**{i['metadata']['name']}**", color=0xde9b35)
                    embed.set_image(url=i['metadata']['imageUrl'])
                    embed.add_field(name="Rounds Played", value=f"{i['stats']['rounds']['displayValue']}")
                    embed.add_field(name="Rounds Won", value=f"{i['stats']['wins']['displayValue']}")
                    embed.set_footer(text=f"Your Steam ID is: {userid}")
                    menu.add_page(embed)

                menu.add_button(back_button)
                menu.add_button(next_button)
                menu.add_button(delete_button)
                await menu.start()

    @commands.command()
    @commands.cooldown(rate=5, per=5, type=commands.BucketType.user)
    async def csgorecoil(self, ctx, gun, type="recoil", mode="regular"):
        if type.lower() not in ["recoil", "control"]:
            return await ctx.send("Invalid type. Valid options are `recoil/control`.")

        if mode.lower() not in ["regular", "scoped"]:
            return await ctx.send("Invalid mode. Valid options are `regular/scoped`")

        if gun.lower() not in ["sg553", "aug", "ssg08", "awp", "scar20", "g3sg1"] and mode.lower() == "scoped":
            return await ctx.send("This firearm cannot be scoped in.")

        if gun.lower() in ["m4a1", "m4a1s", "m4a1-s"]:
            gun = "m4a1"

        elif gun.lower() in ["galil", "galilar", "galil-ar"]:
            gun = "galil"

        elif gun.lower() in ["glock", "glock18", "glock-18"]:
            gun = "glock"

        elif gun.lower() in ["ump", "ump45", "ump-45"]:
            gun = "ump45"

        gunrecoil_dict = {
            "ak47": "https://cdn.discordapp.com/attachments/863461817631244288/863462292863451136/ak47-spray.gif",
            "m4a4": "https://cdn.discordapp.com/attachments/863461817631244288/863463180407537664/m4a4-spray.gif",
            "m4a1": "https://cdn.discordapp.com/attachments/863461817631244288/863807608921784320/M4A1-S_spray.gif",
            "galil": "https://cdn.discordapp.com/attachments/863461817631244288/863810779597373470/galil_spray.gif",
            "glock": "https://cdn.discordapp.com/attachments/863461817631244288/863811122049056768/Glock-18-Spray-Pattern.gif",
            "ump45": "https://cdn.discordapp.com/attachments/863461817631244288/869605710219083776/UMP-45-Spray-Pattern.gif"}

        guncompensate_dict = {
            "ak47": "https://cdn.discordapp.com/attachments/863461817631244288/863463146697654322/ak47-compensate.gif",
            "m4a4": "https://cdn.discordapp.com/attachments/863461817631244288/863463299668508702/m4a4-compensate.gif",
            "m4a1": "https://cdn.discordapp.com/attachments/863461817631244288/863807970302754826/m4a1s_comp.gif",
            "galil": "https://cdn.discordapp.com/attachments/863461817631244288/863810805623029790/galil_compensate.gif",
            "glock": "https://cdn.discordapp.com/attachments/863461817631244288/863811143717093376/Glock-18-Recoil-Compensation.gif",
            "ump45": "https://cdn.discordapp.com/attachments/863461817631244288/869605737456894052/UMP-45-Recoil-Compensation.gif"}

        if type.lower() == "recoil":
            embed = discord.Embed(title="<:csgo:857649117068918795> Counter Strike Global Offensive", description=f"{gun.upper()} {type}", color=0xde9b35)
            embed.set_image(url=gunrecoil_dict[gun.lower()])
            await ctx.send(embed=embed)

        elif type.lower() == "control":
            embed = discord.Embed(title="<:csgo:857649117068918795> Counter Strike Global Offensive", description=f"{gun.upper()} Control", color=0xde9b35)
            embed.set_image(url=guncompensate_dict[gun.lower()])
            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(CSGO(bot))
