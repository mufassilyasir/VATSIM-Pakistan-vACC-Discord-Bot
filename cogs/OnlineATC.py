from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from lib.db import db
from dotenv import load_dotenv

import discord
import aiohttp
import os

load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

class OnlineATC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    scheduler = AsyncIOScheduler()
    db.autosave(scheduler)


    async def online(self):
        url = "https://data.vatsim.net/v3/vatsim-data.json"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as response:
                if response.status == 200:
                    data = await response.json()

                    big_list = []
                    for controllers in data['controllers']:
                        callsign = str(controllers['callsign'])
                        big_list.append(callsign)

                        if callsign.startswith("OP") or callsign.startswith("CHR") or callsign.startswith("ISB"):
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)
                            
                            if Bool != "True":
                                if controllers['frequency'] != "199.998":
                                    name = controllers['name']
                                    logon_time = controllers['logon_time']

                                    DATA = {"CHR_APP":"Cherat Approach","CHR-N_APP":"Cherat Approach",
                                    "CHR-S_APP":"Cherat Approach","ISB_CTR":"Islamabad Control",
                                    "OPBN_TWR":"Bannu Tower","OPBN_GND":"Bannu Ground","OPBW_TWR":"Bahawalpur Tower",
                                    "OPBW_GND":"Bahawalpur Ground","OPCH_TWR":"Chitral Tower","OPCH_GND":"Chitral Ground",
                                    "OPDG_TWR":"D.G. Khan Tower","OPDG_GND":"D.G. Khan Ground","OPDI_GND":"D.I. Khan Ground",
                                    "OPDI_TWR":"D.I. Khan Tower","OPFA_TWR":"Faisalabad Tower","OPFA_GND":"Faisalabad Ground",
                                    "OPGT_TWR":"Gilgit Tower","OPGT_GND":"Gilgit Ground","OPIS_APP":"Islamabad Approach",
                                    "OPIS_GND":"Islamabad Ground","OPIS_DEP":"Islamabad Departures","OPIS_DEL":"Islamabad Delivery",
                                    "OPIS_TWR":"Islamabad Tower","OPLA_GND":"Lahore Ground","OPLA_APP":"Lahore Approach","OPLA_TWR":"Lahore Tower",
                                    "OPLR_CTR":"Lahore Control","OPLR-E_CTR":"Lahore Control - East","OPLR-S_CTR":"Lahore Control - South",
                                    "OPLR-W_CTR":"Lahore Control - West","OPMF_GND":"Muzaffarabad Ground","OPMF_TWR":"Muzaffarabad Tower",
                                    "OPMT_TWR":"Multan Tower","OPMT_GND":"Multan Ground","OPPC_GND":"Parachinar Ground","OPPC_TWR":"Parachinar Tower","OPPS_GND":"Peshawar Ground","OPPS_TWR":"Peshawar Tower","OPQT_TWR":"Quetta Tower","OPQT_GND":"Quetta Ground","OPRK_GND":"Rahim Yar Khan Ground","OPRK_TWR":"Rahim Yar Khan Ground","OPRN_TWR":"Chaklala Tower","OPRN_APP":"Chaklala Approach","OPSK_GND":"Sukkur Ground","OPSK_TWR":"Sukkur Tower","OPZB_GND":"Zhob Ground","OPZB_TWR":"Zhob Tower","OPST_GND":"Sialkot Ground","OPST_TWR":"Sialkot Tower","OPSS_GND":"Saidu Sharif Ground","OPSS_TWR":"Saidu Sharif Tower","OPSD_GND":"Skardu Ground","OPSD_TWR":"Skardu Tower","OPDB_GND":"Dalbandin Ground","OPDB_TWR":"Dalbandin Tower","OPGD_GND":"Gwadar Ground","OPGD_TWR":"Gwadar Tower","OPJI_GND":"Jiwani Ground","OPJI_TWR":"Jiwani Tower","OPKC_APP":"Karachi Approach","OPKC_TWR":"Karachi Tower","OPKC_GND":"Karachi Ground","OPKD_TWR":"Hyderabad Tower","OPKH_TWR":"Khuzdar Tower","OPKH_GND":"Khuzdar Ground","OPKR_CTR":"Karachi Control","OPKR-C_CTR":"Karachi Control - Central","OPKR-S_CTR":"Karachi Control - South","OPKR-W_CTR":"Karachi Control - West","OPKR-E_CTR":"Karachi Control - East","OPMJ_TWR":"Moenjodaro Tower","OPMJ_GND":"Moenjodaro Ground","OPNH_GND":"Nawabshah Ground","OPNH_TWR":"Nawabshah Tower","OPOR_TWR":"Ormara Tower","OPOR_GND":"Ormara Ground","OPPG_GND":"Panjgur Ground","OPPG_TWR":"Panjgur Tower","OPPI_TWR":"Pasni Tower","OPPI_GND":"Pasni Ground","OPTU_GND":"Turbat Ground","OPTU_TWR":"Turbat Tower","OPSW_TWR":"Sawan Tower"}
                                    try:
                                        facility = DATA[callsign]
                                    except KeyError:
                                        a=callsign.split('_')
                                        facility_new = f"{a[0]}_{a[2]}"
                                        try:
                                            facility = DATA[facility_new]
                                        except KeyError:
                                            facility = callsign
                                    embed = discord.Embed(title = "ATC Online Notification", description = f"{name} ({controllers['cid']}) is online on **{facility}** ({callsign})!",colour = discord.Color.from_rgb(92, 159, 36),timestamp = datetime.utcnow())
                                    embed.set_footer(text="Pakistan vACC", icon_url=self.bot.user.avatar_url)
                                    online_channel = self.bot.get_channel(917745898690326569)
                                    await online_channel.send(embed=embed, delete_after=56400.0)

                                    value = "True"
                                    db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)

                        
                        if "ASIA_W_FSS" in callsign:
                            Bool = db.field("SELECT Bool FROM onlineatc WHERE CallSign = ?", callsign)

                            if Bool != "True":
                                if controllers['frequency'] != "199.998":

                                    name = controllers['name']
                                    logon_time = controllers['logon_time']
                                    DATA = {"ASIA_W_FSS" : "West Asia Control"}
                                    try:
                                        facility = DATA[callsign]
                                    except KeyError:
                                        a=callsign.split('_')
                                        facility_new = f"{a[0]}_{a[2]}"
                                        try:
                                            facility = DATA[facility_new]
                                        except KeyError:
                                            facility = callsign
                                    embed = discord.Embed(title = "ATC Online Notification", description = f"{name} ({controllers['cid']}) is online on **{facility}** ({callsign})!",colour = discord.Color.from_rgb(92, 159, 36),timestamp = datetime.utcnow())
                                    embed.set_footer(text="Pakistan vACC", icon_url=self.bot.user.avatar_url)
                                    online_channel = self.bot.get_channel(917745898690326569)
                                    await online_channel.send(embed=embed, delete_after=56400.0)

                                    value = "True"
                                    db.execute("INSERT INTO onlineatc (CallSign, TimeOnline, Bool) VALUES (?,?,?)", callsign, logon_time, value)

                    
                    
                    
        all = db.records("SELECT * FROM onlineatc")
        for a in all:
            if a[0] not in big_list:
                db.execute("DELETE FROM onlineatc WHERE CallSign = ?", a[0])

 
    @commands.Cog.listener()
    async def on_ready(self):
        print("online atc")
        self.scheduler.start()
        self.scheduler.add_job(self.online, CronTrigger(second="45"))                                

                    
                    

                       



def setup(bot):
    bot.add_cog(OnlineATC(bot))
