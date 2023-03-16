from discord.ext import commands
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from lib.db import db
from datetime import datetime
from dotenv import load_dotenv
import discord
import os
import requests

load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

class Startup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    scheduler = AsyncIOScheduler()
    db.autosave(scheduler)
    
    async def deletebotlogsmessages(self):
        channel = self.bot.get_channel(917492137250132028)
        messages = await channel.history(limit=600).flatten()
        for m in messages:
            diff = datetime.utcnow() - m.created_at
            if diff.total_seconds() > 86400:
                await m.delete()

    async def updateonlinecontrollers(self):
        headers = {'Authorization' : "$WnY%#MN@U_UAxtg"}
        r = requests.get("https://vatsimpakistan.com/api/update/online-controllers", headers=headers)

        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        
        if r.status_code != 200:
            try:
                s = r.json()
            except:
                s = r.content
            await channel.send(f"**{r.status_code}** Status Code at Update Online ATC API Endpoint, error. ```{s}```")
    
    async def APIcall(self):
        headers = {'Authorization' : "$WnY%#MN@U_UAxtg"}
        r = requests.get("https://vatsimpakistan.com/api/update/stats", headers=headers)
        r1 = requests.get("https://vatsimpakistan.com/api/update/events", headers=headers)
        r2 = requests.get("https://vatsimpakistan.com/api/update/controller-roster", headers=headers)
        r3 = requests.get("https://vatsimpakistan.com/api/update/news", headers=headers)
        r4 = requests.get("https://vatsimpakistan.com/api/update/controllers-top", headers=headers)

        channel = self.bot.get_channel(LOG_CHANNEL_ID)
    
        try:
            s = r.json()
        except:
            s = r.content
        await channel.send(f"**{r.status_code}** Status Code at Update Stats API Endpoint ```{s}```")

        try:
            s = r1.json()
        except:
            s = r1.content
        await channel.send(f"**{r1.status_code}** Status Code at Update Events API Endpoint ```{s}```")
    
        try:
            s = r2.json()
        except:
            s = r2.content
        await channel.send(f"**{r2.status_code}** Status Code at Update Controller Roster API Endpoint ```{s}```")

        try:
            s = r3.json()
        except:
            s = r3.content
        await channel.send(f"**{r3.status_code}** Status Code at Update News API Endpoint ```{s}```")
    
        try:
            s = r4.json()
        except:
            s = r4.content
        await channel.send(f"**{r4.status_code}** Status Code at Update Controller Top API Endpoint ```{s}```")


    @commands.Cog.listener()
    async def on_connect(self):
        self.bot.launch_time = datetime.utcnow()
        print("Bot connected!")

    @commands.Cog.listener()
    async def on_ready(self):
        activity = discord.Activity(name="Pakistan vACC Airspace 👀 | Developed by Mufassil Yasir | v1.1", type=discord.ActivityType.watching)
        await self.bot.change_presence(activity=activity)
        print ("Starting up")
        self.scheduler.start()
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        await channel.send("Getting Ready..... Engines Started! :man_running: ")
        self.scheduler.add_job(self.updateonlinecontrollers, CronTrigger(second=30))
        #self.scheduler.add_job(self.APIcall, CronTrigger(second=0, minute=0, hour="1,3,8,11,14,17,20,23"))
        self.scheduler.add_job(self.deletebotlogsmessages, CronTrigger(second=0, minute=0, hour="23"))

    @commands.command(description = "This command gets you the bot it self statistics. Run the command `-botinfo` and try it out!")
    @commands.guild_only()
    async def uptime(self, ctx):
        embed = discord.Embed(title = "My Statistics:", colour = discord.Color.from_rgb(92, 159, 36), timestamp = datetime.utcnow())
        embed.set_thumbnail(url = self.bot.user.avatar_url)

        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        fields = [("Bot version:", "v1.1", True),
                   ( "Uptime:", f"{days}d, {hours}h, {minutes}m, {seconds}s", True)]
        
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Startup(bot))