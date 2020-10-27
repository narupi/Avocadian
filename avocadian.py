import discord
from googlecalendar import GoogleCalendar


class Avocadian(discord.Client):
    def __init__(self, cal: GoogleCalendar):
        self.cal = cal

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_reaction_add(self):
        pass

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content[0] == '/':
            command = message.content.split()[0]

            if command == '/ping':
                await message.channel.send('pong')

            if command == '/reg':
                summary, location, description, start, end = message.content[5:].split(',')
                print(summary, location, description, start, end)
                cal.add_event()
