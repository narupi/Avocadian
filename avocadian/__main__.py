import os
import configparser
from avocadian import Avocadian
from googlecalendar import GoogleCalendar

def main():
    inifile = configparser.SafeConfigParser()
    inifile.read('config.ini')
    TOKEN = inifile.get('DISCORD_API_TOKEN', 'token')
    CALENDAR_ID = inifile.get('GOOGLE_CALENDAR_ID', 'id')
    calendar = GoogleCalendar()
    calendar.add_event("A","bB", "C", "2020-04-04", "2020-05-01")

#client = Avocadian(calendar)
#client.run(TOKEN)

if __name__ == '__main__':
    main()
