import discord
from discord.ext import commands
from main import bot

def xstr(string):
  if string is None: return ""
  else: return string

class Utility(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases = ["ping"])
  async def Ping(self, ctx):
    """
    `g!ping` gets the latency of the bot in milliseconds
    """
    await ctx.message.add_reaction("🏓")
    await ctx.send(f"{round(1000*bot.latency)} ms")

  @commands.command(aliases = ["help"])
  async def Help(self, ctx):
    """
    `g!Help` shows this message
    """
    formatted = {}
    for command in bot.commands:
      original = xstr(formatted.get(command.cog_name))
      if len(command.aliases) == 0:
        formatted[command.cog_name] = f"{original}\n**{command}** {command.help}".strip()
      else:
        aliases = ", ".join(command.aliases)
        formatted[command.cog_name] = f"{original}\n**{command}, {aliases}** {command.help}".strip()
    embed = discord.Embed(title="Help", color=0x3498db)
    for cog in formatted:
      embed.add_field(name = cog, value = formatted[cog], inline = False)
    embed.set_footer(text=f"requested by {str(ctx.message.author)}")
    await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Utility(bot))
