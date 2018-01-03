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
        ttt=TTT()
        board = await ttt.draw_board_async()
        prev_board = await ctx.send(f'```{board}```')
        chan = ctx.channel
        for x in range(10):
            await ctx.channel.send(f'{p1.mention} it is your turn.', delete_after=2.0)
            move = None
            def check(m):
                print('Check')
                loop = asyncio.get_event_loop()
                rex = re.compile('[0-3][\,][0-3]')
                if rex.match(m.content):
                    return True
                if m.content is not None and m.author != self.bot.user and m.channel == chan:
                    try:
                        print('bad ' + m.content)
                        loop.create_task(self.fail(ctx))
                    except Exception as e:
                        print('bad: '+m.content)
                        print(str(e))
                return False
            try:
                msg = await self.bot.wait_for('message', timeout=15.0, check=check)

                msg_stuff = msg.content.split(',')
                await msg.delete()
                move = [int(msg_stuff[1])-1,int(msg_stuff[0])-1]


            except asyncio.TimeoutError:
                await ctx.channel.send(f'{p2.mention} wins because the opponent forfeited')
                break

            print('Gone through')
            board = await ttt.draw_board_async(move,'X')
            await prev_board.edit(content=f'```{board}```')

            await ctx.channel.send(f'{p2.mention} if is your turn.', delete_after=1.0)
            try:
                msg = await self.bot.wait_for('message', timeout=15.0, check=check)
                msg_stuff = msg.content.split(',')
                await msg.delete()
                move = [int(msg_stuff[1])-1,int(msg_stuff[0])-1]

            except asyncio.TimeoutError:
                await ctx.channel.send(f'{p1.mention} wins because the opponent forfeited')
                break

            board = await ttt.draw_board_async(move,'O')
            await prev_board.edit(content=f'```{board}```')

    async def fail(self,ctx):
        await ctx.send('Invalid move please try again', delete_after=3.0)



     
def setup(bot):
    bot.add_cog(TicTacToe(bot))

