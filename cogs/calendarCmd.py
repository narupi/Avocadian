from discord.ext import commands
import datetime
import pickle
import os.path
import json
import configparser
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class CalendarCmdCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.credentials = self.load_credentials()
        self.calendarId = self.load_calendarId()
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

    def load_calendarId(self):
        inifile = configparser.ConfigParser()
        inifile.read('config.ini')
        return inifile.get('GOOGLE_CALENDAR_ID', 'id')


    def change_date_format(self, date):
        return datetime.datetime.strptime(date, '%Y/%m/%d-%H:%M').isoformat()+'+09:00'


    @commands.command()
    async def register(self, ctx, *args):
        try:
            summary, location, description, start, end, *_ = args[0].split(',')
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
            try: 
                result = self.service.events().insert(calendarId=self.calendarId, body=event).execute()
                await ctx.send("Event id: "+result['id'])
            except Exception as e:
                await ctx.send("Registration Error\n"+e)

        except ValueError:
            await ctx.send("Hint: /register SUMMARY,LOCATION,DESCRIPTION,YY/MM/DD-HH:MM,YY/MM/DD-HH:MM")



def setup(bot):
    bot.add_cog(CalendarCmdCog(bot))
