import discord
from discord.ext import commands
from main import bot

class Admin(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @commands.is_owner()
  async def load(self, ctx, cog: str):
    """
    Loads the module specified.
    """
    embed = discord.Embed(title="Loaded cog")
    try:
      bot.load_extension(f"cogs.{cog}")
    except:
      embed.description = f":red_square: Failed to load `{cog}`"
    else:
      embed.description = f":green_square: Successfully loaded `{cog}`"
    embed.set_footer(text=f"Requested by {str(ctx.message.author)}")
    await ctx.reply(embed=embed)

  @commands.command()
  @commands.is_owner()
  async def unload(self, ctx, cog: str):
    """
    Unloads the module specified.
    """
    if cog == "admin":
      await ctx.message.add_reaction("⚠️")
      return
    embed = discord.Embed(title="Unloaded cog")
    try:
      bot.unload_extension(f"cogs.{cog}")
    except:
      embed.description = f":red_square: Failed to unload `{cog}`"
    else:
      embed.description = f":green_square: Successfully unloaded `{cog}`"
    embed.set_footer(text=f"Requested by {str(ctx.message.author)}")
    await ctx.reply(embed=embed)

  @commands.command(aliases=["restart"])
  @commands.is_owner()
  async def reload(self, ctx, cog: str=None):
    """
    Reloads all cogs
    """
    embed = discord.Embed(title="Reloaded cog(s)")
    if cog != None:
      try:
        bot.reload_extension(f"cogs.{cog}")
      except:
        embed.description = (f":red_square: Failed to reload`{cog}`")
      else:
        embed.description = (f":green_square: Successfully reloaded `{cog}`")
    else:
      #temporary list to store reloaded statuses
      temp = []
      extensions = [e for e in bot.extensions]
      for module in extensions:
        try:
          bot.reload_extension(module)
        except:
          temp.append(f":red_square: `{module}`")
        else:
          temp.append(f":green_square: `{module}`")
      embed.description = "\n".join(temp)
    embed.set_footer(text=f"Requested by {str(ctx.message.author)}")
    await ctx.reply(embed=embed)

def setup(bot):
  bot.add_cog(Admin(bot))
