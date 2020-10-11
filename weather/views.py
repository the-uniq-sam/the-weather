import requests
from django.shortcuts import render
from .models import City

# Create your views here.
def index(request):
    
    cities = City.objects.all()

    weather_data = []

    for city in cities:
        url='https://www.metaweather.com/api/location/search/?query={}'
        temp=requests.get(url.format(city)).json()
        url='https://www.metaweather.com/api/location/{}/'
        temp=requests.get(url.format(temp[0]['woeid'])).json()
        #use 0 to 4 for future dates
        city_weather = {
            'city' : city,
            'weather_state' : temp['consolidated_weather'][0]['weather_state_name'],
            'wind_direction' : temp['consolidated_weather'][0]['wind_direction_compass'],
            'min_temp' : int(temp['consolidated_weather'][0]['min_temp']),
            'max_temp' : int(temp['consolidated_weather'][0]['max_temp']),
            'humidity' : temp['consolidated_weather'][0]['humidity'],
            'visibility' : temp['consolidated_weather'][0]['visibility'],
        }
        weather_data.append(city_weather)

    context = {'weather_data' : weather_data}

    return render(request, 'weather/weather.html', context)
