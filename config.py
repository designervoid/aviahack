TOKEN = '877450224:AAH8eOrZ0akUuN6er_LBoCerDzzHo-ZyUbA'

PAYMENTS_PROVIDER_TOKEN = '381764678:TEST:9316'  # @BotFather -> Bot Settings -> Payments
AVIA_IMAGE_URL = 'https://azimuth.aero/uploads/ckeditor/pictures/24/content_komponovka.jpg'

help_message = '''
Через этого бота можно забронировать билеты на самолет.
Отправьте команду /buy, чтобы перейти к покупке.
Узнать правила и положения можно воспользовавшись командой /terms.
'''

start_message = 'Привет! Это демонстрация работы платежей в Telegram!\n' + help_message

pre_buy_demo_alert = '''\
Так как сейчас я запущен в тестовом режиме, для оплаты нужно использовать карточку с номером `4242 4242 4242 4242`
Счёт для оплаты:
'''

terms = '''\
*Спасибо, что выбрали нашего бота. Мы надеемся, вам понравится!*
'''

tm_title = 'Авиационный билет'
tm_description = '''\
Эконом Класс
'''

AU_error = '''\
Попробуйте выбрать другой адрес!
'''

wrong_email = '''\
Нам кажется, что указанный имейл не действителен.
Попробуйте указать другой имейл
'''

successful_payment = '''
Ура! Платеж на сумму `{total_amount} {currency}` совершен успешно!
Купить ещё билет - /buy
'''


MESSAGES = {
    'start': start_message,
    'help': help_message,
    'pre_buy_demo_alert': pre_buy_demo_alert,
    'terms': terms,
    'tm_title': tm_title,
    'tm_description': tm_description,
    'AU_error': AU_error,
    'wrong_email': wrong_email,
    'successful_payment': successful_payment,
}




