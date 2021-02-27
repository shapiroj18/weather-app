import httpx
import os
import json
from datetime import date
from dotenv import load_dotenv

load_dotenv()

def israining():
    """
    Gets weather data for today.
    """
    openweathermap_api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    lat = os.getenv("LAT")
    lon = os.getenv("LON")    
    params = {
        'lat': lat,
        'lon': lon,
        'exclude': 'current,minutely,hourly',
        'appid': openweathermap_api_key,
        'units': 'imperial',
    }
    r = httpx.get('https://api.openweathermap.org/data/2.5/onecall', params=params)
    
    
    for i in r.json()['daily']:
        weather_date = date.fromtimestamp(i['dt'])
        todays_date = date.today()
        if weather_date == todays_date:
            
            temp = i['temp']['day']
            
            
            return temp, i['weather']
                
    
def send_message():
    """
    This checks the weather and sends the message via Telegram.
    """
    temp, weather = israining()
    
    message = ''
    for i in weather:
        if int(str(i['id'])[:1]) in [2, 3, 5]:
            message += f'\U00002614 Grab an Umbrella, it\'s raining today: \nDescription: {i["description"]}.\n'
        elif int(str(i['id'])[:1]) in [6]:
            message += f'\U00002603 Grab a jacket, it\'s going to snow today! \nDescription: {i["description"]}.\n'
            
    message += f'\nThe temperature will be around {round(temp)}°F.'
    
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    params = {
        'chat_id': chat_id,
        'text': message
    }

    resp = httpx.get(f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage', params=params)
    
    
def main():
    send_message()
    
if __name__ == "__main__":
    main()