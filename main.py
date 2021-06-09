import os
from discord.ext import commands
from keep_alive import keep_alive

bot = commands.Bot(command_prefix="p!")

bot.load_extension("cogs.utility")
bot.load_extension("cogs.admin")
bot.load_extension("cogs.fun")
bot.load_extension("cogs.errorhandler")

keep_alive()
bot.run(os.getenv("TOKEN"))
