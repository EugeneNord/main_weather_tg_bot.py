import requests
import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
bot = Bot(os.getenv('tg_bot_token'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    '''
    Функция, которая реагирует на команду /start.
    В качестве ответа отображается стикер и сообщение-подсказка,
    которое содержит имя пользователя.
    '''
    await message.answer_sticker(os.getenv('STICKER'))
    await message.answer(f'Привет,{message.from_user.full_name}!\n'
                         f'Напиши название города, и я пришлю сводку погоды!')


@dp.message_handler()
async def get_weather(message: types.Message):
    '''
    Функция принимает сообщение пользователя и возвращает прогноз погоды,
    в случае совпадения с перечнем городов, или сообщение об ошибке,
    если сообщение было неверным.
    '''

    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B',
    }

    try:
        weather_request = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={os.getenv("open_weather_token")}&units=metric'
            )

        data = weather_request.json()

        city = data['name']
        current_temperature = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно, не пойму, что там происходит!'

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrice_timestamp = datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.fromtimestamp(data['sys']['sunset'])

        await message.reply(f'Погода в {city}:\n'
                            f'Температура: {current_temperature}C° {wd}\n'
                            f'Влажность: {humidity}%\n'
                            f'Давление: {pressure} мм.рт.ст\n'
                            f'Ветер: {wind} м.с.\n'
                            f'Восход солнца: {sunrice_timestamp}\n'
                            f'Закат солнца: {sunset_timestamp}')
    except:
        await message.reply("\U0001F62C Проверьте название города \U0001F62C")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
