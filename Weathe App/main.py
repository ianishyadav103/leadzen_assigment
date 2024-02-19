import requests

api_key = input('Enter yout open weather map api key')

city = input('Enter city name: ')

url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    temp = data['main']['temp']-273.15
    humidity = data['main']['humidity']
    windspeed = data['wind']['speed']
    desc = data['weather'][0]['description']

    print(f'\nTeamprature: {"%.2f" %  (temp)} Celcius ')
    print(f'Description: {desc}\n')
    print("Humiditty:",humidity)
    print("Wind Speed:",windspeed)
else:
    data = response.json()
    print("Error: ",data['message'])
