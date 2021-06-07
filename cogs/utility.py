import discord
import random
from discord.ext import commands
from main import bot
from cogs.errorhandler import rfooter

class myhelp(commands.HelpCommand):

  def get_command_signature(self, command):
    return f"{self.clean_prefix}{command.qualified_name} {command.signature}"

  #the help command
  async def send_bot_help(self, mapping: dict=None):
    embed = discord.Embed(title="Help")
    for cog, command in mapping.items():
      s = [f"**{c.qualified_name}** {c.help}" for c in command]
      #if there are commands in this cog
      if s:
        #using getattr() here to avoid raising an error
        cog_name = getattr(cog, "qualified_name", "No Category")
        embed.add_field(name=cog_name, value="\n".join(s), inline=False)
    embed.set_footer(text=f"Requested by {str(self.context.message.author)}")
    await self.context.reply(embed=embed)

  #the command specific help command
  async def send_command_help(self, command: str=None):
    embed = discord.Embed(title=self.get_command_signature(command))
    embed.add_field(name="Help", value=command.help, inline=False)
    a = command.aliases
    #if the command has aliases
    if a:
      embed.add_field(name="Aliases", value=", ".join(a), inline=False)
    embed.set_footer(text=f"Requested by {str(self.context.message.author)}")
    await self.context.reply(embed=embed)

  #help command specific error handler
  async def send_error_message(self, e):
    embed = discord.Embed(title="An error occured!", description=f"```{e}```")
    embed.set_footer(text=rfooter[random.randint(0, len(rfooter)-1)])
    await self.context.reply(embed=embed)

class utility(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.help_command = bot.help_command
    bot.help_command = myhelp(command_attrs={"aliases": ["h"]})
    bot.help_command.cog = self

  @commands.command()
  async def ping(self, ctx):
    """
    Gets the bot's latency to Discord
    """
    await ctx.message.add_reaction("🏓")
    embed = discord.Embed(title="Pong!", description=f"{1000*round(bot.latency, 3)} ms")
    embed.set_footer(text=f"Requested by {str(ctx.message.author)}")
    await ctx.reply(embed=embed)

def setup(bot):
  bot.add_cog(utility(bot))
