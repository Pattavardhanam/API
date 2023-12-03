#imports
from flask import Flask, render_template, request
import requests
import json
from datetime import datetime
import pytz

#Flask App Initialization
app = Flask(__name__)

#Utility Functions
def kelvin_to_celsius(kelvin_temperature):
    return kelvin_temperature - 273.15

def get_humidity_icon(humidity):
    if humidity < 30:
        return "🌞"
    elif 30 <= humidity <= 70:
        return "⛅"
    else:
        return "☔"

#Route Definition
@app.route('/', methods=['GET', 'POST'])
def index(): #Route Function
    city = None
    temperature = None
    humidity = None
    humidity_icon = None
    sunrise = None
    sunset = None
    local_sunrise = None
    local_sunset = None
    error_message = None

    if request.method == 'POST':
        city = request.form['city']
        api_key = 'fc6e40e159e364768339076531970a30'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(url)
        
        if response.status_code == 200:
            weather_data = json.loads(response.text)
            temperature_kelvin = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            sunrise = weather_data['sys']['sunrise']
            sunset = weather_data['sys']['sunset']

            # Convert temperature to Celsius and round to 2 decimal places
            temperature = round(kelvin_to_celsius(temperature_kelvin), 2)

            # Get humidity icon
            humidity_icon = get_humidity_icon(humidity)

            # Extract time zone from API response
            timezone = weather_data['timezone']

            # Convert UTC timestamps to local time
            local_timezone = pytz.timezone(pytz.country_timezones(weather_data['sys']['country'])[0])
            local_sunrise = datetime.utcfromtimestamp(sunrise).replace(tzinfo=pytz.utc).astimezone(local_timezone)
            local_sunset = datetime.utcfromtimestamp(sunset).replace(tzinfo=pytz.utc).astimezone(local_timezone)
        else:
            error_message = f"Error getting weather data for {city}. Please try again."

    return render_template('index.html',
                           city=city,
                           temperature=temperature,
                           humidity=humidity,
                           humidity_icon=humidity_icon,
                           local_sunrise=local_sunrise,
                           local_sunset=local_sunset,
                           error_message=error_message)

#Runs the Flask Appp
if __name__ == '__main__':
    app.run(debug=True)
