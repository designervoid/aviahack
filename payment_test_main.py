import telebot
from telebot import types
from datetime import datetime
from db import AviaSchleduleArrival, AviaSchleduleDeparture, UserData
from config import TOKEN
from config import MESSAGES, PAYMENTS_PROVIDER_TOKEN, AVIA_IMAGE_URL
from datetime import datetime
from datetime import timedelta



STATE = 0
provider_token = '381764678:TEST:9316'
PRICE = types.LabeledPrice(label='АвиаБилет', amount=422200)


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
    date_today = {'today': str(datetime.utcfromtimestamp(message.date).strftime('%d-%m-%Y'))}
    return date_today['today']


def date_user_input(message):
    date_today = {'user_input': str(datetime.utcfromtimestamp(message.date).strftime('%d-%m-%Y'))}
    return date_today['user_input']


def custom_keyboard_in_commands(message,
                                custom_keyboard, text='Выберите что вам нужно'):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False, True)
    user_markup.add(*custom_keyboard)
    bot.send_message(message.from_user.id, text, reply_markup=user_markup)


def resize_custom_keyboard_in_commands(message, custom_keyboard, text):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*custom_keyboard)
    bot.send_message(message.from_user.id, text, reply_markup=keyboard)


def requests_to_text(message, answer='Укажите номер рейса или регистрационный номер билета'):
    log(message, answer)
    bot.send_message(message.chat.id, '{}'.format(answer))

# MAIN MENU
@bot.message_handler(commands=['start'])
def start_handler(message):
    words = 'Расписание', 'Правила перевозки', 'Бронирование перевозки', \
            'Операции с бронированием', 'Проверка наличия мест'
    custom_keyboard_in_commands(message=message, custom_keyboard=words, text='Здравствуйте. Вас приветствует '
                                                                             'консультант авиакомпании Аврора.'
                                                                              ' Чем могу помочь?')


@bot.message_handler(commands=['schedule'])
@bot.message_handler(regexp='Расписание')
def start_schedule(message):
    global STATE
    STATE = 1
    cmnds = 'Сегодня', 'Завтра', 'Своя дата', 'Назад к выбору меню'
    custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Выберите дату для просмотра расписания '
                                                                             'авиарейса')


@bot.message_handler(commands=['rules_traffic'])
@bot.message_handler(regexp='Правила перевозки')
def start_rules_traffic(message):
    global STATE
    STATE = 5
    cmnds = 'Внутрирегиональный', 'Межрегиональный', 'Международный', 'Назад к выбору меню'
    custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Выберите тип рейса')

# START BOOKING
@bot.message_handler(commands=['/booking'])
@bot.message_handler(regexp='Бронирование перевозки')
def start_booking(message):
    global STATE
    STATE = 6
    cmnds = 'На этой неделе', 'В следующем месяце', 'Назад к выбору меню'
    resize_custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Выберите промежуток')


@bot.message_handler(regexp='На этой неделе')
def start_booking_time_this_week(message):
    global STATE
    STATE = 7
    requests_to_text(message=message, answer='Введите ваше имя и номер')


@bot.message_handler(regexp='В следующем месяце')
def start_booking_time_this_week(message):
    global STATE
    STATE = 8
    requests_to_text(message=message, answer='Введите ваше имя и номер')


@bot.message_handler(commands=['operations_with_booking'])
@bot.message_handler(regexp='Операции с бронированием')
def start_oprtions_wth_booking(message):
    global STATE
    STATE = 10
    cmnds = 'Отмена бронирования', 'Обмен авиабилета', 'Доп. услуги', 'Назад к выбору меню'
    custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Выберите тип операции')


@bot.message_handler(commands=['operations_with_places'])
@bot.message_handler(regexp='Проверка наличия мест')
def start_oprtions_wth_places(message):
    global STATE
    STATE = 9
    requests_to_text(message=message, answer='Введите номер рейса и фамилию')


@bot.message_handler(commands=['terms'])
def command_terms(message):
    bot.send_message(message.chat.id,
                     'Инфо о авиа')

# PAYMENT
@bot.message_handler(commands=['pay'])
@bot.message_handler(regexp='Оплатить')
def command_pay(message, text='Демонстрация свободных мест',
                title=MESSAGES['tm_title'], description=MESSAGES['tm_description'],
                prices=PRICE, photo_url=AVIA_IMAGE_URL):
    bot.send_message(message.chat.id,
                     text, parse_mode='Markdown')
    bot.send_invoice(message.chat.id,
                     title=title,
                     description=description,
                     provider_token=PAYMENTS_PROVIDER_TOKEN,
                     currency='RUB',
                     photo_url=photo_url,
                     photo_height=512,  # !=0/None, иначе изображение не покажется
                     photo_width=512,
                     photo_size=512,
                     is_flexible=False,  # True если конечная цена зависит от способа доставки
                     prices=[prices],
                     start_parameter='avia-ticket-example',
                     invoice_payload='some-invoice-payload-for-our-internal-use'
                     )


@bot.message_handler(commands=['pay_business'])
def command_pay_business(message):
    PRICE_BUSINESS = types.LabeledPrice(label='АвиаБилет Бизнес', amount=4222200)
    command_pay(message, text='Ваш счет к оплате',
                title=MESSAGES['tm_title'], description='Бизнес-класс',
                prices=PRICE_BUSINESS, photo_url=None)


@bot.shipping_query_handler(func=lambda query: True)
def shipping(query):
    print(query)
    bot.answer_shipping_query(query.id, ok=True,
                              error_message='Повторите позже!')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(query):
    bot.answer_pre_checkout_query(query.id, ok=True,
                                  error_message="Повторите позже!")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     'Спасибо за оплату! Снято `{} {}`'.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')

# STATES WITH TICKETS
@bot.message_handler(commands=['today'])
@bot.message_handler(regexp='Сегодня')
def start_today_check(message):
    global STATE
    STATE = 2
    cmnds = 'Прибытие', 'Отправление', 'Назад к выбору типа'
    custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Выберите тип отправки')


@bot.message_handler(commands=['tomorrow'])
@bot.message_handler(regexp='Завтра')
def start_tomorrow_check(message):
    global STATE
    STATE = 3
    cmnds = 'Прибытие', 'Отправление', 'Назад к выбору типа'
    custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Выберите тип отправки')


@bot.message_handler(regexp='Своя дата')
def start_user_input_check(message):
    global STATE
    STATE = 4
    global user_input
    requests_to_text(message=message, answer='Введите дату')


@bot.message_handler(regexp='Пересесть в бизнес-класс')
def start_sit_business(message):
    global STATE
    STATE = 11
    requests_to_text(message=message, answer='Введите номер вашего авиабилета')


@bot.message_handler(regexp='Докупить багаж')
def start_buy_bagadge(message):
    global STATE
    STATE = 12
    requests_to_text(message=message, answer='Введите номер вашего авиабилета')


# HIDE
@bot.message_handler(commands=['stop'])
def stop_handler(message):
    user_hide = telebot.types.ReplyKeyboardRemove()

# TEXT
@bot.message_handler(content_types=['text'])
def text_handler(message):
    print(STATE)
    if STATE == 0 or STATE == 1:
        if message.text == 'Назад к выбору меню':
            start_handler(message=message)

    elif STATE == 2:  # check today date
        if message.text == 'Прибытие':
            for data in AviaSchleduleArrival.select():
                check = date_user_today(message)
                if str(check) == str(data.date):
                    requests_to_text(message=message, answer='Airport: {} \n'
                                                             'Number Flight: {} \n'
                                                             'Date: {} \n'
                                                             'Departure: {} \n'
                                                             'Arrival: {}'.format(data.airport,
                                                                                  data.flight,
                                                                                  data.date,
                                                                                  data.departure,
                                                                                  data.arrival))

        elif message.text == 'Отправление':
            for data in AviaSchleduleDeparture.select():
                check = date_user_today(message)
                if str(check) == str(data.date):
                    requests_to_text(message=message, answer='Airport: {} \n'
                                                             'Number Flight: {} \n'
                                                             'Date: {} \n'
                                                             'Departure: {} \n'
                                                             'Arrival: {}'.format(data.airport,
                                                                                  data.flight,
                                                                                  data.date,
                                                                                  data.departure,
                                                                                  data.arrival))
        elif message.text == 'Назад к выбору меню':
            start_handler(message=message)

    elif STATE == 3:    # check tommorow date
        if message.text == 'Прибытие':
            for data in AviaSchleduleArrival.select():
                next_day = (datetime.now() + timedelta(days=1)).strftime('%d-%m-%Y')
                if str(next_day) == str(data.date):
                    requests_to_text(message=message, answer='Airport: {} \n'
                                                             'Number Flight: {} \n'
                                                             'Date: {} \n'
                                                             'Departure: {} \n'
                                                             'Arrival: {}'.format(data.airport,
                                                                                  data.flight,
                                                                                  data.date,
                                                                                  data.departure,
                                                                                  data.arrival))

        elif message.text == 'Отправление':
            for data in AviaSchleduleDeparture.select():
                next_day = (datetime.now() + timedelta(days=0)).strftime('%d-%m-%Y')
                if str(next_day) == str(data.date):
                    requests_to_text(message=message, answer='Airport: {} \n'
                                                             'Number Flight: {} \n'
                                                             'Date: {} \n'
                                                             'Departure: {} \n'
                                                             'Arrival: {}'.format(data.airport,
                                                                                  data.flight,
                                                                                  data.date,
                                                                                  data.departure,
                                                                                  data.arrival))

        elif message.text == 'Назад к выбору меню':
            start_handler(message=message)

    elif STATE == 4:
        if message.text == 'Назад к выбору меню':
            start_handler(message=message)
        elif message.text:
            user_input_data = message.text
            for data in AviaSchleduleArrival.select():
                if str(user_input_data) == str(data.date):
                    requests_to_text(message=message, answer='Airport: {} \n'
                                                             'Number Flight: {} \n'
                                                             'Date: {} \n'
                                                             'Departure: {} \n'
                                                             'Arrival: {}'.format(data.airport,
                                                                                  data.flight,
                                                                                  data.date,
                                                                                  data.departure,
                                                                                  data.arrival))

            for data in AviaSchleduleDeparture.select():
                if str(user_input_data) == str(data.date):
                    requests_to_text(message=message, answer='Airport: {} \n'
                                                             'Number Flight: {} \n'
                                                             'Date: {} \n'
                                                             'Departure: {} \n'
                                                             'Arrival: {}'.format(data.airport,
                                                                                  data.flight,
                                                                                  data.date,
                                                                                  data.departure,
                                                                                  data.arrival))


    elif STATE == 5:
        vars_avia_types = 'Внутрирегиональный', 'Межрегиональный', 'Международный'
        companies = 'Аврора', 'Аэрофлот', 'Назад к выбору меню'
        vars_rules_traffic = 'Нормы багажа', 'Перевозка негабаритного багажа', \
                             'Перевозка домашних животных', 'Перевозка спорт инвентаря', 'Назад к выбору меню'

        if message.text == 'Назад к выбору меню':
            start_handler(message=message)
        elif message.text in vars_avia_types:
            custom_keyboard_in_commands(message=message, custom_keyboard=companies, text='Выберите авиакомпанию')
        elif message.text in companies:
            resize_custom_keyboard_in_commands(message=message, custom_keyboard=vars_rules_traffic,
                                               text='Выберите категорию')
        elif message.text == 'Перевозка домашних животных':
            requests_to_text(message=message, answer=''' 
                    Если вы решили взять в путешествие своего питомца, обязательно сообщите об 
                    этом авиакомпании не позднее, чем за 36 часов до вылета (диспетчеру при бронировании 
                    или покупке авиабилета), поскольку перевозка животных производится только с согласия 
                    авиакомпании и существуют ограничения по количеству и видам перевозимых животных.''')

    elif STATE == 6:
        if message.text == 'Назад к выбору меню':
            start_handler(message=message)

    elif STATE == 7:
        if message.text == 'Назад к выбору меню':
            start_handler(message=message)
        else:
            user_input_st_6 = message.text
            UserData.create(data=user_input_st_6,
                            is_relative=True)
            bot.send_message(message.chat.id, 'Ваша заявка принята, ожидайте звонка'
                                              '\nВведите /start для выхода в главное меню')

    elif STATE == 8:
        if message.text == 'Назад к выбору меню':
            start_handler(message=message)
        else:
            user_input_st_7 = message.text
            UserData.create(data=user_input_st_7,
                            is_relative=True)
            bot.send_message(message.chat.id, '\nВаша заявка принята, ожидайте звонка'
                                              'Введите /start для выхода в главное меню')

    elif STATE == 9:
        if message.text == 'Назад к выбору меню':
            start_handler(message=message)
        else:
            user_input_flight_ln = message.text
            UserData.create(data=user_input_flight_ln,
                            is_relative=True)
            cmnds = 'Оплатить', 'Операции', 'Назад к выбору меню'
            custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Вы авторизованы')
            bot.send_photo(message.from_user.id, photo=open('/Users/lucio/Desktop/avia.jpg', 'rb'))

    elif STATE == 10:
        if message.text == 'Назад к выбору меню':
            start_handler(message=message)
        else:
            user_input_st10 = message.text
            UserData.create(data=user_input_st10,
                            is_relative=True)
            if message.text == 'Отмена бронирования' or message.text == 'Обмен авиабилета' or message.text == 'Другое':
                requests_to_text(message=message, answer='Введите ваше имя и номер телефона.'
                                                         '\nНаш оператор свяжется с вами.')
            elif message.text == 'Доп. услуги':
                cmnds = 'Пересесть в бизнес-класс', 'Докупить багаж', 'Другое', 'Назад к выбору меню'
                custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Выберите желаемую услугу')

    elif STATE == 11:
        if message.text == 'Назад к выбору меню':
            start_handler(message=message)
        elif message.text:
            user_input_st10_buy = message.text
            UserData.create(data=user_input_st10_buy,
                            is_relative=True)
            bot.send_photo(message.from_user.id, photo=open('/Users/lucio/Desktop/avia.jpg', 'rb'))

            msg = bot.send_message(message.from_user.id, 'Выберите свободное место(пример: F16)')
            bot.register_next_step_handler(msg, command_pay_business)
    elif STATE == 12:
        if message.text == 'Назад к выбору меню':
            start_handler(message=message)
        else:
            user_input_st12 = message.text
            UserData.create(data=user_input_st12,
                            is_relative=True)
            commands = 'Да', 'Нет'
            resize_custom_keyboard_in_commands(message=message, custom_keyboard=commands,
                                               text='В стоимость вашей услуги включена только ручная кладь.'
                                                    ' Хотите докупить место для вещей?')
            if message.text == 'Да':
                PRICE_BUSINESS = types.LabeledPrice(label='АвиаБилет Бизнес', amount=122200)
                command_pay(message, text='Ваш счет к оплате',
                            title=MESSAGES['tm_title'], description='Докупить место для вещей',
                            prices=PRICE_BUSINESS, photo_url=None)
                stop_handler(message=message)
            else:
                start_buy_bagadge(message=message)

    steps = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
    if STATE in steps:
        if message.text == 'Назад к выбору типа':
            start_schedule(message=message)

        elif message.text == 'Назад к выбору даты':
            start_schedule(message=message)
    # add handler with date of user message


if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=0)

