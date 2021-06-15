import os
from discord.ext import commands
from keep_alive import keep_alive

bot = commands.Bot(command_prefix=commands.when_mentioned_or("p!", "P!"), case_insensitive=True)

cogs = ["utility", "admin", "tictactoe", "errorhandler"]

for cog in cogs:
  bot.load_extension(f"cogs.{cog}")

keep_alive()
bot.run(os.getenv("TOKEN"))
