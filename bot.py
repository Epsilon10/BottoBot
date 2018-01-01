import discord
from discord.ext import commands
import json
import asyncio

cogs = [
    'cogs.config',
    'cogs.mod',
    'cogs.cr'
    
]

async def get_pre(bot, message):
    with open('settings/config.json') as f:
        data = json.load(f)
    try:
        prefix =data[str(message.guild.id)]['prefix']
        return prefix
    except Exception as e:
        return '.'
bot = commands.Bot(command_prefix=get_pre, description='Bot')


@bot.event
async def on_ready():
    print(f'Bot is online!')
    await bot.change_presence(game=discord.Game(name='.help'))

@bot.event
async def on_member_join(member):
    with open('config/settings.json') as f:
        data = json.load(f)
    try:
        msg = data[str(ctx.guild.id)]['welcome msg']
        ctx.channel.send(msg)
    except Exception as e:
        pass


@bot.check
async def check_channel_blacklist(ctx):
    with open('settings/config.json') as f:
        data = json.load(f)
    try:
        return str(ctx.channel.id) not in data[str(ctx.guild.id)]['blacklists']['channels']
    except Exception as e:
        return True
@bot.check
async def check_user_blacklist(ctx):
    with open('settings/config.json') as f:
        data = json.load(f)
    try:
        return str(ctx.message.author.id) not in data[str(ctx.guild.id)]['blacklists']['users']
    except Exception as e:
        return True

@bot.event
async def on_guild_join(guild):
    my_data = {str(guild.id): {'Name:': guild.name}}
    with open('settings/config.json') as data_file:
        data = json.load(data_file)
        data.update({str(guild.id): {'Name:': guild.name}})
        with open('settings/config.json', 'w') as f:
            f.write(json.dumps(data))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.send(f'You are missing the permission(s) '+','.join(error.missing_perms))
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send(f'Your are missing the the parameter <{error.param}>')
    elif isinstance(error, commands.DisabledCommand):
        await ctx.channel.send('This command is disabled')

@bot.command()
async def ping(ctx):
    ''' Websocket latency'''
    em = discord.Embed()
    em.title = '**Pong! Websocket Latency**'
    em.set_author(name='Cuckoo Bot', icon_url=bot.user.avatar_url)
    em.description = '{0:.3f}'.format(bot.latency * 1000) + ' ms'
    await ctx.channel.send(embed=em)

if __name__ == "__main__":
    for cog in cogs:
        try:
            bot.load_extension(cog)
            print('Loaded extension: {}'.format(cog))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(cog, exc))

bot.run('Mzk2NjY0MDU0OTIxNDI4OTky.DSkttg.wjN181r_V4jgBDba4MnmBGNs13c', bot=bot)






