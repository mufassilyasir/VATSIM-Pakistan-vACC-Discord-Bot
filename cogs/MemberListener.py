import discord
import os
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

class MemberListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(Title = f"**Welcome**",colour=discord.Color.from_rgb(92, 159, 36),
        description = f"Welcome to {member.mention}! to {member.guild.name}. Please follow the server rules and have a good time. ")
        await member.send(embed=embed)
        embed = discord.Embed(title = "**Member Joined **", colour = discord.Color.from_rgb(92, 159, 36),timestamp = datetime.utcnow())
        embed.set_thumbnail(url = member.avatar_url)
        fields = [("Who?", member.mention,  False), 
                ("Name", str(member.name), True),
                ("Bot?", member.bot, True),
                ("Created Discord account on", member.created_at.strftime("%d/%m/%Y %H:%M:%S UTC"), True),
                ("Joined this server on", member.joined_at.strftime("%d/%m/%Y %H:%M:%S UTC"), True)]
        
        for name, value, inline in fields:
            embed.add_field(name = name, value = value, inline = inline)
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        await channel.send(embed=embed)


        role1 = discord.utils.get(member.guild.roles, id = 810145043208863774)

        try:
            await member.add_roles(role1)
        except:
            await channel.send(f"Error I could not assign a role to the member {member.mention}")
        else:
            embed1 = discord.Embed(colour = discord.Color.from_rgb(92, 159, 36),timestamp = datetime.utcnow())
            embed1.add_field(inline=False, name = "**Role Assigned:**", value = f"I successfully assigned the **{role1}** role to {member.mention}")
            await channel.send(embed=embed1)
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(title = "**Member Left**",colour=discord.Color.from_rgb(92, 159, 36), timestamp = datetime.utcnow())
        embed.set_thumbnail(url = member.avatar_url)
        embed.add_field(inline=False,name = f"{member}, Left the server!", value = "..." )
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        await channel.send(embed=embed)

def setup(bot):
  bot.add_cog(MemberListener(bot))