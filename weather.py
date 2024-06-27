import requests
import datetime
import os
from dotenv import load_dotenv
from typing import Union


def get_weather(coordinates) -> Union[str, dict]:
    """
    Функция принимает долготу и широту в виде двух чисел с плавущей точкой, 
    использует API для получения данных о погоде и возвращает 
    подробную информацию о погодных условиях завтра в виде
    словаря.

    Аргументы:
    latitude (float): Широта
    longitude (float): Долгота

    Вывод:
    result (dict): Информация о погоде.
    Или
    result (str): Сообщение об ошибке.
    """
    try:
        latitude = coordinates['lat']
        longitude = coordinates['lng']
        load_dotenv()
        api_key = os.getenv('WEATHER_API')
        url = f'http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}&units=metric'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            tomorrow = f'{str(datetime.date.today() + datetime.timedelta(days=1))} 12:00:00'
            forecast_tomorrow = []
            for forecast in data['list']:
                forecast_time = forecast['dt_txt']
                if forecast_time == tomorrow:
                    forecast_tomorrow.append(forecast)
            result = {'temp': forecast_tomorrow[0]['main']['temp'],
                    'main': forecast_tomorrow[0]['weather'][0]['main'],
                    'wind_speed': forecast_tomorrow[0]['wind']['speed']}
            return result
        else:
            result = 'Ошибка подключения к серверу.'
            return result
    except Exception as e:
        result = str(e)
        return result