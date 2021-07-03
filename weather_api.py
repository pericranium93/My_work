import requests
import json
from datetime import datetime


class Forecast:
    def __init__(self, key, lat, lon, count_days=5):
        """
        :param lat: широта (диапазон от -180 до 180)
        :param lon: долгота (диапазон от -90 до 90)
        :param count_days: Колво дней, на которые строится прогноз
        """
        self.__url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric' \
                     f'&appid={key}'
        self.__weather_data = self.__get_api()
        self.count_days = count_days

    def __get_api(self):
        """
        Делаем запрос на API
        :return: Возвращаем словарь с полученными данными
        """
        response = requests.get(self.__url)
        return dict(response.json())

    def get_pressure(self):
        """
        Метод определяет максимальное значение давления в мм.рт.ст на заданной территории за следующие 5 дней,
        считая текущий.
        :return: Возвращает f-строку со значениями даты и давления
        """
        max_pressure = 0
        date_pressure = ''
        n = 0
        for day in self.__weather_data['daily']:
            if n == self.count_days:
                break
            if day['pressure'] > max_pressure:
                max_pressure = day['pressure']
                date_pressure = datetime.utcfromtimestamp(day['dt']).strftime('%d-%m-%Y')
            n += 1
        return f'Максимальное давление равное {round(max_pressure / 1.333)} мм.рт.ст. ' \
               f'будет наблюдаться {date_pressure}'

    def get_temp(self):
        """
        Метод определяет максимальную разницу между ночной и утренней температурой
        на заданной территории за следующие 5 дней, считая текущий.
        :return: Возвращает f-строку со значениями даты и максимальной разницей температуры
        """
        date_temp = ''
        temp = 0
        n = 0
        for day in self.__weather_data['daily']:
            if n == self.count_days:
                break
            max_dif_temp = round(abs(day['temp']['night'] - day['temp']['morn']), 2)
            if max_dif_temp > temp:
                temp = max_dif_temp
                date_temp = datetime.utcfromtimestamp(day['dt']).strftime('%d-%m-%Y')
            n += 1
        return f'Максимальная разница ночной и утренней температур равная {temp} градусов Цельсия ' \
               f'будет наблюдаться {date_temp}'

    def get_forecast(self):
        """
        Возвращает прогноз погоды.
        :return: f-строку с результатами выполнения методов get_pressure и get_temp
        """
        return f'{self.get_pressure()}\n{self.get_temp()}'

# Реализовывать ввод с клавиатуры до конца не стал, т.к. в задании сказано о том, чтобы выводить данные по своему городу
# lat = input('Введите значение широты (от -180 до 180)')
# lon = input('Введите значение долготы (от -90 до 90)')
key = input('Введите значение ключа')


coord_weather = Forecast(key, lat=51.6720400, lon=39.1843000, )
print(coord_weather.get_pressure())
print(coord_weather.get_temp())
print(coord_weather.get_forecast())


response = requests.get(f'https://api.openweathermap.org/data/2.5/onecall?lat=51.6720400&lon=39.1843000&units=metric'
                        f'&appid={key}')

# text_for_me = json.dumps(response.json(), sort_keys=True, indent=4)
# print(text_for_me)

text = dict(response.json())

max_pressure = 0
date_pressure = ''
date_temp = ''
temp = 0
n = 0
for day in text['daily']:
    if n == 5:
        break
    if day['pressure'] > max_pressure:
        max_pressure = day['pressure']
        date_pressure = datetime.utcfromtimestamp(day['dt']).strftime('%d-%m-%Y')
    max_dif_temp = round(abs(day['temp']['night'] - day['temp']['morn']), 2)
    if max_dif_temp > temp:
        temp = max_dif_temp
        date_temp = datetime.utcfromtimestamp(day['dt']).strftime('%d-%m-%Y')
    n += 1

print(f'Максимальное давление в Воронеже будет {date_pressure} = {max_pressure} гПА\n'
      f'Максимальная разница температур будет {date_temp} и составляет {temp} градуса Цельсия')