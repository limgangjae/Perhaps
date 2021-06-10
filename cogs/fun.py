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

    invitation = lambda d=False: [
      [
        Button(label="Decline", style=ButtonStyle.red, disabled=d),
        Button(label="Accept", style=ButtonStyle.green, disabled=d)
      ]
    ]

    msg = await ctx.send(f"**{opponent.mention}, {ctx.message.author.mention} invited you to a game of TicTacToe!**", components=invitation())

    try:

      invite = await bot.wait_for("button_click", check=lambda res: res.user.id == opponent.id and res.message.id == msg.id, timeout=60)

      if invite.component.label == "Decline":
        await invite.respond(type=InteractionType.UpdateMessage, content=f"**{opponent.mention} declined the invitation!**", components=invitation(True))
        return
        
      else:
        await invite.respond(type=InteractionType.UpdateMessage, content=f"**{opponent.mention} accepted the invitation!**", components=invitation(True))
        await asyncio.sleep(1)
        pass
    
    except asyncio.TimeoutError:
      await msg.edit(type=InteractionType.UpdateMessage, content=f"**Timed out!**", components=invitation(True))
      return

    options = [
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0]
    ]

    O = 1
    X = -1

    #the person who has the turn
    turn = random.choice([O, X])


#----------------------------------------------------------------------------------------------------------------


    #updates the board to match the options
    def board(disabled: bool=False):

      board = [[0]*3 for i in range(3)]

      for i in range(3):
        for j in range(3):
          if options[i][j] == O:
            board[i][j] = Button(style=ButtonStyle.green, label="O", id=f"{i} {j}", disabled=True)
          elif options[i][j] == X:
            board[i][j] = Button(style=ButtonStyle.red, label="X", id=f"{i} {j}", disabled=True)
          else:
            board[i][j] = Button(style=ButtonStyle.grey, label="\u200b", id=f"{i} {j}", disabled=disabled)
      return board

    #check if there is a winner
    def has_won():

      #check horizontal
      for x in options:
        if sum(x) == 3 or sum(x) == -3:
          return True

      #check vertical
      for y in range(3):
        v = options[0][y] + options[1][y] + options[2][y]
        if v == 3 or v == -3:
          return True

      #check diagonals
      d = options[0][2] + options[1][1] + options[2][0]
      if d == 3 or d == -3:
        return True

      d = options[0][0] + options[1][1] + options[2][2]
      if d == 3 or d == -3:
        return True

    def is_tie():

      if not ("0" in str(options)) and not has_won():
        return True

    def get_player(team):

      if team == 1:
        return opponent
      else:
        return ctx.message.author


#----------------------------------------------------------------------------------------------------------------


    await msg.edit(f"**{get_player(turn).mention}({turn}) goes first**", components=board())


    while True:
      try:

        #wait 60 seconds for the user who has this turn to react
        res = await bot.wait_for("button_click", check=lambda res: res.user.id == get_player(turn).id and res.message.id == msg.id, timeout=60) 

        #changes the selected option's value depending on who's turn it is
        options[int(res.component.id.split()[0])][int(res.component.id.split()[1])] = turn

        #if there is a winner
        if has_won():
          await res.respond(type=InteractionType.UpdateMessage, content=f"**🎉 {get_player(turn).mention} is the winner! 🎉**", components=board(True))
          return
        elif is_tie():
          await res.respond(type=InteractionType.UpdateMessage, content=f"**Draw!**", components=board(True))
          return
        else:
          turn = -turn
          await res.respond(type=InteractionType.UpdateMessage, content=f"**{get_player(turn).mention}'s turn**", components=board())
          pass

      #if the player in turn times out
      except asyncio.TimeoutError:
        await msg.edit(f"**Timed out! 🎉 {get_player(-turn).mention} is the winner! 🎉**", components=board(True))
        return

def setup(bot):
  bot.add_cog(Fun(bot))
