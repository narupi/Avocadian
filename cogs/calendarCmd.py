from discord.ext import commands
import datetime
import pickle
import os.path
import json
import configparser
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError


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
            except HttpError as e:
                print(e)
                await ctx.send("Registration error")
                await ctx.send("Hint: /register SUMMARY,LOCATION,DESCRIPTION,YY/MM/DD-HH:MM,YY/MM/DD-HH:MM")

        except ValueError:
            await ctx.send("Hint: /register SUMMARY,LOCATION,DESCRIPTION,YY/MM/DD-HH:MM,YY/MM/DD-HH:MM")

    @commands.command()
    async def event(self, ctx):
        now = datetime.datetime.now().isoformat() + "+09:00"
        events_result = self.service.events().list(calendarId=self.calendarId, timeMin=now,
            maxResults=50, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            await ctx.send('No upcoming events.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            message = event['summary']+" ("+event['description']+" ["+event['location']+"]) : "+start+"  "+event['id']
            await ctx.send(message)

    @commands.command()
    async def delete(self, ctx, *args):
        if len(args) != 1:
            await ctx.send("Hint: /delete EVENT_ID")
        else :
            eventId = args[0]
            try:
                event = self.service.events().get(calendarId=self.calendarId, eventId=eventId).execute()
                self.service.events().delete(calendarId=self.calendarId, eventId=eventId).execute()
                start = event['start'].get('dateTime', event['start'].get('date'))
                message = event['summary']+" ("+event['description']+" ["+event['location']+"]) : "+start
                await ctx.send("Delete event : "+message)
            except HttpError as e:
                print(e)
                await ctx.send("Delete error")
                await ctx.send("Hint: /delete EVENT_ID")



def setup(bot):
    bot.add_cog(CalendarCmdCog(bot))
