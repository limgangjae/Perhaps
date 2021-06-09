import discord
import asyncio
import random
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from main import bot

class Fun(commands.Cog):
  def __init__(self, bot):
    DiscordComponents(bot)
    self.bot = bot

  @commands.command(aliases=["tic", "ttt"])
  async def tictactoe(self, ctx, opponent: discord.Member):
    """
    Starts a game of TicTacToe
    """

    if opponent == ctx.message.author:
      await ctx.send("**You cannot play against yourself!**")
      return

    options = [
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0]
    ]

    #the person who has the turn
    global turn
    turn = random.choice([ctx.message.author, opponent])


#----------------------------------------------------------------------------------------------------------------


    #updates the board to match the options
    def board(disabled: bool=False):

      board = [[0]*3 for i in range(3)]

      for i in range(3):
        for j in range(3):
          if options[i][j] == -1:
            board[i][j] = Button(style=ButtonStyle.red, label="X", id=f"{i} {j}", disabled=True)
          elif options[i][j] == 1:
            board[i][j] = Button(style=ButtonStyle.green, label="O", id=f"{i} {j}", disabled=True)
          else:
            board[i][j] = Button(style=ButtonStyle.grey, label="\u200b", id=f"{i} {j}", disabled=disabled)
      return board


    #passes the turn to the opponent
    def next_turn():

      global turn

      if turn == ctx.message.author:
        turn = opponent
      else:
        turn = ctx.message.author


    #check if there is a winner
    def has_won():

      #check horizontal
      for x in options:
        if sum(x) == 3:
          return opponent
        elif sum(x) == -3:
          return ctx.message.author

      #check vertical
      for y in range(3):
        v = options[0][y] + options[1][y] + options[2][y]
        if v == 3:
          return opponent
        elif v == -3:
          return ctx.message.author

      #check diagonals
      d = options[0][2] + options[1][1] + options[2][0]
      if d == 3:
        return opponent
      elif d == -3:
        return ctx.message.author

      d = options[0][0] + options[1][1] + options[2][2]
      if d == 3:
        return opponent
      elif d == -3:
        return ctx.message.author


#----------------------------------------------------------------------------------------------------------------


    msg = await ctx.reply(f"**{turn.mention} goes first**", components=board())


    while True:
      try:

        #the check for the interaction
        def check(res):

          global l
          l = [int(i) for i in res.component.id.split()]

          #if the button is grey and the user that clicked has this turn return true
          return options[l[0]][l[1]] == 0 and res.user.id == turn.id and res.message.id == msg.id and res.channel.id == msg.channel.id

        #wait 60 seconds for the user who has this turn to react
        res = await bot.wait_for("button_click", check=check, timeout=60) 

        #changes the selected option's value depending on who's turn it is
        if turn == ctx.message.author:
          options[l[0]][l[1]] = -1
        else:
          options[l[0]][l[1]] = 1

        #if there is a winner
        if has_won():
          await msg.edit(f"**🎉 {has_won().mention} is the winner! 🎉**", components=board(True))
          return
        else:
          next_turn()
          await res.respond(type=InteractionType.UpdateMessage, content=f"**{turn.mention}'s turn**", components=board())
          pass

      #if the player in turn times out
      except asyncio.TimeoutError:
        next_turn()
        await msg.edit(f"**Timed out! 🎉 {turn.mention} is the winner! 🎉**", components=board(True))
        return

def setup(bot):
  bot.add_cog(Fun(bot))
