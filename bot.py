import discord
from discord.ext import commands
import json
import asyncio
import sys
from io import StringIO

cogs = [
    'cogs.config',
    'cogs.mod',
    'cogs.cr',
    'cogs.brawlstars',
    'cogs.tictactoe'
    
]
token = open('/Users/moommen/Desktop/token.txt').read()
owner = 299357465236078592

def is_owner():
    return commands.check(lambda ctx: ctx.message.author.id == owner)

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
    with open('settings/config.json') as f:
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

@bot.command(name='bot')
async def bot_info(ctx):
    ''' Gives information about the bot '''
    em = discord.Embed()
    em.title = '**CuckooBot**'
    em.description = 'A discord bot for moderation. Still in development'
    em.add_field(name='Servers', value=str(len(bot.guilds)))
    em.add_field(name='Creator', value='Epsilon#0036')
    em.add_field(name='Source', value='[GitHub](https://github.com/Epsilon10/CuckooBot)')
    em.add_field(name='Invite', value='[Bot Invite](https://discordapp.com/oauth2/authorize?client_id=396664054921428992&scope=bot)')
    em.add_field(name='Created On', value='December 30th 4:02 pm')
    await ctx.channel.send(embed = em)

@bot.command()
async def ping(ctx):
    ''' Websocket latency'''
    em = discord.Embed()
    em.title = '**Pong! Websocket Latency**'
    em.set_author(name='Cuckoo Bot', icon_url=bot.user.avatar_url)
    em.description = '{0:.3f}'.format(bot.latency * 1000) + ' ms'
    await ctx.channel.send(embed=em)


def cleanup_code(content):
    '''Automatically removes code blocks from the code.'''
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return content.replace('```','')

    return content

@is_owner()
@bot.command(name='eval')
async def _eval(ctx,*,code: str):
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    code = cleanup_code(code)
    try:
        exec(code)
        sys.stdout = old_stdout
        await ctx.channel.send('```{}```'.format(redirected_output.getvalue()))
    except Exception as e:
        await ctx.channel.send('```{}```'.format(str(e)))
    


if __name__ == "__main__":
    for cog in cogs:
        try:
            bot.load_extension(cog)
            print('Loaded extension: {}'.format(cog))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(cog, exc))

bot.run(str(token), bot=bot)






