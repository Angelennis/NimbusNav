from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_noaa_forecast(grid_x, grid_y):
    office = 'GRR'
    forecast_url = f"https://api.weather.gov/gridpoints/{office}/{grid_x},{grid_y}/forecast"
    forecast_hourly_url = f"https://api.weather.gov/gridpoints/{office}/{grid_x},{grid_y}/forecast/hourly"

    # Set a timeout (in seconds)
    timeout_seconds = 5

    try:
        forecast_response = requests.get(forecast_url, timeout=timeout_seconds)
        forecast_hourly_response = requests.get(forecast_hourly_url, timeout=timeout_seconds)
        forecast_response.raise_for_status()
        forecast_hourly_response.raise_for_status()
    except requests.RequestException as e:
        return {'error': str(e)}

    forecast_data = forecast_response.json()['properties']
    forecast_hourly_data = forecast_hourly_response.json()['properties']

    return {
        '7_day_forecast': forecast_data,  
        'hourly_forecast': forecast_hourly_data
    }

# Adjusted to handle potential missing keys
def parse_7_day_forecast(forecast_data):
    weekly_forecast = []
    for day in forecast_data.get('periods', []):
        day_forecast = {
            'name': day.get('name', 'N/A'),
            'startTime': day.get('startTime', 'N/A'),
            'endTime': day.get('endTime', 'N/A'),
            'temperatureUnit': day.get('temperatureUnit', 'N/A'),
            'temperatureTrend': day.get('temperatureTrend', 'N/A'),
            #'probabilityOfPrecipitation': {'unitCode': "wmoUnit:percent",'value': null},
            #'dewpoint': {"unitCode": "wmoUnit:degC", "value": -7.2222222222222223},
            #'relativeHumidity': {"unitCode": "wmoUnit:percent","value": 74},
            'windSpeed': day.get('windSpeed', 'N/A'),
            'windDirection': day.get('windDirection', 'N/A'),
            'icon': day.get('icon', 'N/A'),
            'shortForecast': day.get('shortForecast', 'N/A'),
            'detailedForecast': day.get('detailedForecast', 'N/A'),
            'dayTemp': day.get('temperature', 'N/A'),
            'isDaytime': day.get('isDaytime', 'N/A')
        }
        weekly_forecast.append(day_forecast)
    return weekly_forecast

def parse_hourly_forecast(hourly_forecast_data):
    hourly_forecast = []
    for hour in hourly_forecast_data.get('periods', [])[:12]:
        hourly_forecast.append({
            'time': hour['startTime'],
            'temp': hour.get('temperature', 'N/A'),
            'condition': hour.get('shortForecast', 'N/A')
        })
    return hourly_forecast

@app.route('/')
def dashboard():
    grid_x = 63
    grid_y = 50
    weather_data = get_noaa_forecast(grid_x, grid_y)

    if 'error' in weather_data:
        return f"Error fetching data: {weather_data['error']}", 500

    weekly_forecast = parse_7_day_forecast(weather_data['7_day_forecast'])
    hourly_forecast = parse_hourly_forecast(weather_data['hourly_forecast'])

    current_weather = hourly_forecast[0] if hourly_forecast else {}

    return render_template('home.html', weekly_forecast=weekly_forecast, hourly_forecast=hourly_forecast, current_weather=current_weather)
if __name__ == '__main__':
    app.run(debug=True)
