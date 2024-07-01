from django.shortcuts import HttpResponse
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def ipaddress(request):
    visitor_name = request.GET.get('visitor_name', 'Guest')
    client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))

    try:
#         # Fetch location and weather info based on client IP
        location_response = requests.get(f'http://ip-api.com/json/{client_ip}')
        location_response.raise_for_status()
        location_data = location_response.json()
        city = location_data.get('city', 'Unknown')
        region = location_data.get('regionName', 'Unknown')

        # Fetch weather information using the location
        weather_api_key = "b5cd38be4ccf8894936e6b2aab15cf84"
        weather_response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric')
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        temperature = weather_data['main'].get('temp', 'N/A')

        response_data = {
            'client_ip': client_ip,
            'location': city,
            'greeting': f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}'
        }

    except requests.RequestException as e:
        return Response({'error': str(e)}, status=500)

    return Response(response_data)



