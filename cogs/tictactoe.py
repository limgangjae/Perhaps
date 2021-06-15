import discord
import asyncio
import random
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from main import bot

class TicTacToe(commands.Cog):
  def __init__(self, bot):
    DiscordComponents(bot)
    self.bot = bot

  @commands.command()
  async def rules(self, ctx):
    """
    Explains the rules of Tic-tac-toe
    """
    embed = discord.Embed(title="Tic-tac-toe")
    embed.add_field(name="Definition", value="Tic-tac-toe is a game for two players, X and O, who take turns marking the spaces in a 3x3 grid.")
    embed.add_field(name="How to play", value="When it is your turn, click on a button that has not been marked yet to place your mark.", inline=False)
    embed.add_field(name="Winning", value="In order to win the game, a player must place three of their marks in a horizontal, vertical, or diagonal row.", inline=False)
    await ctx.reply(embed=embed, components=[Button(label="More information", style=5, url="https://en.wikipedia.org/wiki/Tic-tac-toe")])

  @commands.command(aliases=["ttt", "OX"])
  @commands.cooldown(1, 50, commands.BucketType.user)
  async def tictactoe(self, ctx, opponent: discord.Member):
    """
    Starts a game of Tic-tac-toe
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

    msg = await ctx.send(f"**Hey {opponent.mention}, {ctx.message.author.mention} invited you to a game of TicTacToe!**", components=invitation())

    try:
      res = await bot.wait_for("button_click", check=lambda res: res.user == opponent and res.message.id == msg.id, timeout=60)

      if res.component.label == "Accept":
        await res.respond(type=InteractionType.UpdateMessage, content=f"**{opponent.mention} accepted the invitation!**", components=invitation(True))
        await asyncio.sleep(1)
      else:
        await res.respond(type=InteractionType.UpdateMessage, content=f"**{opponent.mention} declined the invitation!**", components=invitation(True))
        return

    except asyncio.TimeoutError:
      await msg.edit("**Timed out!**", components=invitation(True))
      return

    O, X = 1, -1
    turn = random.choice([O, X])
    options = [[0]*3 for i in range(3)]

    def player(team):
      if team == O: return opponent
      else: return ctx.message.author

    #returns a user interactible board that corresponds to the current options
    def board(disabled: bool=False):
      board = [[0]*3 for i in range(3)]
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
      if 3 in (abs(options[0][0] + options[1][1] + options[2][2]), abs(options[0][2] + options[1][1] + options[2][0])): return True

    await msg.edit(f"**{player(turn).mention} goes first**", components=board())

    while True:
      try:
        res = await bot.wait_for("button_click", check=lambda res: res.user == player(turn) and res.message.id == msg.id, timeout=40)
        options[int(res.component.id.split()[0])][int(res.component.id.split()[1])] = turn

        if has_won():
          await res.respond(type=InteractionType.UpdateMessage, content=f"**🎉 {player(turn).mention} is the winner! 🎉**", components=board(True))
          return
        elif "0" not in str(options):
          await res.respond(type=InteractionType.UpdateMessage, content=f"**Draw!**", components=board(True))
          return
        else:
          turn = -turn
          await res.respond(type=InteractionType.UpdateMessage, content=f"**{player(turn).mention}'s turn**", components=board())
          pass

      except asyncio.TimeoutError:
        await msg.edit(f"**Timed out! 🎉 {player(-turn).mention} is the winner! 🎉**", components=board(True))
        return

def setup(bot):
  bot.add_cog(TicTacToe(bot))
