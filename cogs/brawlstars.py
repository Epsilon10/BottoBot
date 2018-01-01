import discord
from discord.ext import commands
import asyncio
import aiohttp
import async_timeout
import json
from bs4 import BeautifulSoup

class BrawlStars:

    def __init__(self,bot):
        self.bot = bot
        self.values = []

    async def fetch(self,session, url):
        with async_timeout.timeout(10):
            async with session.get(url) as response:
                return await response.text()

    async def get_data(self,url):
        async with aiohttp.ClientSession() as session:
            return await self.fetch(session, url)

    @commands.command()
    async def bsprofile(self,ctx,tag):
        tag = tag.replace('#','').upper()
        try:
            url = f'https://brawlstats.io/players/{tag}'
            page = await self.get_data(url)
            res = await self.bot.loop.run_in_executor(None,self.get_info, page)
            #await ctx.channel.send(', '.join(res))
            em = discord.Embed()
            em.title = res[-2]
            em.add_field(name='Band', value=res[8])
            em.add_field(name='Trophies', value=res[0])
            em.add_field(name='Best Trophies', value=res[1])
            em.add_field(name='victories', value = res[3])
            em.add_field(name='Showdown victories', value = res[4])
            em.add_field(name='Best Time as a Boss', value = res[5])
            em.add_field(name='Best robo rumble time', value = res[6])
            await ctx.channel.send(embed=em)

        except Exception as e:
            print(str(e))

        
    def get_info(self, page):
        print('hi')
        classes = ['trophies', 'victories', 'showdown-victories', 'boss-time', 'robo-time', 'player-name brawlstars-font', 'band-name mr-2']
        soup = BeautifulSoup(page, "lxml")
        vals = []
        for x in classes:
            if x == 'trophies':
                for val in soup.find_all('div', attrs = {'class':x})[:2]:
                    vals.append(val.text)
            val = soup.find('div', attrs = {'class': x}).text
            vals.append(val)
        return vals


        

        
def setup(bot):
    bot.add_cog(BrawlStars(bot))