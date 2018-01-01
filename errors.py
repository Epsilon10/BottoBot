import discord
from discord.ext import commands

class BlackListedChannel(commands.CommandError):
	def __init__(self, channel: discord.TextChannel):
		self.error_msg = 'This bot has been blacklisted in this channel'
