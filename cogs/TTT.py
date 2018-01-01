import discord
from discord.ext import commands

class TTT:
    def __init__(self):
        self.current_board = [
            ['X',' ',' '],
            [' ','Z',' '],
            ['A',' ',' ']
        ]


    async def draw_board_async(self, move=None, marker=None):
        print(move)
        if move is not None:
            self.current_board[move[0]][move[1]] = marker or ''
        board = ''
        for x in range(3):
            board+= '+---+---+---+\n| {} | {} | {} |\n'.format(self.current_board[x][0],self.current_board[x][1],self.current_board[x][2])
        board += '+---+---+---+'
        print(board)
        return board

        