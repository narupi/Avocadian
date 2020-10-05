import os
from avocadian import Avocadian

TOKEN = os.environ["DISCORD_API_TOKEN"]
client = Avocadian()
client.run(TOKEN)