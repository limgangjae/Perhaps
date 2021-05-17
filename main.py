import os
from discord.ext import commands
from keep_alive import keep_alive

bot = commands.Bot(command_prefix='g!')
bot.help_command = None

#bot.load_extension("cogs.memory_game")
bot.load_extension("cogs.utility")

keep_alive()
bot.run(os.getenv("TOKEN"))
