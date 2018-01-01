import discord
from discord.ext import commands
import json
import asyncio
import datetime
class Mod:
    def __init__(self, bot):
        self.bot = bot
    

    @commands.has_permissions(kick_members=True)
    @commands.group(invoke_without_command=True)
    async def blacklist(self, ctx):
        '''Blacklist a channel, user, or command'''
        await ctx.channel.send(f'```{ctx.prefix}blacklist <user>|<channel>|<command>```')
    @blacklist.command()
    async def channel(self, ctx, chan: discord.TextChannel):
        with open('settings/config.json') as f:
            data=json.load(f)
        try:
            if 'blacklists' not in data[str(ctx.guild.id)]:
                data[str(ctx.guild.id)]['blacklists'] = {}
                data[str(ctx.guild.id)]['blacklists']['channels'] = []
            if str(chan.id) not in data[str(ctx.guild.id)]['blacklists']['channels']:
                vals = data[str(ctx.guild.id)]['blacklists']['channels']
                vals.append(str(chan.id))
                print(vals)
                data[str(ctx.guild.id)]['blacklists']['channels'] = vals
            with open('settings/config.json', 'w') as f:
                json.dump(data,f)

            await ctx.channel.send(f'This bot has been disabled in {chan}')
        except Exception as e:
            print(str(e))

    @blacklist.command()
    async def user(self, ctx, user: discord.Member):
        with open('settings/config.json') as f:
            data=json.load(f)
        try:
            if 'blacklists' not in data[str(ctx.guild.id)]:
                data[str(ctx.guild.id)]['blacklists'] = {}
            if 'users' not in data[str(ctx.guild.id)]['blacklists']:
                data[str(ctx.guild.id)]['blacklists']['users'] = []
            if str(user.id) not in data[str(ctx.guild.id)]['blacklists']['users']:
                vals = data[str(ctx.guild.id)]['blacklists']['users']
                vals.append(str(user.id))
                print(vals)
                data[str(ctx.guild.id)]['blacklists']['users'] = vals
            with open('settings/config.json', 'w') as f:
                json.dump(data,f)

            await ctx.channel.send('This user has been blacklisted')
        except Exception as e:
            print(str(e))
    
        
    @commands.group(invoke_without_command=True)
    @commands.has_permissions(kick_members=True)
    async def whitelist(self,ctx):
        '''Remove a channel, user, or command from bot's blacklist'''
        await ctx.channel.send(f'```{ctx.prefix}whitelist <user>|<channel>|<command>```')
    @whitelist.command()
    async def channel(self,ctx,chan: discord.TextChannel):
        with open('settings/config.json') as f:
            data = json.load(f)
        try:
            vals=data[str(ctx.guild.id)]['blacklists']['channels'] 
            try:
                vals.remove(str(chan.id))
                data[str(ctx.guild.id)]['blacklists']['channels'] = vals
                with open('settings/config.json','w') as f:
                    json.dump(data,f)
                await ctx.channel.send('channel whitelisted!')
            except ValueError:
                await ctx.channel.send('That channel isn\'t blacklisted')

        except KeyError:
            await ctx.channel.send('That channel isn\'t blacklisted')

    @whitelist.command()
    async def user(self,ctx,user: discord.Member):
        with open('settings/config.json') as f:
            data = json.load(f)
        try:
            vals=data[str(ctx.guild.id)]['blacklists']['users'] 
            try:
                vals.remove(str(user.id))
                data[str(ctx.guild.id)]['blacklists']['users'] = vals
                with open('settings/config.json','w') as f:
                    json.dump(data,f)
                await ctx.channel.send('User whitelisted!')
            except ValueError:
                await ctx.channel.send('That user isn\'t blacklisted')

        except KeyError:
            await ctx.channel.send('That user isn\'t blacklisted')
    
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def announce(self,ctx,channel: discord.TextChannel, *,message):
        '''
        Send an announcement with the bot
        ''' 
        await channel.send(message)


    @commands.command()            
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user: discord.Member, *,reason=None):    
        '''
        Kicks a user
        ''' 
        await user.kick()
        await ctx.channel.send(f'**{user.name}#{user.discriminator} has been kicked.** Get outta town')
        await self.mod_log_entry(user,ctx.user, 'Kick', str(ctx.guild.id), reason)
        
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, user: discord.Member, *,reason=None):    
        '''
        Ban a user
        '''  
        await user.ban()
        await ctx.channel.send(f'**{user.name}#{user.discriminator} has been banned.** Hes gone for good my friend, but you probably don\'t want him back considering you banned him')
        await self.mod_log_entry(user,ctx.user, 'Ban',str(ctx.guild.id), reason)

    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def addrole(self, ctx, user: discord.Member, *,role_name: str):
        role = discord.utils.get(ctx.guild.roles, name=role_name)

        if role is not None:
            try:
                await user.add_roles(roler)
                await ctx.channel.send(f'**{user.name}#{user.discriminator}** now has the role *{role.name}*')
            except Exception as e:
                await ctx.channel.send("You don't have the permission **Manage Roles** to perform this action")
        else:
            await ctx.channel.send("This role does not exist")

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def mute(self, ctx, user: discord.Member, *, reason=None):
        '''
        Mutes a user
        '''
        await ctx.channel.set_permissions(user, send_messages=False)
        await ctx.channel.send(f'**{user.name}#{user.discriminator} has been muted**')
        await self.mod_log_entry(user,ctx.message.author, 'Mute', str(ctx.guild.id),reason)
        

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def unmute(self, ctx, user: discord.Member, *,reason=None):
        ''' Unmutes a user'''
        await ctx.channel.set_permissions(user, send_messages=True)
        await ctx.channel.send(f'**{user.name}#{user.discriminator} has been unmuted**')
        await self.mod_log_entry(user,ctx.message.author, 'Unmute', str(ctx.guild.id),reason)
        

    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def warn(self, ctx, user: discord.Member, *,reason=None):
        ''' Warns a user '''
        await ctx.channel.send(f'**{user.name}#{user.discriminator} has been warned.**')
        await user.send(f'You have been warned in {ctx.guild.name} for {reason or "Not disclosed yet."}. Contact {ctx.message.author.name}#{ctx.message.author.discriminator} if you have any questions.')
        await self.mod_log_entry(user,ctx.message.author, 'Warn', str(ctx.guild.id),reason)
    
    

    async def mod_log_entry(self,user, moderator, action, guild_id,reason):
        print(guild_id)
        with open('settings/config.json') as f:
            data = json.load(f)
        chan = data[guild_id]['log channel'] or None
        
        if chan is not None:
            em = discord.Embed()
            em.title = action
            em.add_field(name='**User**', value=f'{user.name}#{user.discriminator}')
            em.add_field(name='**User id**', value=str(user.id))
            em.add_field(name='Moderator responsible', value=f'{moderator.name}#{moderator.discriminator}')
            em.add_field(name='Reason', value=reason or 'Not specified')
            em.set_thumbnail(url=str(user.avatar_url))
            em.set_footer(text=str(datetime.datetime.now()), icon_url=str(moderator.avatar_url))
            await self.bot.get_channel(int(chan)).send(embed=em)
        
        
def setup(bot):
    bot.add_cog(Mod(bot))


