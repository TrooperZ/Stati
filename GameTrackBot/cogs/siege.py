#!/usr/bin/python
# -*- coding: utf-8 -*-
# siege.py
    
# R6S stats for GameTrackBot.

import discord
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv
import os
import aiohttp
import asyncio
from operator import itemgetter
import json
from pprint import pprint
from reactionmenu import ButtonsMenu, ComponentsButton
import urllib.parse
import datetime

load_dotenv()

class R6(commands.Cog):
    """Rainbow Six Siege stats"""   
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=5, per=5, type=commands.BucketType.user)
    async def r6stats(self, ctx, user: str, platform="pc", info="default"):
        """Fetch general R6 stats for a user. Platform is pc by default (pc/xbox/ps4) and you can choose general/casual/ranked/bomb/secure/hostage for info selected"""
        if info.lower() not in ['default', 'general','casual', 'ranked', 'bomb', 'secure', 'hostage']:
            return await ctx.send("Invalid info option. Valid options are `general/casual/ranked/bomb/secure/hostage`")

        if platform.lower() not in ['pc', 'xbox', 'ps4']:
            return await ctx.send("Invalid platform. Valid options are `pc/xbox/ps4`.")

        elif platform.lower() == 'pc':
            emojiplatform = "<:uplay:855513596108210176>"

        elif platform.lower() == "xbox":
            emojiplatform = "<:xbox:855513924035805246>"

        elif platform.lower() == "ps4":
            emojiplatform = "<:psn:855513595856814100>"

        async with aiohttp.ClientSession(headers={'Authorization': os.getenv('R6STATS_API')}) as session:
            async with session.get(f"https://api2.r6stats.com/public-api/stats/{user}/{platform.lower()}/generic") as response:
                datageneral = await response.json()

            async with session.get(f"https://api2.r6stats.com/public-api/stats/{user}/{platform.lower()}/seasonal") as response:
                datarank = await response.json()

                pprint(datageneral)

                try:
                    username = datageneral['username']
                except Exception as e:
                    await ctx.send(e)
                    return await ctx.send("User not found. Check the name and verify that you are using the correct platform (PC is default platform)")

                lvl = datageneral['progression']['level']
                xp = datageneral['progression']['total_xp']
                rank = datarank['seasons']['north_star']['regions']['ncsa'][0]['rank_text']
                playtime = datageneral['stats']['general']['playtime'] / 3600
                pfp = datageneral['avatar_url_256']

                kills = datageneral['stats']['general']['kills']
                deaths = datageneral['stats']['general']['deaths']
                kd = datageneral['stats']['general']['kd']
                wins = datageneral['stats']['general']['wins']
                loss = datageneral['stats']['general']['losses']
                wl = datageneral['stats']['general']['wl']
                headshots = datageneral['stats']['general']['headshots']
                hdpct = round(headshots/kills * 100, 3)
                assist = datageneral['stats']['general']['assists']
                blindkill = datageneral['stats']['general']['blind_kills']
                dbno = datageneral['stats']['general']['dbnos']
                melee = datageneral['stats']['general']['melee_kills']
                penet = datageneral['stats']['general']['penetration_kills']
                reviv = datageneral['stats']['general']['revives']
                suicide = datageneral['stats']['general']['suicides']
                barr = datageneral['stats']['general']['barricades_deployed']
                reinf = datageneral['stats']['general']['reinforcements_deployed']       
                reviv = datageneral['stats']['general']['revives']

                ckill = datageneral['stats']['queue']['casual']['kills']
                cwin = datageneral['stats']['queue']['casual']['wins']
                closs = datageneral['stats']['queue']['casual']['losses']
                cdeath = datageneral['stats']['queue']['casual']['deaths']
                ckd = datageneral['stats']['queue']['casual']['kd']
                cwl = datageneral['stats']['queue']['casual']['wl']
                cplaytime = datageneral['stats']['queue']['casual']['playtime'] / 3600

                rkill = datageneral['stats']['queue']['ranked']['kills']
                rwin = datageneral['stats']['queue']['ranked']['wins']
                rloss = datageneral['stats']['queue']['ranked']['losses']
                rdeath = datageneral['stats']['queue']['ranked']['deaths']
                rkd = datageneral['stats']['queue']['ranked']['kd']
                rwl = datageneral['stats']['queue']['ranked']['wl']
                rplaytime = datageneral['stats']['queue']['ranked']['playtime'] / 3600
                
                btime = datageneral['stats']['gamemode']['bomb']['playtime'] / 3600
                bwin = datageneral['stats']['gamemode']['bomb']['wins']
                bloss = datageneral['stats']['gamemode']['bomb']['losses']
                bscore = datageneral['stats']['gamemode']['bomb']['best_score']
                bwl = datageneral['stats']['gamemode']['bomb']['wl']

                stime = datageneral['stats']['gamemode']['secure_area']['playtime'] / 3600
                swin = datageneral['stats']['gamemode']['secure_area']['wins']
                sloss = datageneral['stats']['gamemode']['secure_area']['losses']
                sscore = datageneral['stats']['gamemode']['secure_area']['best_score']
                skatt = datageneral['stats']['gamemode']['secure_area']['kills_as_attacker_in_objective']
                skdef = datageneral['stats']['gamemode']['secure_area']['kills_as_defender_in_objective']
                ssecure = datageneral['stats']['gamemode']['secure_area']['times_objective_secured']
                swl = datageneral['stats']['gamemode']['secure_area']['wl']

                htime = datageneral['stats']['gamemode']['hostage']['playtime'] / 3600
                hwin = datageneral['stats']['gamemode']['hostage']['wins']
                hloss = datageneral['stats']['gamemode']['hostage']['losses']
                hscore = datageneral['stats']['gamemode']['hostage']['best_score']
                hwl = datageneral['stats']['gamemode']['hostage']['wl']
                hdeny = datageneral['stats']['gamemode']['hostage']['extractions_denied']

                embed1 = discord.Embed(title=f"{emojiplatform} {username} | <:r6logo:855511007450365962> Rainbow Six Siege", description=f"**Overview**\nRank: {rank} | Level: {lvl} ({xp} XP) | Playtime: {round(playtime, 1)}h", color=0xbababa)
                embed1.add_field(name=":crossed_swords: KD", value=f"{kills} Kills / {deaths} Deaths ({kd} KD)", inline=False)
                embed1.add_field(name=":trophy: WL", value=f"{wins} Wins / {loss} Losses ({wl} WL)", inline=False)
                embed1.add_field(name="<:headshot:858777135186313267> Headshots", value=f"{headshots} Headshots ({hdpct}%)", inline=False)
                embed1.add_field(name="Assists", value=f"{assist}")
                embed1.add_field(name="Downs", value=f"{dbno}")
                embed1.add_field(name="Melee Kills", value=f"{melee}")
                embed1.add_field(name="Blind Kills", value=f"{blindkill}")
                embed1.add_field(name="Penetration Kills", value=f"{penet}")
                embed1.add_field(name="Suicides", value=f"{suicide}")
                embed1.add_field(name="Revives", value=f"{reviv}")
                embed1.add_field(name="Barricades", value=f"{barr}")
                embed1.add_field(name="Reinforcments", value=f"{reinf}")
                embed1.set_thumbnail(url=pfp)

                embed2 = discord.Embed(title=f"{emojiplatform} {username} | <:r6logo:855511007450365962> Rainbow Six Siege", description=f"**Casual**\nPlaytime: {round(cplaytime, 1)}h", color=0xbababa)
                embed2.add_field(name=":crossed_swords: KD", value=f"{ckill} Kills / {cdeath} Deaths ({ckd} KD)", inline=False)
                embed2.add_field(name=":trophy: WL", value=f"{cwin} Wins / {closs} Losses ({cwl} WL)", inline=False)
                embed2.set_thumbnail(url=pfp)   
                
                embed3 = discord.Embed(title=f"{emojiplatform} {username} | <:r6logo:855511007450365962> Rainbow Six Siege", description=f"**Ranked**\nRank: {rank} |Playtime: {round(rplaytime, 1)}h", color=0xbababa)
                embed3.add_field(name=":crossed_swords: KD", value=f"{rkill} Kills / {rdeath} Deaths ({rkd} KD)", inline=False)
                embed3.add_field(name=":trophy: WL", value=f"{rwin} Wins / {rloss} Losses ({rwl} WL)", inline=False)
                embed3.set_thumbnail(url=pfp) 

                embed4 = discord.Embed(title=f"{emojiplatform} {username} | <:r6logo:855511007450365962> Rainbow Six Siege", description=f"**Bomb**\nPlaytime: {round(btime, 1)}h", color=0xbababa)
                embed4.add_field(name=":trophy: WL", value=f"{bwin} Wins / {bloss} Losses ({bwl} WL)", inline=False)
                embed4.add_field(name=":medal: Best Score", value=f"{bscore}", inline=False)
                embed4.set_thumbnail(url=pfp) 


                embed5 = discord.Embed(title=f"{emojiplatform} {username} | <:r6logo:855511007450365962> Rainbow Six Siege", description=f"**Secure Area**\nPlaytime: {round(stime, 1)}h", color=0xbababa)
                embed5.add_field(name=":trophy: WL", value=f"{swin} Wins / {sloss} Losses ({swl} WL)", inline=False)
                embed5.add_field(name=":medal: Best Score", value=f"{sscore}", inline=False)
                embed5.add_field(name=":shield: Obj Defender Kills", value=f"{skdef}", inline=False)
                embed5.add_field(name=":dagger: Obj Attacker Kills", value=f"{skatt}", inline=False)
                embed5.add_field(name=":lock: Secures", value=f"{ssecure}", inline=False)
                embed5.set_thumbnail(url=pfp) 

                embed6 = discord.Embed(title=f"{emojiplatform} {username} | <:r6logo:855511007450365962> Rainbow Six Siege", description=f"**Hostage**\nPlaytime: {round(htime, 1)}h", color=0xbababa)
                embed6.add_field(name=":trophy: WL", value=f"{hwin} Wins / {hloss} Losses ({hwl} WL)", inline=False)
                embed6.add_field(name=":medal: Best Score", value=f"{hscore}", inline=False)
                embed6.add_field(name=":octagonal_sign: Extractions Denied", value=f"{hdeny}", inline=False)
                embed6.set_thumbnail(url=pfp) 
                
                if info.lower() == "general":
                    return await ctx.send(embed=embed1)

                elif info.lower() == "casual":
                    return await ctx.send(embed=embed2)

                elif info.lower() == "ranked":
                    return await ctx.send(embed=embed3)

                elif info.lower() == "bomb":
                    return await ctx.send(embed=embed4)

                elif info.lower() == "secure":
                    return await ctx.send(embed=embed5)

                elif info.lower() == "hostage":
                    return await ctx.send(embed=embed6)

                
                menu = menu = ButtonsMenu(ctx, menu_type=ButtonsMenu.TypeEmbed)

                back_button = ComponentsButton(style=ComponentsButton.style.secondary, label='◀️', custom_id=ComponentsButton.ID_PREVIOUS_PAGE)
                next_button = ComponentsButton(style=ComponentsButton.style.secondary, label='▶️', custom_id=ComponentsButton.ID_NEXT_PAGE)
                delete_button = ComponentsButton(style=ComponentsButton.style.red, label='❌', custom_id=ComponentsButton.ID_END_SESSION)

                menu.add_page(embed1)
                menu.add_page(embed2)
                menu.add_page(embed3)
                menu.add_page(embed4)
                menu.add_page(embed5)
                menu.add_page(embed6)

                menu.add_button(back_button)
                menu.add_button(next_button)
                menu.add_button(delete_button)
                await menu.start()

    @commands.command()
    @commands.cooldown(rate=5, per=5, type=commands.BucketType.user)
    async def r6operators(self, ctx, user: str, platform="pc"):
        """Fetch general R6 stats for a user. Platform is pc by default (pc/xbox/ps4) and you can choose general/casual/ranked/bomb/secure/hostage for info selected"""
        if platform.lower() not in ['pc', 'xbox', 'ps4']:
            return await ctx.send("Invalid platform. Valid options are `pc/xbox/ps4`.")

        elif platform.lower() == 'pc':
            emojiplatform = "<:uplay:855513596108210176>"

        elif platform.lower() == "xbox":
            emojiplatform = "<:xbox:855513924035805246>"

        elif platform.lower() == "ps4":
            emojiplatform = "<:psn:855513595856814100>"

        async with aiohttp.ClientSession(headers={'Authorization': os.getenv('R6STATS_API')}) as session:
            async with session.get(f"https://api2.r6stats.com/public-api/stats/{user}/{platform.lower()}/operators") as response:
                dataops = await response.json()
                pprint(dataops)

                dataops_sort = sorted(dataops['operators'], key=itemgetter('kills'), reverse=True) 

                pprint(dataops_sort)

            async with session.get(f"https://api2.r6stats.com/public-api/stats/{user}/{platform.lower()}/weapons") as response:
                dataweapons = await response.json()
                pprint(dataweapons)

                try:
                    username = dataops['username']
                except:
                    return await ctx.send("User not found. Check the name and verify that you are using the correct platform (PC is default platform)")




def setup(bot):
    bot.add_cog(R6(bot))
