from datetime import datetime, timedelta
from discord.ext import commands
from time import time
from discord.ext.commands.errors import MissingRequiredArgument
from dotenv import load_dotenv
from math import radians, cos, sin, sqrt, atan2
from lib.db import db
from typing import Optional

import aiohttp
import discord
import os
import requests
import asyncio

load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Ping command
    @commands.command(description = "This command calculates the time taken from the message being sent by the user and the message being returned by the bot. Use `-ping` and you will get a ping. ", brief = "Displays time taken by the server to respond back in ms")
    @commands.guild_only()
    async def Ping(self, ctx):
        start = time()
        message = await ctx.send("Pinging Server...")
        end = time()

        await message.edit(content = f"Server to Discord latency: `{self.bot.latency*1000:,.0f}` ms\nUser to bot response time `{(end-start)*1000:,.0f}` ms. :fire:")

    
    #userinfo command
    # @commands.command(description = "This command will give you public information about a user account. Make sure to mention them correctly.", brief = "Returns information for a user leave empty to check your self")
    # async def UserInfo(self, ctx, target: Optional[discord.Member]):
    #     target = target or ctx.message.author

    #     embed = discord.Embed(title = "User Information", colour = target.colour,timestamp = datetime.utcnow())
    #     embed.set_footer(icon_url= ctx.message.author.avatar_url, text = f"Information requested by {ctx.message.author.name}")
    #     embed.set_thumbnail(url = target.avatar_url)
    #     fields = [("ID", target.id,  False), 
    #             ("Name", str(target.name), True),
    #             ("Bot?", target.bot, True),
    #             ("Created Discord account on", target.created_at.strftime("%d/%m/%Y %H:%M:%S UTC"), True),
    #             ("Joined this server on", target.joined_at.strftime("%d/%m/%Y %H:%M:%S UTC"), True)]
        
    #     for name, value, inline in fields:
    #         embed.add_field(name = name, value = value, inline = inline)
    #     await ctx.send(embed=embed)
    
    #serverinfo command
    # @commands.command(description = "This command returns server information. For example when it was created at, Number of members and more!", brief = "Returns server information")
    # async def ServerInfo(self, ctx):
    #     embed = discord.Embed(title= "Server Information", colour = discord.Colour(0xff0000),timestamp = datetime.utcnow())
    #     embed.set_footer(icon_url= ctx.message.author.avatar_url, text = f"Information requested by {ctx.message.author.name}")
    #     embed.set_thumbnail(url = ctx.guild.icon_url)
    #     fields1 = [("Server Name", ctx.guild.name, True),
    #                 ("Owner", ctx.guild.owner.mention, True),
    #                 ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S UTC"), True),
    #                 ("Members including bots", len(ctx.guild.members), True),
    #                 ("Living Creatures", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
    #                 ("\u200b", "\u200b", True)]
        
    #     for name, value, inline in fields1:
    #         embed.add_field(name = name, value = value, inline = inline)
    #     await ctx.send(embed=embed)
    
   #metar API
    @commands.command(description = "This command displays metar for the specified ICAO code. Use `-metar` followed by the ICAO code and you will be displayed the METAR information for that airport.", brief = "Displays metar for the specified ICAO")
    @commands.guild_only()
    async def Metar(self, ctx,*,icao_random :str):
        icao = icao_random.upper()
        url = f"https://api.checkwx.com/metar/{icao}/decoded"

        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                headers = {"X-API-Key": "13b7b59ea5404c29bd637e3a5f"}
                async with cs.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()

                        if data["results"] == 1:
                            data_original = data["data"][0]['raw_text']
                            formatted_data = str(data_original)


                            embed = discord.Embed(title = "Metar Information", colour = discord.Color.from_rgb(92, 159, 36))
                            embed.add_field(inline=False, name=f"{icao} Metar:", value=formatted_data)
                            await ctx.send(embed=embed)

                    
                        else:
                            await ctx.send(f"Oops {ctx.message.author.name}, that ICAO was not found. Are you sure that ICAO code matches an airport ICAO? :face_with_raised_eyebrow: `Err: InvalidICAOCode` ")

                    elif response.status == 401:
                        await ctx.send("This doesn't happen often, standby. `Err:Invalidcred`")
                    
                    elif response.status == 429:
                        await ctx.send("Metar service is down. `Err:Servicenotresponding`")
                
                    elif response.status == 404:
                        await ctx.send(f"Oops {ctx.message.author.name}, that ICAO was not found. Are you sure that ICAO code matches an airport ICAO? :face_with_raised_eyebrow: `Err: InvalidICAOCode` ")
                
                    else:
                        await ctx.send(f"`Err: {response.status} response code`")
    @Metar.error
    async def Metar_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter an icao code after the command for example, `-metar opkc`")

    @commands.command(description = "Displays number of arrivals, their callsign, departure airport and ETA to the airport and displays number of departures, their callsign, arrival airport and departure time for the specified airport ICAO code.")
    #@commands.guild_only()
    async def traffic(self, ctx, icao: Optional[str]):
        def distance(lat1, lat2, lon1, lon2):
            lat1 = radians(lat1)
            lon1 = radians(lon1)
            lat2 = radians(lat2)
            lon2 = radians(lon2)

            dlon = lon2 - lon1

            dlat = lat2 - lat1

            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            R = 6373.0
            distance = R * c
            return distance

        if icao == None:
            r = requests.get("https://data.vatsim.net/v3/vatsim-data.json")
            if r.status_code == 200:
                try:
                    data1 = r.json()
                except:
                    dep_count = "N/A"
                    arr_count = "N/A"
                    arrivals = "N/A"
                    departures = "N/A"
                    await ctx.send("Uh oh, it appears VATSIM server could not be reached. Please try again later. :confused:")
                else:
                    dep_count = 0
                    arr_count = 0
                    arrivals = []
                    departures = []
                
                    for x in data1['pilots']:
                        if x['flight_plan'] != None:
                            if x['flight_plan']['departure'] != None:
                                if x['flight_plan']['departure'].upper() != "OPRN":
                                    if str(x['flight_plan']['departure']).startswith("OP"):
                                        append_this = {"callsign" : str(x['callsign']), "dep" : str(x['flight_plan']['departure']), "arr" : str(x['flight_plan']['arrival']), "deptime" : str(x['flight_plan']['deptime'])}
                                        departures.append(append_this)
                                        dep_count += 1
                    
                            if x['flight_plan']['arrival'] != None:
                                if x['flight_plan']['arrival'].upper().startswith("OP"):
                                    if x['flight_plan']['arrival'].upper() != "OPRN":
                                        arr_count += 1
                                        eta = "N/A"
                                        dist = distance(float(db.field("SELECT coordinate1 FROM airports WHERE icao = ?", str(x['flight_plan']['arrival']).upper())), x['latitude'], float(db.field("SELECT coordinate2 FROM airports WHERE icao = ?", str(x['flight_plan']['arrival']).upper())), x['longitude'])
                                        dist_nm = dist / 1.852
                        
                                        if int(x['groundspeed']) != 0:
                                            time1 = dist_nm / x['groundspeed']
                                            time_in_mins = time1 * 60
                                            time_then = datetime.utcnow() + timedelta(minutes=time_in_mins)
                                            eta = f'{datetime.strftime(time_then, "%H:%M")}Z'
                                        append_this_arr = {'callsign' : str(x['callsign']), 'dep' : str(x['flight_plan']['departure']), 'arr' : str(x['flight_plan']['arrival']), 'eta' : str(eta)}
                                        arrivals.append(append_this_arr)
                    
                    embed = discord.Embed(title=f"Arrival Traffic Statistics", colour = discord.Color.from_rgb(92, 159, 36))
                    embed.add_field(inline=False, name=f"Arrivals:", value=arr_count)
                    
                    if len(arrivals) != 0:
                        arrivals.sort(key=lambda x: x.get('eta'))
                        for arr in arrivals:
                            embed.add_field(inline=True, name=f"Callsign:", value=arr['callsign'])
                            embed.add_field(inline=True, name=f"Departure:", value=arr['dep'])
                            embed.add_field(inline=True, name=f"Arrival & ETA:", value=f"{arr['arr']}, {arr['eta']}")

                    embed.set_footer(text=f"Requested by {ctx.message.author.display_name}", icon_url=ctx.author.avatar_url)
                    embed2 = discord.Embed(title=f"Departure Traffic Statistics", colour = discord.Color.from_rgb(92, 159, 36))
                    embed2.add_field(inline=False, name=f"Departures:", value=dep_count)

                    if len(departures) != 0:
                        departures.sort(key=lambda x: x.get('deptime'))
                        for depx in departures:
                            embed2.add_field(inline=True, name=f"Callsign:", value=depx['callsign'])
                            embed2.add_field(inline=True, name=f"Departure & ETD:", value=f"{depx['dep']}, {depx['deptime']}Z")
                            embed2.add_field(inline=True, name=f"Arrival:", value=depx['arr'])

                    embed2.set_footer(text=f"Requested by {ctx.message.author.display_name}", icon_url=ctx.author.avatar_url)

                    await ctx.send(embed=embed)
                    await ctx.send(embed=embed2)
            else:
                await ctx.send("Uh oh, it appears VATSIM server could not be reached. Please try again later. :confused:")
     
        elif len(icao) == 4 and icao.upper().startswith("OP") and icao != None:
            icao = icao.upper()
            r = requests.get("https://data.vatsim.net/v3/vatsim-data.json")
            if r.status_code == 200:
                try:
                    data1 = r.json()
                except:
                    dep_count = "N/A"
                    arr_count = "N/A"
                    arrivals = "N/A"
                    departures = "N/A"
                    await ctx.send("Uh oh, it appears VATSIM server could not be reached. Please try again later. :confused:")
                else:
                    dep_count = 0
                    arr_count = 0
                    arrivals = []
                    departures = []
                
                    for x in data1['pilots']:
                        if x['flight_plan'] != None:
                            if x['flight_plan']['departure'] != None:
                                if x['flight_plan']['departure'] == icao.upper():
                                    departures.append(f"[{str(x['callsign'])},{str(x['flight_plan']['arrival'])},{str(x['flight_plan']['deptime'])}]")
                                    dep_count += 1
                            if x['flight_plan']['arrival'] != None:
                                if x['flight_plan']['arrival'] == icao.upper():
                                    arr_count += 1
                                    eta = "N/A"
                                    if icao.upper().startswith("OP"):
                                        dist = distance(float(db.field("SELECT coordinate1 FROM airports WHERE icao = ?", icao.upper())), x['latitude'], float(db.field("SELECT coordinate2 FROM airports WHERE icao = ?", icao.upper())), x['longitude'])
                                        dist_nm = dist / 1.852
                        
                                        if int(x['groundspeed']) != 0:
                                            time1 = dist_nm / x['groundspeed']
                                            time_in_mins = time1 * 60
                                            time_then = datetime.utcnow() + timedelta(minutes=time_in_mins)
                                            eta = datetime.strftime(time_then, "%H:%M")
                                    arrivals.append(f"[{str(x['callsign'])},{str(eta)}Z,{str(x['flight_plan']['departure'])}]")

                    embed = discord.Embed(title=f"{icao.upper()} Arrival Traffic Statistics", colour = discord.Color.from_rgb(92, 159, 36))
                    embed.add_field(inline=False, name=f"Arrivals: {arr_count}", value=f"\u200b")
                    if len(arrivals) != 0:
                        for arr in arrivals:
                            arr =  arr.strip('][').split(', ')
                            embed.add_field(inline=True, name=f"Callsign:", value=f"{arr[0].split(',')[0]}")
                            embed.add_field(inline=True, name=f"Departure:", value=f"{arr[0].split(',')[2]}")
                            embed.add_field(inline=True, name="ETA", value=f"{arr[0].split(',')[1]}")

                    embed2 = discord.Embed(title=f"{icao.upper()} Departure Traffic Statistics", colour = discord.Color.from_rgb(92, 159, 36))
                    embed2.add_field(inline=False, name=f"Departures: {dep_count}", value=f"\u200b")

                    if len(departures) != 0:
                        for depx in departures:
                            dep =  depx.strip('][').split(', ')
                            embed2.add_field(inline=True, name=f"Callsign:", value=f"{dep[0].split(',')[0]}")
                            embed2.add_field(inline=True, name=f"Arrival:", value=f"{dep[0].split(',')[1]}")
                            embed2.add_field(inline=True, name=f"Departure Time:", value=f"{dep[0].split(',')[2]}Z")

                    await ctx.send(embed=embed)
                    await ctx.send(embed=embed2)

            
            else:
                await ctx.send("Uh oh, it appears VATSIM server could not be reached. Please try again later. :confused:")
        
        else:
            await ctx.send("The command only works for Pakistan airports.")

    @commands.command(description = "Displays metar, active runway, number of departures and number of arrivals. An example to run the command is `-info opla` ")
    @commands.guild_only()
    async def info(self, ctx, icao :str):
        loading_embed = discord.Embed(colour = discord.Color.from_rgb(92, 159, 36))
        loading_embed.set_author(name=f"Standby {ctx.message.author.display_name}, this is gonna take some time.", icon_url="https://media.giphy.com/media/sSgvbe1m3n93G/source.gif?cid=ecf05e47a0z65sl6qyqji8f06i3zanuj9s581zjo8pp2jns9&rid=source.gif&ct=g")
        msg = await ctx.send(embed=loading_embed)
        url = f"https://api.checkwx.com/metar/{icao.upper()}/decoded"
        is_an_airport = True

        async with aiohttp.ClientSession() as cs:
            headers = {"X-API-Key": "MYAPIKEY"}
            async with cs.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()

                    if data["results"] == 1:
                        data_original = str(data["data"][0]['raw_text'])
                        if icao.upper() == "OPLA":
                            if int(data['data'][0]['wind']['speed_kts']) <= 6:
                                runway = 36
                            elif int(data['data'][0]['wind']['degrees']) >= 90 and int(data['data'][0]['wind']['degrees']) <= 270:
                                runway = 18
                            elif int(data['data'][0]['wind']['degrees']) >= 270 and int(data['data'][0]['wind']['degrees']) <= 360:
                                runway = 36
                            elif int(data['data'][0]['wind']['degrees']) >= 0 and int(data['data'][0]['wind']['degrees']) <= 90:
                                runway = 36
                            else:
                                runway = "N//A"

                        elif icao.upper() == "OPKC":
                            if int(data['data'][0]['wind']['speed_kts']) <= 6:
                                runway = 25
                            elif int(data['data'][0]['wind']['degrees']) >= 0 and int(data['data'][0]['wind']['degrees']) <= 150:
                                runway = "07"
                            elif int(data['data'][0]['wind']['degrees']) >= 150 and int(data['data'][0]['wind']['degrees']) <= 360:
                                runway = 25
                            else:
                                runway = "N//A"
                        
                        elif icao.upper() == "OPIS":
                            if int(data['data'][0]['wind']['speed_kts']) <= 6:
                                runway = 28
                            elif int(data['data'][0]['wind']['degrees']) >= 10 and int(data['data'][0]['wind']['degrees']) <= 190:
                                runway = 10
                            elif int(data['data'][0]['wind']['degrees']) >= 190 and int(data['data'][0]['wind']['degrees']) <= 360:
                                runway = 28
                            elif int(data['data'][0]['wind']['degrees']) >= 0 and int(data['data'][0]['wind']['degrees']) <= 10:
                                runway = 28
                            else:
                                runway = "N//A"

                    else:
                        data_original = "ICAO Not Found"
                        is_an_airport = False
                        await ctx.send(f"Oops {ctx.message.author.display_name}, that ICAO was not found. Are you sure that ICAO code matches an airport ICAO? :face_with_raised_eyebrow: `Err: InvalidICAOCode` ")

                elif response.status == 401:
                    data_original = "N/A"
                    await ctx.send("This doesn't happen often, standby. `Err:Invalidcred`")
                
                elif response.status == 429:
                    data_original = "N/A"
                    await ctx.send("Metar service is down. `Err:Servicenotresponding`")
            
                elif response.status == 404:
                    data_original = "N/A"
                    is_an_airport = False
                    await ctx.send(f"Oops {ctx.message.author.display_name}, that ICAO was not found. Are you sure that ICAO code matches an airport ICAO? :face_with_raised_eyebrow: `Err: InvalidICAOCode` ")
            
                else:
                    data_original = "N/A"
                    await ctx.send(f"`Err: {response.status} response code`")
        
        if is_an_airport == True:
        
            r = requests.get("https://data.vatsim.net/v3/vatsim-data.json")
            if r.status_code == 200:
                try:
                    data1 = r.json()
                except:
                    dep_count = "N/A"
                    arr_count = "N/A"
                else:
                    dep_count = 0
                    arr_count = 0
                    for x in data1['pilots']:
                        if x['flight_plan'] != None:
                            if x['flight_plan']['departure'] != None:
                                if x['flight_plan']['departure'] == icao.upper():
                                    dep_count += 1
                            if x['flight_plan']['arrival'] != None:
                                if x['flight_plan']['arrival'] == icao.upper():
                                    arr_count += 1

            embed = discord.Embed(title=f"{icao.upper()} Airport Information", colour = discord.Color.from_rgb(92, 159, 36))
            embed.add_field(inline=False, name=f"{icao.upper()} Metar", value=data_original)
            if icao.upper() == "OPLA" or icao.upper() == "OPKC" or icao.upper() == "OPIS":
                embed.add_field(inline=False, name=f"{icao.upper()} Active Runway", value=runway)
            embed.add_field(inline=False, name=f"{icao.upper()} Departures", value=dep_count)
            embed.add_field(inline=False, name=f"{icao.upper()} Arrivals", value=arr_count)
            await ctx.send(embed=embed)

            # if icao.upper().startswith("OP") and len(icao) == 4 and icao != None:
            #     online_pos = db.records("SELECT * FROM onlineatc")
            #     if len(online_pos) != 0:
            #         embed2 = discord.Embed(title=f"vACC Online ATC", colour = discord.Color.from_rgb(92, 159, 36))
            #         for x in online_pos:
            #             embed2.add_field(inline=False, name=x[1], value=f"Controller: {x[4]} - {x[5]}")
            #         await ctx.send(embed=embed2)
            
            await msg.delete()

        else:
            await msg.delete()
            await ctx.send(f"Oops {ctx.message.author.display_name}, that ICAO was not found. Are you sure that ICAO code matches an airport ICAO? 🤨 Err: InvalidICAOCode")
    
    @info.error
    async def info_error(self, ctx, error):        
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Please mention the airport icao code. Example: `-info opla`")

    @commands.command()
    @commands.guild_only()
    async def groupflight(self, ctx):
        dep_icao = await ctx.send("What is the departure ICAO code? Reply within 30 seconds.")

        try:
            dep_icao_wait = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 30.0)
        
        except asyncio.TimeoutError:
            await dep_icao.delete()
            await ctx.send("Oops, you ran out of time. Please run the command again.")
    
        else:
            dep_rwy = await ctx.send("What is the departure runway? Reply within 30 seconds.")
            try:
                dep_rwy_wait = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 30.0)
        
            except asyncio.TimeoutError:
                await dep_icao.delete()
                await dep_icao_wait.delete()
                await dep_rwy.delete()
                await ctx.send("Oops, you ran out of time. Please run the command again.")
            
            else:
                dep_time = await ctx.send("What is the estimated departure time? Format example: *'15th January, 2022 2000z'*. Reply within 30 seconds.")
                
                try:
                    dep_time_wait = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 30.0)
                
                except asyncio.TimeoutError:
                    await dep_icao.delete()
                    await dep_icao_wait.delete()
                    await dep_rwy.delete()
                    await dep_rwy_wait.delete()
                    await dep_time.delete()
                    await ctx.send("Oops, you ran out of time. Please run the command again.")
                
                else:
                
                    arr_icao = await ctx.send("What is the arrival ICAO code? Reply within 30 seconds.")

                    try:
                        arr_icao_wait = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 30.0)

                    except asyncio.TimeoutError:
                        await dep_icao.delete()
                        await dep_icao_wait.delete()
                        await arr_icao.delete()
                        await dep_rwy.delete()
                        await dep_rwy_wait.delete()
                        await dep_time.delete()
                        await dep_time_wait.delete()
                        await ctx.send("Oops, you ran out of time. Please run the command again.")
            
                    else:

                        ask_arr_rwy = await ctx.send("What is the arrival runway? Reply within 30 seconds.")

                        try:
                            ask_arr_rwy_wait = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 30.0)
                        
                        except asyncio.TimeoutError:
                            await dep_icao.delete()
                            await dep_icao_wait.delete()
                            await arr_icao.delete()
                            await dep_rwy.delete()
                            await dep_rwy_wait.delete()
                            await ask_arr_rwy.delete()
                            await dep_time.delete()
                            await dep_time_wait.delete()
                            await ctx.send("Oops, you ran out of time. Please run the command again.") 
                        
                        else:
                            ask_route = await ctx.send("What is the routing for the group flight? Reply within 30 seconds.")

                            try:
                                ask_route_wait = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 30.0)
                            
                            except asyncio.TimeoutError:
                                await dep_icao.delete()
                                await dep_icao_wait.delete()
                                await arr_icao.delete()
                                await ask_route.delete()
                                await dep_rwy.delete()
                                await dep_rwy_wait.delete()
                                await ask_arr_rwy.delete()
                                await dep_time.delete()
                                await dep_time_wait.delete()
                                await ctx.send("Oops, you ran out of time. Please run the command again.")
                            
                            else:
                                embed = discord.Embed(title=f"Group Flight {datetime.strftime(datetime.utcnow(),'%d-%m-%Y')}", colour = discord.Color.from_rgb(92, 159, 36))
                                embed.add_field(inline=False, name="Departure ICAO:", value=dep_icao_wait.content)
                                embed.add_field(inline=False, name="Departure Runway:", value=dep_rwy_wait.content)
                                embed.add_field(inline=False, name="Arrival ICAO:", value=arr_icao_wait.content)
                                embed.add_field(inline=False, name="Arrival Runway:", value=ask_arr_rwy_wait.content)
                                embed.add_field(inline=False, name="Flight Route:", value=ask_route_wait.content)
                                embed.set_footer(text= f"Group flight created by: {ctx.message.author.display_name}", icon_url=ctx.author.avatar_url)
                                await ctx.send(embed=embed)
                                await dep_icao.delete()
                                await dep_icao_wait.delete()
                                await arr_icao.delete()
                                await ask_route.delete()
                                await dep_rwy.delete()
                                await dep_rwy_wait.delete()
                                await ask_arr_rwy.delete()
                                await ask_route_wait.delete()
                                await ask_route.delete()
                                await dep_time.delete()
                                await dep_time_wait.delete()
                
def setup(bot):
    bot.add_cog(UserCommands(bot))
                    
