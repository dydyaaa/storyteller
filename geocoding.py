import os
from opencage.geocoder import OpenCageGeocode
from dotenv import load_dotenv
from typing import Union


def geocoding(city: str) -> Union[str, dict]:
    """
    Функция принимает название города в виде строки использует API
    для получения координат и возвращает их
    в виде словаря {'lat': широта, 'lng': долгота}. 
    Если город не найден, возвращает строку "City not found". 

    Аргументы:
    city (str): Название города.

    Вывод:
    result (dict): Координаты города.
    Или
    result (str): Сообщение об ошибке.
    """
    try:
        load_dotenv()
        geocoder = OpenCageGeocode(os.getenv('GEOCODING_API'))
        results = geocoder.geocode(city)
        if results == []:
            result = 'Город не найден'
            return result
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        result = {'lat': lat, 'lng': lng}
        return result
    except Exception as e:
        result = e
        return str(e)