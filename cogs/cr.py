import discord
from discord.ext import commands
import asyncio
import aiohttp
import async_timeout
import json
BASE_URL = 'http://statsroyale.com/profile/'

class ClashRoyale:
    def __init__(self,bot):
        self.bot = bot

    async def fetch(self,session, url):
        with async_timeout.timeout(10):
            async with session.get(url) as response:
                return await response.json()

    async def get_data(self,url):
        async with aiohttp.ClientSession() as session:
            return await self.fetch(session, url)

    @commands.command()
    async def profile(self,ctx,tag=None):
        ''' Get you CR profile from statsroyale.com '''
        if tag is None:
            with open('settings/tags.json') as f:
                data = json.load(f)
            if str(ctx.message.author.id) in data:
                tag = data[str(ctx.message.author.id)]
                print(tag)
            else:
                await ctx.channel.send('You do not have a saved profile. Please save by doing ```(p)save <tag>```')
        else:
            tag = tag.replace('#','').upper()
        url = f'http://statsroyale.com/profile/{tag}?appjson=1'
        try:
            profile_json = await self.get_data(url)
            em = discord.Embed()
            em.title = profile_json['profile']['name']
            em.add_field(name='Trophies', value=profile_json['profile']['trophies'])
            em.add_field(name='Personal Best', value=profile_json['profile']['maxscore'])
            em.add_field(name='Wins', value=profile_json['profile']['wins'])
            em.add_field(name='Losses', value=profile_json['profile']['losses'])
            em.add_field(name='Level', value=profile_json['profile']['level'])
            em.add_field(name='3 Crown Wins', value=profile_json['profile']['threeCrownWins'])
            em.add_field(name='Max Challenge Wins', value=profile_json['profile']['challenge']['maxWins'])
            em.add_field(name='Clan', value=profile_json['profile']['alliance']['name'])
            em.add_field(name='Donations', value=profile_json['profile']['totalDonations'])
            em.add_field(name='Upcoming Chests', value=', '.join([f'{val}: {key}' for key, val in profile_json['chests'].items()]))
            em.set_footer(text='Powered by statsroyale.com')
            await ctx.channel.send(embed=em)
        except Exception as e:
            await ctx.channel.send(str(e))
            print(str(e))
            return


    @commands.command()
    async def save(self,ctx,tag):
        try:
            tag = tag.replace('#','').upper()
            with open('settings/tags.json') as f:
                data = json.load(f)
            data[str(ctx.message.author.id)] = tag
            with open('settings/tags.json','w') as f:
                json.dump(data,f)
            await ctx.channel.send('Profile saved!')
        except Exception as e:
            print(str(e))


def setup(bot):
    bot.add_cog(ClashRoyale(bot))
