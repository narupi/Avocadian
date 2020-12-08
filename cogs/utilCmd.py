from discord.ext import commands
from discord import ChannelType
import os
import datetime
import urllib.error
import urllib.request

class UtilCmdCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command()
    async def backup(self, ctx):
        BACKUP_PATH = './backup/'
        if not os.path.exists(BACKUP_PATH):
            os.mkdir(BACKUP_PATH)

        for channel in self.bot.get_all_channels():
            if channel.category and channel.type != ChannelType.voice:
                FILE_PATH = BACKUP_PATH+str(channel.category)+'/'+str(channel)
                if not os.path.exists(FILE_PATH+'/images'):
                    os.makedirs(FILE_PATH+'/images') 
                filename = str(datetime.date.today())
                await ctx.send('save to ' + FILE_PATH+'/'+filename+'.txt')

                with open(FILE_PATH+'/'+filename+'.txt', 'w') as f:
                    async for message in channel.history(oldest_first=True):
                        if message.attachments:
                            try:
                                f.write(str(message.created_at)+' Image id:'+str(message.filename)+'\n')
                                for item in message.attachments:
                                    request = urllib.request.Request(item.url)
                                    request.add_header('User-Agent', 'Mozilla/5.0')
                                    with urllib.request.urlopen(request) as web_image:
                                        image = web_image.read()
                                        with open(FILE_PATH+'/images/'+str(message.created_at)+item.filename, mode='wb') as fi:
                                            fi.write(image)
                            except urllib.error.URLError as e:
                                print(e)
                        else :
                            f.write(str(message.created_at)+' '+str(message.content)+'\n')

        await ctx.send('All channels backup complete.')


def setup(bot):
    bot.add_cog(UtilCmdCog(bot))

