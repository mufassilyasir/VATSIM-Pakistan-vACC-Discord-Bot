import discord
from discord.ext import commands
from datetime import datetime



class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    


#help menu
    @commands.command(description = "Help Menu.")
    @commands.guild_only()
    async def Help(self, ctx, commandSent=None):
        if commandSent != None:
            
            for command in self.bot.commands:
                if commandSent.upper() == command.name.upper():

                    paramString = ""

                    for param in command.clean_params:
                        paramString += param + ", "

                    paramString = paramString[:-2]

                    if len(command.clean_params) == 0:
                        paramString = "None"
                        
                    embed=discord.Embed(title=f"How to use command: {command.name}?", description=command.description, colour = discord.Color.from_rgb(92, 159, 36) ,timestamp = datetime.utcnow())
                    embed.set_footer(icon_url= ctx.message.author.avatar_url, text = f"Information requested by {ctx.message.author.name}")
                    await ctx.send(embed=embed)
    
        else:
            embed=discord.Embed(title="Help Menu!", colour = discord.Color.from_rgb(92, 159, 36) ,timestamp = datetime.utcnow())
            embed.set_footer(icon_url= ctx.message.author.avatar_url, text = f"Information requested by {ctx.message.author.name}")
            embed.add_field(name="Uptime:", value="Displays bot uptime.")
            embed.add_field(name="Ping:", value="Displays time taken by the server to respond back in ms", inline=False)
            embed.add_field(name="Music:", value="Detailed information on how to play music is available through command `-help play`")
            embed.add_field(name="Metar:", value="Displays metar for the specified ICAO", inline=False)
            embed.add_field(name="Traffic:", value="Displays traffic information for Pakistan.", inline=False)
            embed.add_field(inline=False, name="Info", value="Displays information for the specified airport ICAO code.")
            embed.add_field(inline=False, name="Group Flight:", value="Run the command `-groupflight` in group flights channel and the bot will ask you further questions so members can join your group flight as well.")
            await ctx.send(embed=embed)

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Help(bot))