import nextcord

key_features = {
    'temp' : 'Temp(in ℃):',
    'feels_like' : 'Feels Like(in ℃):',
    'temp_max' : 'Max Temp(in ℃):',
    'temp_min' : 'Min Temp(in ℃):',
    'humidity' : 'Humidity(in %):',
    'pressure' : 'Pressure(in mb):'
}



def parse_data(data):
    return data

def weathermsg(data, location):
    location = location.title()
    weathermessage = nextcord.Embed(title=f'{location} Weather', description=f'Here is the weather data for {location}.', colour=nextcord.Colour.blurple())
    for key in data:
        weathermessage.add_field(name=key_features[key], value=data[key], inline=True)
    
    weathermessage.set_footer(icon_url="https://pbs.twimg.com/profile_images/1173919481082580992/f95OeyEW_400x400.jpg", text = "Powered by openweathermap.org")
    weathermessage.set_thumbnail(url="https://icons.iconarchive.com/icons/papirus-team/papirus-apps/128/weather-icon.png")
    
    return weathermessage

def error_message():
    weathererror =  nextcord.Embed(title='Location Error', description='There was an error retrieving weather data for that location.', colour=nextcord.Colour.red())
    weathererror.set_thumbnail(url="https://cdn0.iconfinder.com/data/icons/kenline/100/12-512.png")
    weathererror.set_footer(icon_url="https://pbs.twimg.com/profile_images/1173919481082580992/f95OeyEW_400x400.jpg", text = "Powered by openweathermap.org")
    return weathererror
