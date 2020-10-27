import discord
from discord.ext import commands
import traceback 
import configparser


BOT_COGS = [
    'cogs.debugCmd',
    'cogs.calendarCmd'

]

class Avocadian(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)

        for cog in BOT_COGS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        print('BOT起動')

if __name__ == '__main__':
    inifile = configparser.ConfigParser()
    inifile.read('config.ini')
    TOKEN = inifile.get('DISCORD_API_TOKEN', 'token')

    bot = Avocadian(command_prefix='/')
    bot.run(TOKEN) 
