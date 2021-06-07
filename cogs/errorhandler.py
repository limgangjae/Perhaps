import discord
import random
from discord.ext import commands

rfooter = [":(", "Press F to pay respects", "RIP", "no u", "Uhh...", "this is awkward", "'aight Imma head out"]

class ErrorHandler(commands.Cog):

  def __init__(self, bot):
    bot.self = bot

  @commands.Cog.listener()
  async def on_command_error(self, ctx, e):
    if hasattr(ctx.command, "on_error"):
      return
    else:
      embed = discord.Embed(title="An error occured!", description=f"```{e}```")
      embed.set_footer(text=rfooter[random.randint(0, len(rfooter)-1)])
      await ctx.reply(embed=embed)

def setup(bot):
  bot.add_cog(ErrorHandler(bot))
