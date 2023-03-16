from discord.ext import commands

import discord
import traceback
import os
import requests
import chat_exporter
from io import *
class AdministratorCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    #@commands.has_any_role(810135707586134032, 804331016168276028)
    #@commands.guild_only()
    async def helpus(self,ctx):

        r1 = requests.get("https://vatsimpakistan.com/api/update/news")
        await ctx.send(r1.status_code)
        embed1 = discord.Embed(title="**Staff Help Menu \n\n Moderation Commands!**", colour=discord.Color.from_rgb(92, 159, 36))
        embed1.set_thumbnail(url = ctx.guild.icon_url)
        embed1.add_field(inline=False, name="Notice:", value="If you are able to run this command you have staff permissions. Hence these commands are for you.")
        embed1.add_field(inline=False, name="Send Announcement:", value="This command sends a custom message to the specified channel. To use this command simply use `-announcement` and the bot will ask you for further questions.")
        embed1.add_field(inline=False, name="Send DM:", value="This command sends a custom message to the specified server member. To use this command simply use `-dm` followed by member id or mention and the bot will ask you for the message that will be sent to the member. An example to run this command can be: \n `-dm 49490627609119727`")
        embed1.add_field(inline=False, name="Kick Member:", value="This command will kick the specified member with a DM (if DM's are allowed by the member) and reason. To use this command simply use `-kick` followed by member id or mention and the bot will ask you for the reason. If you did not provide any reason within the time frame provided by the bot, the bot will automatically kick with reason `No reason provided by the vACC Staff` as default. An example to run this command can be: \n `-kick @mentionthem or their UserID`")
        embed1.add_field(inline=False, name="Delete Messages", value="This command will delete specified number of messages in the channel where it was ran. To use this command simply go to the channel where you wish to delete messages and use `-delete` or `-purge` followed by number of messages that you want to delete. An example to run this command can be: \n `-delete 10`")
        embed1.add_field(inline=False, name="Mute:", value="This command will mute a member. To use this command follow the format `?mute @mention/or their ID [time in hours] [reason]. If time is left empty member will muted forever until manually unmuted. If reason is left empty default reason will be used 'No reason provided by the vACC Staff' ")                                                                    
        embed1.add_field(inline=False, name="Unmute:", value="This command will unmute a member. To use this command follow the format -unmute @mention/or their ID [reason]. If reason is left empty default reason will be used 'No reason provided by the vACC Staff'")    
        embed1.add_field(inline=False, name="Add Member:", value="This command will add a member in the channel where the command was ran with default perms. To use this command follow the format `-addmem and the person you wish to add ID or mention.`")
        embed1.add_field(inline=False, name="Remove member:", value="This command will remove the member in the channel where the command was ran. To use this command follow the format -remmem and the person you wish to remove ID or mention.")
        embed1.add_field(inline=False, name="Add Role:", value="This command will add the role in the channel where the command was ran with default perms. To use this command follow the format -addrole and the role you wish to add ID or mention.")
        embed1.add_field(inline=False, name="Remove role:", value="This command will remove the role in the channel where the command was ran. To use this command follow the format -remrole and the role you wish to remove ID or mention.")
        embed1.add_field(inline=False, name="Add role to everyone:", value="This command will add the role to all members in the server. To use this command follow the format -role_add_all and mention the role you wish to add.")
        embed1.add_field(inline=False, name="Remove role from everyone:", value="This command will remove the role from all members in the server. To use this command follow the format -role_rem_all and the role you wish to remove.")

        await ctx.send(embed=embed1)
    
    
    #social media command
    # @commands.command(hidden= True)
    # @commands.has_any_role(766652488974991390, 804331016168276028)
    # async def socialmedia(self, ctx):
    #     embed = discord.Embed(title="**Nepal vACC Social Media**", colour=discord.Color.from_rgb(92, 159, 36))

    #     embed.add_field(inline=False, name="Website Link:", value="https://nepalvacc.com/")
    #     embed.add_field(inline=False, name="Dashboard Website Link:", value="https://www.members.nepalvacc.com")
    #     embed.add_field(inline=False, name="Instagram Account Link:", value="https://www.instagram.com/vatsim_nepal/")
    #     embed.add_field(inline=False, name="Facebook Account Link:", value="https://www.facebook.com/NepalvACC")
    #     embed.add_field(inline=False, name="Twitter Account Link:", value="https://twitter.com/VatsimN")

    #     await ctx.send(embed=embed)
    #     await ctx.message.delete()
    
    #Rules command
    # @commands.command(hidden=True)
    # @commands.has_any_role(766652488974991390, 804331016168276028)
    # async def send_rules_admin(self, ctx):
    #     embed1 = discord.Embed(title="**Rules**", colour=discord.Color.from_rgb(92, 159, 36))

    #     embed1.add_field(inline=False, name="Discord Terms of Service & Community Guidelines", value="All members must follow Discord's Community Guidelines and Terms of Service at all times.\nToS — https://discordapp.com/terms\nGuidelines — https://discordapp.com/guidelines")
    #     embed1.add_field(inline=False, name="Adhere to VATSIM CoC at all times", value="We ask everyone to show respect to each other at all times. This is Article A1 of the Code of Conduct of the VATSIM Network.\nhttps://www.vatsim.net/documents/code-of-conduct")
    #     embed1.add_field(inline=False, name="Spam, including images, text, or emotes.", value="Do not send spam in the server, including images, text, or emotes. ")
        
    #     embed2 = discord.Embed(title="**Nepal vACC Important Links**", colour=discord.Color.from_rgb(92, 159, 36))

    #     embed2.add_field(inline=False, name="Website Link:", value="https://nepalvacc.com/")
    #     embed2.add_field(inline=False, name="Dashboard Website Link:", value="https://www.members.nepalvacc.com")
    #     embed2.add_field(inline=False, name="Instagram Account Link:", value="https://www.instagram.com/vatsim_nepal/")
    #     embed2.add_field(inline=False, name="Facebook Account Link:", value="https://www.facebook.com/NepalvACC")
    #     embed2.add_field(inline=False, name="Twitter Account Link:", value="https://twitter.com/VatsimN")
    #     embed2.add_field(inline=False, name="Nepal vACC GDPR Link:", value="https://vats.im/NPLGDPR")
    #     embed2.add_field(inline=False, name="Nepal vACC Constituion Link:", value="https://vats.im/NPLConstitution")
    #     embed2.add_field(inline=False, name="Nepal vACC Discord Policy Link:", value="https://vats.im/NPLDiscordPolicy")
        
    #     embed3 = discord.Embed(title="**Nepal vACC Contact Information**", colour=discord.Color.from_rgb(92, 159, 36))
        
    #     embed3.add_field(inline=False, name="To contact Nepal vACC Director", value="**Bikesh Devkota**\n Nepal vACC Director, ACCNPL1\n director_bikesh@nepalvacc.com")
    #     embed3.add_field(inline=False, name="To contact Nepal vACC Deputy Director", value="**Resh B. Bhattarai**\n Nepal vACC Deputy Director, ACCNPL2\n deputy@nepalvacc.com")
    #     embed3.add_field(inline=False, name="To contact Nepal vACC Events & Marketing Director", value="**Ben Pope**\n Nepal vACC Events & Marketing Director, ACCNPL5\n event.director@nepalvacc.com")
    #     await ctx.send(embed=embed1)
    #     await ctx.send(embed=embed2)
    #     await ctx.send(embed=embed3)
    #     await ctx.message.delete()

    @commands.command()
    async def transcriptpls69(self, channel_id :int):
        loading_embed = discord.Embed(color = 0xff0000)
        transcript_channel = self.bot.get_user(388955006633508865)
        loading_embed.set_author(name=f"Standby {transcript_channel.display_name}, this is gonna take some time.", icon_url="https://media.giphy.com/media/sSgvbe1m3n93G/source.gif?cid=ecf05e47a0z65sl6qyqji8f06i3zanuj9s581zjo8pp2jns9&rid=source.gif&ct=g")
        msg = await transcript_channel.send(embed=loading_embed)
        await self.bot.get_channel(channel_id)
        await chat_exporter.quick_export(channel_id, transcript_channel)
        await msg.delete()
        await transcript_channel.send(f"Done check {transcript_channel.mention}")
    
    @commands.command()
    @commands.is_owner()
    async def reload_cog(self, ctx, cog: str):
        await ctx.trigger_typing()
        ext = f"{cog}.py"
        if not os.path.exists(f"./cogs/{ext}"):
            await ctx.send(f"{ctx.message.author.name} I could not unload that Cog. Possibly spelling issue...")
        elif ext.endswith(".py") and not ext.startswith("_"):
            try:
                self.bot.unload_extension(f"cogs.{ext[:-3]}")
                self.bot.load_extension(f"cogs.{ext[:-3]}")
            except Exception:
                desired_trace = traceback.format_exc()
                await ctx.send(f"Failed to reload Cog: `{ext}`\nTrackback Error:\n{desired_trace}")
            else:
                await ctx.send(f"Successfully reloaded Cog {cog}")
    
    @commands.command()
    @commands.is_owner()
    async def load_cog(self, ctx, cog: str):
        await ctx.trigger_typing()
        ext = f"{cog}.py"
        if not os.path.exists(f"./cogs/{ext}"):
            await ctx.send(f"{ctx.message.author.name} I could not load Cog {cog}. Possibly spelling issue...")
        
        elif ext.endswith(".py") and not ext.startswith("_"):
            try:
                self.bot.load_extension(f"cogs.{ext[:-3]}")
            except Exception:
                desired_trace = traceback.format_exc()
                await ctx.send(f"Failed to log Cog: `{ext}`\nTrackback Error:\n{desired_trace}")
            else:
                await ctx.send(f"Successfully reloaded Cog {cog}")




def setup(bot):
    bot.add_cog(AdministratorCommands(bot))