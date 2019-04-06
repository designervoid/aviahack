import telebot
from telebot import types
from datetime import datetime
from db import AviaSchleduleArrival, AviaSchleduleDeparture

TOKEN = '879676273:AAGPMmb_l9m3BVkGgh-U_pkn2X9eU5jtUjw'

state = 0

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


def date_user_today(message):
    date_today = {'today': str(datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d'))}
    return date_today['today']


def date_user_input(message):
    date_today = {'user_input': str(datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d'))}
    return date_today['user_input']


def custom_keyboard_in_commands(message,
                                custom_keyboard, text='Выберите что вам нужно',
                                param_true=True,
                                param_false=False):
    user_markup = telebot.types.ReplyKeyboardMarkup(param_true, param_false)
    user_markup.add(*custom_keyboard)
    bot.send_message(message.from_user.id, text, reply_markup=user_markup)


def resize_custom_keyboard_in_commands(message, custom_keyboard, text):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(*custom_keyboard)
    bot.send_message(message.from_user.id, text, reply_markup=keyboard)


def requests_to_text(message, answer='Укажите номер рейса или регистрационный номер билета'):
    log(message, answer)
    bot.send_message(message.chat.id, '{}'.format(answer))

# MAIN MENU
@bot.message_handler(regexp='start')
def start_handler(message):
    words = 'Расписание', 'Правила перевозки', 'Бронирование перевозки', \
            'Операции с бронированием', 'Проверка наличия мест'
    custom_keyboard_in_commands(message=message, custom_keyboard=words)


@bot.message_handler(regexp='Расписание')
def start_schedule(message):
    cmnds = 'Сегодня', 'Завтра', 'Своя дата', 'Назад к выбору меню'
    custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Выберите дату')


@bot.message_handler(regexp='Правила перевозки')
def start_rules_traffic(message):
    global state
    state = 4
    cmnds = 'Внутрирегиональный', 'Межрегиональный', 'Международный', 'Назад к выбору меню'
    custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Выберите тип рейса')


@bot.message_handler(regexp='Бронирование перевозки')
def start_booking(message):
    requests_to_text(message=message, answer='бронирование')


@bot.message_handler(regexp='Операции с бронированием')
def start_oprtions_wth_booking(message):
    requests_to_text(message=message, answer='операции с бронированием')


@bot.message_handler(regexp='Проверка наличия мест')
def start_avialability_check(message):
    requests_to_text(message=message, answer='проверка наличия мест')

# STATES WITH TICKETS
@bot.message_handler(regexp='Сегодня')
def start_today_check(message):
    global state
    state = 1
    cmnds = 'Прилет', 'Вылет', 'Назад к выбору типа'
    custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Выберите тип')


@bot.message_handler(regexp='Завтра')
def start_tomorrow_check(message):
    global state
    state = 2
    cmnds = 'Прилет', 'Вылет', 'Назад к выбору типа'
    custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Выберите тип')


@bot.message_handler(regexp='Своя дата')
def start_user_input_check(message):
    global state
    state = 3
    global user_input
    user_input = message.from_user.id

# HIDE
@bot.message_handler(regexp='stop')
def stop_handler(message):
    user_hide = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, 'hide',
                     reply_markup=user_hide)

# TEXT
@bot.message_handler(content_types=['text'])
def text_handler(message):
    print(state)
    if state == 1:  # check today date
        if message.text == 'Прилет':
            for data in AviaSchleduleArrival.select():
                check = date_user_today(message)
                if str(check) == str(data.date):
                    requests_to_text(message=message, answer='Airport: {} '
                                                             'Number Flight: {} '
                                                             'Date: {} '
                                                             'Departure: {} '
                                                             'Arrival: {}'.format(data.airport,
                                                                                  data.flight,
                                                                                  data.date,
                                                                                  data.departure,
                                                                                  data.arrival))

        elif message.text == 'Вылет':
            for data in AviaSchleduleArrival.select():
                check = date_user_today(message)
                if str(check) == str(data.date):
                    requests_to_text(message=message, answer='Airport: {} '
                                                             'Number Flight: {} '
                                                             'Date: {} '
                                                             'Departure: {} '
                                                             'Arrival: {}'.format(data.airport,
                                                                                  data.flight,
                                                                                  data.date,
                                                                                  data.departure,
                                                                                  data.arrival))

    elif state == 2:    # check tommorow date
        if message.text == 'Прилет':
            for data in AviaSchleduleArrival.select():
                check = date_user_today(message)
                if str(check) == str(data.date):
                    requests_to_text(message=message, answer='Airport: {} '
                                                             'Number Flight: {} '
                                                             'Date: {} '
                                                             'Departure: {} '
                                                             'Arrival: {}'.format(data.airport,
                                                                                  data.flight,
                                                                                  data.date,
                                                                                  data.departure,
                                                                                  data.arrival))

        elif message.text == 'Вылет':
            for data in AviaSchleduleArrival.select():
                check = date_user_today(message)
                if str(check) == str(data.date):
                    requests_to_text(message=message, answer='Airport: {} '
                                                             'Number Flight: {} '
                                                             'Date: {} '
                                                             'Departure: {} '
                                                             'Arrival: {}'.format(data.airport,
                                                                                  data.flight,
                                                                                  data.date,
                                                                                  data.departure,
                                                                                  data.arrival))


    # elif state 3

    elif state == 4:
        vars_avia_types = 'Внутрирегиональный', 'Межрегиональный', 'Международный'
        companies = 'Аврора', 'Аэрофлот', 'Назад к выбору меню'
        vars_rules_traffic = 'Нормы багажа', 'Перевозка негабаритного багажа', \
                             'Перевозка домашних животных', 'Перевозка спорт инвентаря', 'Назад к выбору меню'

        if message.text in vars_avia_types:
            custom_keyboard_in_commands(message=message, custom_keyboard=companies, text='Выберите авиакомпанию')
        elif message.text in companies:
            resize_custom_keyboard_in_commands(message=message, custom_keyboard=vars_rules_traffic,
                                               text='Выберите категорию')
        elif message.text == 'Перевозка домашних животных':
            requests_to_text(message=message, answer=''' 
                    Если вы решили взять в путешествие своего питомца, обязательно сообщите об этом авиакомпании не позднее, чем за 36 часов до вылета (диспетчеру при бронировании или покупке авиабилета), поскольку перевозка животных производится только с согласия авиакомпании и существуют ограничения по количеству и видам перевозимых животных.''')


    test = 0, 1, 2, 3, 4, 5, 6
    if state in test:
        if message.text == 'Назад к выбору меню':
            start_handler(message=message)

        elif message.text == 'Назад к выбору типа':
            start_schedule(message=message)

        elif message.text == 'Назад к выбору даты':
            start_schedule(message=message)
    # add handler with date of user message


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)

