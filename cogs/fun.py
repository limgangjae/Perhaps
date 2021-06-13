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
  async def tictactoe(self, ctx, opponent: discord.Member=bot.user):
    """
    Starts a game of TicTacToe
    """

    O, X = 1, -1
    turn = random.choice([O, X])
    options = [[0]*3 for i in range(3)]

    def player(team):
      
      if team == O: return opponent
      else: return ctx.message.author

    def board(disabled: bool=False):

      board = options.copy()

      for i in range(3):
        for j in range(3):
          if options[i][j] == O:
            board[i][j] = Button(style=ButtonStyle.green, label="O", id=f"{i} {j}", disabled=True)
          elif options[i][j] == X:
            board[i][j] = Button(style=ButtonStyle.red, label="X", id=f"{i} {j}", disabled=True)
          else:
            board[i][j] = Button(style=ButtonStyle.grey, label=" ", id=f"{i} {j}", disabled=disabled)
      return board

    def has_won():

      #check horizontal and vertical
      for i in range(3):
        if 3 in (abs(sum(options[i])), abs(options[0][i] + options[1][i] + options[2][i])): return True
      #check diagonals
      if 3 in (abs(options[0][2] + options[1][1] + options[2][0]), abs(options[0][0] + options[1][1] + options[2][2])): return True

    def is_draw():

      Olist, Xlist = options.copy()

      for i in range(3):
        for j in range(3):
          #replace the 0s in Olist and Xlist with O and X. if neither player can win in both situations, it is a draw
          if options[i][j] == 0: Olist[i][j], Xlist[i][j] = O, X
      return not has_won(Olist) and not has_won(Xlist)

    if opponent == ctx.message.author:
      await ctx.send("**You cannot play against yourself!**")
      return

    msg = await ctx.send(f"**{player(turn).mention} goes first**", components=board())

    while True:
      try:
        res = await bot.wait_for("button_click", check=lambda res: res.user.id == player(turn).id and res.message.id == msg.id, timeout=40) 
        options[int(res.component.id.split()[0])][int(res.component.id.split()[1])] = turn

        if has_won():
          await res.respond(type=InteractionType.UpdateMessage, content=f"**🎉 {player(turn).mention} is the winner! 🎉**", components=board(True))
          return
        elif is_draw():
          await res.respond(type=InteractionType.UpdateMessage, content=f"**Draw!**", components=board(True))
          return
        else:
          turn = -turn
          await res.respond(type=InteractionType.UpdateMessage, content=f"**{player(turn).mention}'s turn**", components=board())
          pass

      except asyncio.TimeoutError:
        await msg.edit(f"**Timed out! 🎉 {player(-turn).mention} is the winner! 🎉**", components=board(True))
        return


  @commands.command(aliases=["memorygame"])
  async def simon(self, ctx):
    """
    Starts a game of memory skill
    """

    #the length of the sequence the player has to memorize
    difficulty = 4

    #the buttons that the player can interact with
    board = lambda d=False: [
      [
        Button(label=" ", style=ButtonStyle.grey, id="1", disabled=d),
        Button(label=" ", style=ButtonStyle.blue, id="2", disabled=d)
      ],
      [
        Button(label=" ", style=ButtonStyle.green, id="3", disabled=d),
        Button(label=" ", style=ButtonStyle.red, id="4", disabled=d)
      ]
    ]


#----------------------------------------------------------------------------------------------------------------


    #returns a disabled board with the specified button enabled
    def enable_button(x):
      b = board(True)
      for i in range(2):
        for j in range(2):
          if int(board()[i][j].id) == x:
            b[i][j].disabled = False
            return b

    #generates a new sequence
    async def gen(d):

      global sequence

      #the random sequence the player has to replicate by memory
      sequence = [random.choice([1, 2, 3, 4]) for i in range(d)]

      await asyncio.sleep(2)

      for i in sequence:
        await msg.edit("**Generating sequence...**", components=enable_button(i))
        await asyncio.sleep(2)
        await msg.edit(components=board(True))

      await asyncio.sleep(0.3)
      await msg.edit("**Replicate the sequence!**", components=board())


#----------------------------------------------------------------------------------------------------------------


    msg = await ctx.send("**Memory Game Started!**", components=board(True))

    await gen(difficulty)

    
    while True:

      try:

        #if the player has clicked and the input is from the game's message
        res = await bot.wait_for("button_click", check=lambda res: res.user.id == ctx.message.author.id and res.message.id == msg.id, timeout=15)

        #gets the current number in the sequence that the player has to input
        i = sequence.pop(0)

        #if the sequence is empty, meaning that the player has replicated the full sequence
        if not sequence:
          await res.respond(type=InteractionType.UpdateMessage, content="**Advancing to next difficulty...**", components=board(True))
          difficulty += 1
          await gen(difficulty)
          pass
        #if the player input is the same as the current number the player has to input
        elif int(res.component.id) == i:
          await res.respond(type=InteractionType.UpdateMessage, content="**Correct!**", components=board())
          pass
        else:
          await res.respond(type=InteractionType.UpdateMessage, content=f"**Incorrect! Game over\n\nScore: {difficulty-4}**", components=board(True))
          return

      #if the player times out
      except asyncio.TimeoutError:
        await msg.edit(f"**Timed out! Game over\n\nScore: {difficulty-4}**", components=board(True))
        return

def setup(bot):
  bot.add_cog(Fun(bot))
