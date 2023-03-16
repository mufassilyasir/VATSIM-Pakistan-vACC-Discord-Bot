import discord
import os
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))


class EventLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles:
            if len(before.roles) > len(after.roles):
                action = "Role Removed:"
                roles = [r for r in before.roles if r not in after.roles]
                role = [r.mention for r in roles]
                role_update = str(role)[2:-2]
                embed = discord.Embed(title = "Server Changes", colour = discord.Color.from_rgb(92, 159, 36) ,timestamp = datetime.utcnow())
                embed.add_field(name=action, value=f"{role_update} role was removed from {after.mention}", inline=False)
                channel = self.bot.get_channel(LOG_CHANNEL_ID)
                await channel.send(embed=embed)

            else:
                action = "Role Added:"
                roles = [r for r in after.roles if r not in before.roles]
                role = [r.mention for r in roles]
                role_update = str(role)[2:-2]
                embed = discord.Embed(title = "Server Changes!", colour = discord.Color.from_rgb(92, 159, 36) ,timestamp = datetime.utcnow())
                embed.add_field(name=action, value=f"{role_update} role was added to {after.mention}", inline=False)
                channel = self.bot.get_channel(LOG_CHANNEL_ID)
                await channel.send(embed=embed)
                

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        embed = discord.Embed(title = f"{role.guild.name}!", colour = discord.Color.from_rgb(92, 159, 36) ,timestamp = datetime.utcnow())
        embed.add_field(inline=False, name = "Role Created:", value=f"{role.mention}")
        embed.set_thumbnail(url = role.guild.icon_url)
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        embed = discord.Embed(title = f"{role.guild.name}!", colour = discord.Color.from_rgb(92, 159, 36) ,timestamp = datetime.utcnow())
        embed.add_field(inline=False, name = "Role Deleted:", value=f"{role.name}")
        embed.set_thumbnail(url = role.guild.icon_url)
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        embed1 = discord.Embed(title = "Role Updated!", colour = discord.Color.from_rgb(92, 159, 36) ,timestamp = datetime.utcnow())
        embed1.set_thumbnail(url = after.guild.icon_url)
        embed2 = discord.Embed(title = "Role Updated!", colour = discord.Color.from_rgb(92, 159, 36) ,timestamp = datetime.utcnow())
        embed2.set_thumbnail(url = after.guild.icon_url)
        if before.name != after.name:
            embed = discord.Embed(title = "Role Updated!", colour = discord.Color.from_rgb(92, 159, 36) ,timestamp = datetime.utcnow())
            embed.set_thumbnail(url = after.guild.icon_url)
            
            fields = [("Before:", before, False),
                      ("After:", after, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value = value, inline=inline)
            channel = self.bot.get_channel(LOG_CHANNEL_ID)
            await channel.send(embed=embed)
        
        if before.permissions != after.permissions:  
            for beforepermissions in before.permissions:
                for afterpermissions in after.permissions:
                    if beforepermissions[0] == afterpermissions[0]:
                        if beforepermissions[1] == True and afterpermissions[1] == False:
            
                            fields = [("Role Name:", after.mention, False),
                                 ("Before:", str(beforepermissions)[1:-1], False),
                                    ("After:", str(afterpermissions)[1:-1], False)]

                            for name, value, inline in fields:
                                embed1.add_field(name=name, value = value, inline=inline)

            channel = self.bot.get_channel(LOG_CHANNEL_ID)
            await channel.send(embed=embed1)

            for sec_before_perms in before.permissions:
                for sec_after_perms in after.permissions:
                    if sec_before_perms[0] == sec_after_perms[0]:
                        if sec_before_perms[1] == False and sec_after_perms[1] == True:
                            fields = [("Role Name:", after.mention, False),
                                    ("Before:", str(sec_before_perms)[1:-1], False),
                                    ("After:", str(sec_after_perms)[1:-1], False)]

                            for name, value, inline in fields:
                                embed2.add_field(name=name, value = value, inline=inline)


            channel = self.bot.get_channel(LOG_CHANNEL_ID)
            await channel.send(embed=embed2)


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        embed = discord.Embed(title = f"{channel.guild.name}!", colour = discord.Color.from_rgb(92, 159, 36) ,timestamp = datetime.utcnow())
        embed.add_field(inline=False, name = "Channel Created:", value=f"{channel.mention}")
        embed.set_thumbnail(url = channel.guild.icon_url)
        self.channel = self.bot.get_channel(LOG_CHANNEL_ID)
        await self.channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        embed = discord.Embed(title = f"{channel.guild.name}!", colour = discord.Color.from_rgb(92, 159, 36) ,timestamp = datetime.utcnow())
        embed.add_field(inline=False, name = "Channel Deleted:", value=f"{channel.name}")
        embed.set_thumbnail(url = channel.guild.icon_url)
        self.channel = self.bot.get_channel(LOG_CHANNEL_ID)
        await self.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot:
            if before.content != after.content:
                embed = discord.Embed(title = f"Message edited in channel:", description = f"{after.channel.mention}",colour = discord.Color.from_rgb(92, 159, 36) ,timestamp = datetime.utcnow())
                embed.set_footer(text = f"Edited by {after.author.display_name}", icon_url=after.author.avatar_url)
                embed.add_field(inline=False, name="Before:", value=before.content)
                embed.add_field(inline=False, name="After:", value=after.content)
                self.channel = self.bot.get_channel(LOG_CHANNEL_ID)
                await self.channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            embed = discord.Embed(title = "Message Deleted!",colour = discord.Color.from_rgb(92, 159, 36) ,timestamp = datetime.utcnow())
            embed.set_footer(text = f"Message Author: {message.author.display_name}", icon_url=message.author.avatar_url)
            embed.add_field(inline = False, name=f"Message sent in channel:", value=f"{message.channel.mention}")
            embed.add_field(inline=False, name = "Message Content:", value =message.content)
            log = self.bot.get_channel(LOG_CHANNEL_ID)
            await log.send(embed=embed)



def setup(bot):
    bot.add_cog(EventLogger(bot))