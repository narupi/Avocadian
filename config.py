import configparser

config = configparser.ConfigParser()

config['DISCORD_API_TOKEN'] = {
    'token': 'SAMPLE_DISCORD_BOT_API_TOKEN'
}
config['GOOGLE_CALENDAR_ID'] = {
    'id': 'SAMPLE_GOOGLE_CALENDAR_ID'
}
with open('config.ini', 'w') as file:
    config.write(file)
