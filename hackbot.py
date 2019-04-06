import telebot
from telebot import types
from datetime import datetime
from db import AviaSchleduleArrival, AviaSchleduleDeparture

TOKEN = '879676273:AAGPMmb_l9m3BVkGgh-U_pkn2X9eU5jtUjw'

base = {}

bot = telebot.TeleBot(TOKEN)

print(bot.get_me())


def log(message, answer):
    print('\n-------')
    print(datetime.now())
    print('Сообщение от {0} {1}. (id = {2}) '
          '\n Текст - {3}'.format(message.from_user.first_name,
                                  message.from_user.last_name,
                                  str(message.from_user.id),
                                  message.text))
    print(answer)


def custom_keyboard_in_commands(message,
                                custom_keyboard, text='Выберите что вам нужно'):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.add(*custom_keyboard)
    bot.send_message(message.from_user.id, text, reply_markup=user_markup)


def requests_to_text(message, answer='Укажите номер рейса или регистрационный номер билета'):
    log(message, answer)
    bot.send_message(message.chat.id, '{}'.format(answer))


def user_data_input(message):
    if message.text == 'Прилет':
        for data in AviaSchleduleArrival.select():
            requests_to_text(message=message, answer='Airport: {} '
                                                     'Number Flight: {} '
                                                     'Date: {} '
                                                     'Departure: {} '
                                                     'Arrival: {}'.format(data.airport,
                                                                          data.flight,
                                                                          data.date,
                                                                          data.departure,
                                                                          data.arrival))
    if message.text == 'Вылет':
        for data in AviaSchleduleDeparture.select():
            requests_to_text(message=message, answer='Airport: {} '
                                                     'Number Flight: {} '
                                                     'Date: {} '
                                                     'Departure: {} '
                                                     'Arrival: {}'.format(data.airport,
                                                                          data.flight,
                                                                          data.date,
                                                                          data.departure,
                                                                          data.arrival))

    if message.text == 'Назад к выбору':
        start_handler(message=message)

    if message.text == 'Назад к выбору даты':
        start_schedule(message=message)

    if message.text == 'Назад к выбору типа':
        start_schedule(message=message)


@bot.message_handler(regexp='start')
def start_handler(message):
    bot.send_message(chat_id=message.from_user.id, text=message.date)
    words = 'Расписание', 'Правила перевозки', 'Бронирование перевозки', \
            'Операции с бронированием', 'Проверка наличия мест'
    custom_keyboard_in_commands(message=message, custom_keyboard=words)


@bot.message_handler(regexp='Расписание')
def start_schedule(message):
    cmnds = 'Сегодня', 'Завтра', 'Своя дата', 'Назад к выбору'
    custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Какая дата вам нужна')


@bot.message_handler(regexp='Правила перевозки')
def start_rules_traffic(message):
    requests_to_text(message=message, answer='правила перевозки')


@bot.message_handler(regexp='Бронирование перевозки')
def start_booking(message):
    requests_to_text(message=message, answer='бронирование')


@bot.message_handler(regexp='Операции с бронированием')
def start_oprtions_wth_booking(message):
    requests_to_text(message=message, answer='операции с бронированием')


@bot.message_handler(regexp='Проверка наличия мест')
def start_avialability_check(message):
    requests_to_text(message=message, answer='проверка наличия мест')


@bot.message_handler(regexp='Сегодня')
def start_today_check(message):
    cmnds = 'Прилет', 'Вылет', 'Назад к выбору типа'
    custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Выберите тип')


@bot.message_handler(regexp='Завтра')
def start_today_check(message):
    cmnds = 'Прилет', 'Вылет', 'Назад к выбору типа'
    custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Выберите тип')


@bot.message_handler(regexp='stop')
def stop_handler(message):
    user_hide = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, 'hide',
                     reply_markup=user_hide)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    user_data_input(message=message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)

