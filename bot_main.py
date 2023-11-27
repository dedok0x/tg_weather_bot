from telebot import TeleBot
import requests
import datetime
# import schedule
# import time

openweather_api_key = "KEY"

BOT_TOKEN = 'TOKEN'

bot = TeleBot(BOT_TOKEN)

current_state = {}


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    if message.chat.id in current_state:
        del current_state[message.chat.id]
    bot.send_message(message.chat.id, "\
    Здавствуй, я помогу тебе узнать погоду на сегодня.\nУзнать погоду в определенном городе /get_weather"
                           )


@bot.message_handler(func=lambda message: True)
def default_message(message):
    global current_state
    if message.text == '/get_weather':
        current_state[message.chat.id] = 'awaiting_city'
        bot.send_message(message.chat.id, "Введите ваш город")
    elif message.chat.id in current_state and current_state[message.chat.id] == 'awaiting_city':
        city = message.text
        bot.send_message(message.chat.id, get_weather(city, openweather_api_key), parse_mode="HTML")
        del current_state[message.chat.id]  # Удаляем состояние после завершения сценария
    else:
        bot.send_message(message.chat.id, "Прости, не могу тебя понять")


# # Функция для отправки сообщения
# async def send_daily_message(user_id, message):
#     await bot.send_message(user_id, message)


# # Задача для отправки сообщения каждый день в определенное время
# def schedule_daily_message(user_id, message, hour, minute):
#     schedule.every().day.at(f"{hour}:{minute}").do(send_daily_message, user_id, message)


def get_weather(city: str, token: str) -> str:
    try:
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?&q={city}&units=metric&lang=ru&appid={token}")
        data = response.json()
        date_now = datetime.date.today().strftime("%d.%m.%Y")
        answer = (f"{date_now}\n"
                  "---------------------------------------\n"
                  f"Город: <b>{data['name']}</b>\n"
                  f"Сегодня: <b>{data['main']['temp']}℃ </b>{data['weather'][0]['description']}\n"
                  f"Ощущается как: <b>{data['main']['feels_like']}℃</b>\n"
                  f"Минимальная температура за день: <b>{data['main']['temp_min']}℃</b>\n"
                  f"Максимальная температура за день: <b>{data['main']['temp_max']}℃</b>\n"
                  f"Скорость ветра: <b>{data['wind']['speed']}</b> м/c\n"
                  f"Рассвет: <b>{datetime.datetime.fromtimestamp(data['sys']['sunrise']).time()}</b>\n"
                  f"Закат: <b>{datetime.datetime.fromtimestamp(data['sys']['sunset']).time()}</b>")
        return answer
    except Exception:
        return 'Не могу найти погоду по данному городу'


# запуск бота
bot.infinity_polling()

# # Запуск планировщика задач
# while True:
#     schedule.run_pending()
#     time.sleep(1)