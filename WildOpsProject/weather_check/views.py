import requests
import json
import os
from django.shortcuts import render
from django.conf import settings

def weather_check(request):
    def calc_wind_dir_text(deg):
        deg_mod = deg % 360
        if deg_mod >= 337.5 or deg_mod < 22.5:
            return "N"
        elif deg_mod < 67.5:
            return "NE"
        elif deg_mod < 112.5:
            return "E"
        elif deg_mod < 157.5:
            return "SE"
        elif deg_mod < 202.5:
            return "S"
        elif deg_mod < 247.5:
            return "SW"
        elif deg_mod < 292.5:
            return "W"
        else:
            return "NW"

    def get_color(value, thresholds):
        try:
            value = float(value)
            if value <= thresholds['green']:
                return 'green'
            elif value <= thresholds['yellow']:
                return 'orange'
            else:
                return 'red'
        except ValueError:
            return 'red'

    def fetch_kp_index():
        kp_url = "https://kjen.dk/kp/kp/get_kp_simple.php"
        try:
            response = requests.get(kp_url)
            response.raise_for_status()
            kp_values = response.text.strip().split('\n')
            latest_kp = kp_values[0] if kp_values else "KP_ERROR"
            highest_kp_24h = kp_values[1] if len(kp_values) > 1 else "KP_ERROR"
            
            if latest_kp != "KP_ERROR":
                return float(latest_kp)
            elif highest_kp_24h != "KP_ERROR":
                return float(highest_kp_24h)
            else:
                return "KP_ERROR"
        except Exception as e:
            return "KP_ERROR"

    api_key = settings.WEATHERAPI_KEY
    rapidapi_key = settings.RAPIDAPI_KEY
    if not api_key:
        return render(request, 'weather_check/weather_error.html', {'error': 'No API key.'})

    lat = request.GET.get('lat', None)
    lon = request.GET.get('lon', None)
    location_str = request.GET.get('location', None)

    if lat and lon:
        query = f"{lat},{lon}"
    elif location_str:
        query = location_str
    else:
        OL_PEJETA_LAT = 0.0076
        OL_PEJETA_LON = 36.8748
        query = f"{OL_PEJETA_LAT},{OL_PEJETA_LON}"

    url = f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={query}&days=1"
    response = requests.get(url)
    data = response.json()

    if 'current' not in data or 'forecast' not in data:
        error_message = data.get('error', {}).get('message', 'No current weather data.')
        return render(request, 'weather_check/weather_error.html', {'error': error_message})

    current = data['current']
    daily = data['forecast']['forecastday'][0]
    weather_info = {
        'text': current['condition']['text'],
        'icon': current['condition']['icon']
    }
    sunrise = daily['astro']['sunrise']
    sunset = daily['astro']['sunset']
    temp = current['temp_c']
    wind_speed = current['wind_kph']
    wind_gust = current.get('gust_kph', 0)
    wind_deg = current['wind_degree']
    wind_dir_text = calc_wind_dir_text(wind_deg)
    precipitation = daily['day'].get('daily_chance_of_rain', 0)
    visibility = current.get('vis_km', 0)
    kp_index = fetch_kp_index()

    # Use absolute path for the weather_thresholds.json file
    thresholds_path = os.path.join(settings.BASE_DIR, 'weather_check', 'data', 'json', 'weather_thresholds.json')
    with open(thresholds_path) as f:
        thresholds = json.load(f)

    context = {
        'weather_info': weather_info,
        'sunrise': sunrise,
        'sunset': sunset,
        'temp': temp,
        'temp_color': get_color(temp, thresholds['temperature']),
        'wind_speed': wind_speed,
        'wind_speed_color': get_color(wind_speed, thresholds['wind_speed']),
        'wind_gust': wind_gust,
        'wind_gust_color': get_color(wind_gust, thresholds['wind_gust']),
        'wind_deg': wind_deg,
        'wind_dir_text': wind_dir_text,
        'precipitation': precipitation,
        'precipitation_color': get_color(precipitation, thresholds['precipitation']),
        'visibility': visibility,
        'visibility_color': get_color(visibility, thresholds['visibility']),
        'kp_index': kp_index,
        'kp_index_color': get_color(kp_index, thresholds['kp_index']),
        'query': query,
        'rapidapi_key': rapidapi_key,
    }
    return render(request, 'weather_check/weather_check.html', context)