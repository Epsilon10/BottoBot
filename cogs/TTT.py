import discord
from discord.ext import commands

class TTT:
    def __init__(self):
        self.current_board = [
            [' ',' ',' '],
            [' ',' ',' '],
            [' ',' ',' ']
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

    def win_conditions(self):
        for x in range(3):
            if self.checkEqual2(self.current_board[x]) and ' ' not in self.current_board[x]:
                return True
            elif self.current_board[x][0] == self.current_board[x][1] == self.current_board[x][2] and ' ' != self.current_board[x][0]:
                return True
        if ((self.current_board[0][0] == self.current_board[1][1] == self.current_board[2][2]) and self.current_board[0][0] != ' ') or  ((self.current_board[0][2] == self.current_board[1][1] == self.current_board[2][0]) and self.current_board[0][2] != ' '):
            return True
        return False


    def checkEqual2(iterator):
        return len(set(iterator)) <= 1

        