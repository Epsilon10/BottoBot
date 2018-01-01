import discord
from discord.ext import commands
import json
import asyncio

class Configuration():

	def __init__(self, bot):
		self.bot=bot

	@commands.command()
	@commands.has_permissions(manage_roles = True)
	async def setprefix(self,ctx,prefix):
		prefix = str(prefix)

		if len(prefix) > 4:
			await ctx.channel.send(f'Prefix {prefix} is too long. Please choose a shorter one.')
		else:
			with open('settings/config.json') as f:
				data = json.load(f)
			data[str(ctx.guild.id)]['prefix'] = prefix
			with open('settings/config.json', 'w') as f:
				json.dump(data, f)
			await ctx.channel.send(f'Prefix set to {prefix}')

	@commands.command()
	@commands.has_permissions(manage_roles = True)
	async def setwelcomemsg(self,ctx,*,msg: str):
		with open('settings/config.json') as f:
			data=json.load(f)
		data[str(ctx.guild.id)]['welcome msg'] = msg
		with open('settings/config.json', 'w') as f:
				json.dump(data, f)

		await ctx.channel.send(f'Welcome message set to {msg}')

	@commands.command()
	@commands.has_permissions(manage_roles = True)
	async def setlogchannel(self,ctx,channel: discord.TextChannel):
		if channel in ctx.guild.channels:
			with open('settings/config.json') as f:
				data=json.load(f)

			data[str(ctx.guild.id)]['log channel'] = str(channel.id)
			with open('settings/config.json', 'w') as f:
				json.dump(data, f)

		await ctx.channel.send(f'Mod log channel set to {channel}')

	@commands.command()
	@commands.has_permissions(manage_roles = True)
	async def setwelcomemsgchannel(self,ctx,channel: discord.TextChannel):
		if channel in ctx.guild.channels:
			with open('settings/config.json') as f:
				data=json.load(f)

			data[str(ctx.guild.id)]['welcome channel'] = str(channel.id)
			with open('settings/config.json', 'w') as f:
				json.dump(data, f)

		await ctx.channel.send(f'Welcome channel set to {channel}')



def setup(bot):
	bot.add_cog(Configuration(bot))


