import os
from discord.ext import commands
from keep_alive import keep_alive

bot = commands.Bot(command_prefix="p!")

COGS = ["utility", "admin", "fun", "errorhandler"]

for cog in COGS:
  bot.load_extension(f"cogs.{cog}")

keep_alive()
bot.run(os.getenv("TOKEN"))
