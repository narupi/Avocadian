import os
from avocadian import Avocadian
from googlecalendar import GoogleCalendar

TOKEN = os.environ["DISCORD_API_TOKEN"]
calendar = GoogleCalendar()
calendar.add_event("A","bB", "C", "2020-04-04", "2020-05-01")

#client = Avocadian(calendar)
#client.run(TOKEN)
