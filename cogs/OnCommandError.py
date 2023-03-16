import discord
from discord.ext import commands

class OnCommandError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
      
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.message.author.name}, `Err: MissingPermissions`")

        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(f"{ctx.message.author.name}, `Err: CommandNotFound`")
        
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.send(f"{ctx.message.author.name}, `Err: ChannelNotFound`")

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"{ctx.message.author.name}, `Err:BotMissingPermissions` ")

        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f"{ctx.message.author.name}, `Err: MemberNotFound` ")
        
        elif isinstance(error, commands.UserNotFound):
            await ctx.send(f"{ctx.message.author.name}, `Err: UserNotFound` ")
        
        elif isinstance(error, commands.NotOwner):
            await ctx.send(f"{ctx.message.author.mention}, Please don't run this command.")

        elif isinstance(error, commands.ConversionError):
            await ctx.send(f"{ctx.message.author.mention}, `Err:ConversionError`")

        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(f"{ctx.message.author.mention}, `Err:ArgumentParsingError`")

        elif isinstance(error, discord.InvalidArgument):
            await ctx.send(f"{ctx.message.author.mention}, `Err:DiscordInvalidArgument`")

        elif isinstance(error, discord.NotFound):
            await ctx.send(f"{ctx.message.author.mention}, `Err:DiscordNotFound`")
        
        else:
            print(f"Oops an error occured. `Err:{error}`")

def setup(bot):
    bot.add_cog(OnCommandError(bot))