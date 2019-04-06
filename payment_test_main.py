import telebot
from telebot import types
from datetime import datetime
from db import AviaSchleduleArrival, AviaSchleduleDeparture, UserData
from config import TOKEN
from config import MESSAGES, PAYMENTS_PROVIDER_TOKEN, TIME_MACHINE_IMAGE_URL



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
    global STATE
    STATE = 4
    cmnds = 'Внутрирегиональный', 'Межрегиональный', 'Международный', 'Назад к выбору меню'
    custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Выберите тип рейса')

# START BOOKING
@bot.message_handler(regexp='Бронирование перевозки')
def start_booking(message):
    global STATE
    STATE = 5
    cmnds = 'На этой неделе', 'В следующем месяце', 'Назад к выбору меню'
    resize_custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Выберите промежуток')


@bot.message_handler(regexp='На этой неделе')
def start_booking_time_this_week(message):
    global STATE
    STATE = 6
    requests_to_text(message=message, answer='Введите ваше имя и номер')


''' 
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_DAY.value)
def user_entering_day(message):
    bot.send_message(message.chat.id, "Мы запомнили этот день. Теперь введите Ваше имя")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_DAY.value)
'''


@bot.message_handler(regexp='Операции с бронированием')
def start_oprtions_wth_booking(message):
    global STATE
    STATE = 7
    cmnds = 'Оплатить', 'Операции'
    custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Страница оплаты')


@bot.message_handler(commands=['terms'])
def command_terms(message):
    bot.send_message(message.chat.id,
                     'Инфо о авиа')

# PAYMENT
@bot.message_handler(commands=['buy'])
def command_pay(message):
    bot.send_message(message.chat.id,
                     "Real cards won't work with me, no money will be debited from your account."
                     " Use this test card number to pay for your Time Machine: `4242 4242 4242 4242`"
                     "\n\nThis is your demo invoice:", parse_mode='Markdown')
    bot.send_invoice(message.chat.id,
                     title=MESSAGES['tm_title'],
                     description=MESSAGES['tm_description'],
                     provider_token=PAYMENTS_PROVIDER_TOKEN,
                     currency='RUB',
                     photo_url=TIME_MACHINE_IMAGE_URL,
                     photo_height=512,  # !=0/None, иначе изображение не покажется
                     photo_width=512,
                     photo_size=512,
                     is_flexible=False,  # True если конечная цена зависит от способа доставки
                     prices=[PRICE],
                     start_parameter='time-machine-example',
                     invoice_payload='some-invoice-payload-for-our-internal-use'
                     )


@bot.shipping_query_handler(func=lambda query: True)
def shipping(query):
    print(query)
    bot.answer_shipping_query(query.id, ok=True,
                              error_message='Oh, seems like our Dog couriers are having a lunch right now. Try again later!')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(query):
    bot.answer_pre_checkout_query(query.id, ok=True,
                                  error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                " try to pay again in a few minutes, we need a small rest.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     'Hoooooray! Thanks for payment! We will proceed your order for `{} {}` as fast as possible! '
                     'Stay in touch.\n\nUse /buy again to get a Time Machine for your friend!'.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')


@bot.message_handler(regexp='Проверка наличия мест')
def start_avialability_check(message):
    requests_to_text(message=message, answer='проверка наличия мест')

# STATES WITH TICKETS
@bot.message_handler(regexp='Сегодня')
def start_today_check(message):
    global STATE
    STATE = 1
    cmnds = 'Прилет', 'Вылет', 'Назад к выбору типа'
    custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Выберите тип')


@bot.message_handler(regexp='Завтра')
def start_tomorrow_check(message):
    global STATE
    STATE = 2
    cmnds = 'Прилет', 'Вылет', 'Назад к выбору типа'
    custom_keyboard_in_commands(message=message, custom_keyboard=cmnds, text='Выберите тип')


@bot.message_handler(regexp='Своя дата')
def start_user_input_check(message):
    global STATE
    STATE = 3
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
    print(STATE)
    if STATE == 1:  # check today date
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
            for data in AviaSchleduleDeparture.select():
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

    elif STATE == 2:    # check tommorow date
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
            for data in AviaSchleduleDeparture.select():
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

    elif STATE == 4:
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
    # STATE 5, 6

    elif STATE == 6:
        user_input = message.text
        UserData.create(data=user_input,
                        is_relative=True)
        bot.send_message(message.chat.id, 'Ваша заявка принята, ожидайте звонка')

    elif STATE == 7:
        if message.text == 'Оплатить':
            pass

    steps = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    if STATE in steps:
        if message.text == 'Назад к выбору меню':
            start_handler(message=message)

        elif message.text == 'Назад к выбору типа':
            start_schedule(message=message)

        elif message.text == 'Назад к выбору даты':
            start_schedule(message=message)
    # add handler with date of user message


if __name__ == '__main__':
    bot.polling(none_stop=True)

