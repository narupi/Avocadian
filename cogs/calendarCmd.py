from discord.ext import commands
import datetime
import pickle
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class CalendarCmdCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.credentials = self.load_credentials()
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def load_credentials(self):
        credentials = None
        SCOPES = ['https://www.googleapis.com/auth/calendar']

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                credentials = flow.run_local_server()
            with open('token.pickle', 'wb') as token:
                pickle.dump(credentials, token)
        
        return credentials

    def change_date_format(self, date):
        return datetime.datetime.strptime(date, '%Y-%m-%d').isoformat()+'Z'


    @commands.command()
    async def register(self, ctx, *args):
        await ctx.send("tourokusita")
        summary, location, description, start, end = args[0].split(',')

        event = {
                'summary': '{}'.format(summary),
                'location': '{}'.format(location),
                'description': '{}'.format(description),
                'start': {
                    'dateTime': '{}'.format(self.change_date_format(start)),
                    'timeZone': 'Japan',
                    },
                'end': {
                    'dateTime': '{}'.format(self.change_date_format(end)),
                    'timeZone': 'Japan',
                    },
                }
        print(event)
#        result = self.service.events().insert(calendarId='', body=event).execute()


def setup(bot):
    bot.add_cog(CalendarCmdCog(bot))
