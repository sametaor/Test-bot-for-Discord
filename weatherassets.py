import discord

key_features = {
    'temp' : 'Temperature(in ℃):',
    'feels_like' : 'Feels Like(in ℃):',
    'temp_max' : 'Max Temperature(in ℃):',
    'temp_min' : 'Min Temperature(in ℃):',
    'humidity' : 'Humidity(in %):',
    'pressure' : 'Pressure(in mb):'
}



def parse_data(data):
    return data

def weathermsg(data, location):
    location = location.title()
    weathermessage = discord.Embed(title=f'{location} Weather', description=f'Here is the weather data for {location}.', colour=discord.Colour.blurple())
    for key in data:
        weathermessage.add_field(name=key_features[key], value=data[key], inline=False)
    
    return weathermessage

def error_message(location):
    location = location.title
    return discord.Embed(title='Error', description=f'There was an error retrieving weather data for {location}.', colour=discord.Colour.red())
