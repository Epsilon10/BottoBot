import discord
from discord.ext import commands
from .TTT import TTT
import asyncio
import async_timeout
import re
class TicTacToe:
    def __init__(self,bot):
        self.bot = bot


    @commands.group(invoke_without_command=True)
    async def tictactoe(self,ctx):
        pass

    @tictactoe.command()
    async def start(self, ctx, p2: discord.Member):
        p1 = ctx.message.author
        ttt=TTT(ctx.message.author.id,p2.id)
        board = await ttt.draw_board_async()
        prev_board = await ctx.channel.send(f'```{board}```')

        for x in range(3):
            await ctx.channel.send(f'{p1.mention} it is your turn.', delete_after=5.0)
            move = None
            async def check(m):
                rex = re.compile('[0-3][\,][0-3]')
                if rex.match(m.content):
                    return True
                await ctx.channel.send('Invalid move or format',delete_after=7.0)
                await m.delete()
                return False
            try:
                msg = await self.bot.wait_for('message', timeout=15.0, check=check)
                move = (msg[1]-1,msg[0]-1)
            except asyncio.TimeoutError:
                await ctx.channel.send(f'{p2.mention} wins because the opponent forfeited')
                break

            board = await ttt.draw_board_async(move,'X')
            prev_board = await prev_board.edit(content=f'```{board}```')

            await ctx.channel.send(f'{p2.mention} if is your turn.')
            try:
                msg = await self.bot.wait_for('message', timeout=15.0, check=check)
                move = (msg[1]-1,msg[0]-1)
            except asyncio.TimeoutError:
                await ctx.channel.send(f'{p1.mention} wins because the opponent forfeited')
                break

            board = await ttt.draw_board_async(move,'O')
            prev_board = await prev_board.edit(content=f'```{board}```')


     
def setup(bot):
    bot.add_cog(TicTacToe(bot))

