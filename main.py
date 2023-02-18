from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import sqlite3
from constant import get_products_query, create_new_user_query
from utils import MenuStack, check_phone_number, check_address, set_integer_flag, get_integer_flag, update_user_filed, \
    get_product_data, start_getting_quantity, get_product_from_user, insert_data_to_basket, fetch_basket_data, \
    delete_item_from_basket, create_order

TOKEN = '5901370716:AAHAdCqATJZ6WSQRUm4buzP-fivEBdkYLuU'

bot = TeleBot(TOKEN, parse_mode=None)


def main_menu_keyboard():
    """
    Эта функция создает первоначальное меню в нашем тг боте
    :return Обьект класса ReplyKeyboardMarkup
    """

    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    cart = KeyboardButton("Корзина🧺")
    menu = KeyboardButton("Меню🍔")
    settings = KeyboardButton("Настройки⚙️")
    delivery = KeyboardButton("Доставка🚚")
    rep = KeyboardButton("Отзывы и предложения📝")
    contacts = KeyboardButton("Контакты☎️")

    markup.add(cart)
    markup.add(menu, contacts)
    markup.add(settings, delivery, rep)

    return markup

stack = MenuStack(main_menu_keyboard())


def get_product_names() -> list:
    products = []

    try:
        conn = sqlite3.connect("Pizza_db")
        cursor = conn.cursor()
        sql = get_products_query()
        cursor.execute(sql)

        for product in cursor.fetchall():
            products.append(product[0])

    except Exception as e:
        print(e)

    return products

def menu_keyboard():
    '''это меню высвечивает товары в нашей базе данных
    :return Обьект класса ReplyKeyboardMarkup'''

    products = get_product_names()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    row = []
    for product in products:
        button = KeyboardButton(product)
        row.append(button)
        if len(row) == 3:
            keyboard.add(*row)
            row = []


    if row:
        keyboard.add(row[0])
    back_button = KeyboardButton("Назад🔙")
    keyboard.add(back_button)

    return keyboard

@bot.message_handler(func=lambda message: message.text == "Введите номер телефона")
def update_phone_number(message):
    chat_id = message.chat.id
    if not check_phone_number(chat_id):
        set_integer_flag(1, 'phone_being_entered', 'user', chat_id)
        bot.send_message(chat_id, "Введите номер телефона(должен содержать только цифры): ")

@bot.message_handler(func=lambda message: message.text == "Введите ваш адресс")
def update_address_number(message):
    chat_id = message.chat.id
    if not check_address(chat_id):
        set_integer_flag(1, 'address_being_entered', 'user', chat_id)
        bot.send_message(chat_id, "Введите ваш адресс: ")

@bot.message_handler(commands=["start"])
def start_handler(message):
    chat_id = message.chat.id

    create_user(chat_id)

    reply = f"Welcome to the hell {message.from_user.first_name} "
    bot.reply_to(message, reply, reply_markup=get_user_details_keyboard(chat_id))
    print(f'Name_of_user - {message.from_user.first_name}')
    print(f'Username_of_user - @{message.from_user.username}')
    print(f'ID_user - {message.from_user.id}')


def check_phone_if_yes_update(chat_id, message):
    if get_integer_flag(column_name='phone_being_entered',
                        table_name='user',
                        chat_id=chat_id) == 1:
        if message.text.isnumeric():
            update_user_filed(chat_id, 'phone_number', int(message.text))
            set_integer_flag(0, 'phone_being_entered', 'user', chat_id)
            bot.send_message(chat_id, "Номер телефона сохранён.", reply_markup=get_user_details_keyboard(chat_id))
        else:
            bot.send_message(chat_id, "Номер телефона должен содержать только цифры!")


def check_address_if_yes_update(chat_id, message):
    if get_integer_flag(column_name='address_being_entered',
                        table_name='user',
                        chat_id=chat_id) == 1:

        update_user_filed(chat_id, 'location', message.text)
        set_integer_flag(0, 'address_being_entered', 'user', chat_id)
        bot.send_message(chat_id, "Адрес сохранён.", reply_markup=get_user_details_keyboard(chat_id))

def get_user_details_keyboard(chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    phone_exist = False
    address_exist = False
    if not check_phone_number(chat_id):
        get_phone_button = KeyboardButton("Введите номер телефона ")
        markup.add(get_phone_button)
    else:
        phone_exist = True

    if not check_address(chat_id):
        get_address_button = KeyboardButton("Введите ваш адресс")
        markup.add(get_address_button)
    else:
        address_exist = True
    if phone_exist and address_exist:
        markup = main_menu_keyboard()


    return  markup

def create_user(chat_id):
    try:
        conn = sqlite3.connect('Pizza_db')
        cursor = conn.cursor()
        sql = create_new_user_query(chat_id)
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)




@bot.message_handler(func=lambda message: message.text == "Меню🍔")
def menu_handler(message):
    reply = "Выберите пиццу"
    bot.reply_to(message, reply, reply_markup=menu_keyboard())
    stack.push(menu_keyboard())


def choose_amount_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    row1 = [KeyboardButton("1"),KeyboardButton("2"),KeyboardButton("3")]
    row2 = [KeyboardButton("4"),KeyboardButton("5"),KeyboardButton("6")]
    row3 = [KeyboardButton("7"),KeyboardButton("8"),KeyboardButton("9")]
    row4 = KeyboardButton("Назад⬅️")

    keyboard.add(*row1)
    keyboard.add(*row2)
    keyboard.add(*row3)
    keyboard.add(row4)
    return keyboard


@bot.message_handler(func=lambda message: message.text in get_product_names())
def product_handler(message):
    product_name = message.text
    product_description, product_price, id_ = get_product_data(product_name)
    reply_message = f"*Наименование блюда:*{product_name}\n"
    reply_message += f"*Описание:*{product_description}\n"
    reply_message += f"*Цена за одну пиццу:*{product_price} сум"

    start_getting_quantity(message.chat.id, product_name)

    stack.push(choose_amount_keyboard())
    bot.send_message(message.chat.id, reply_message, parse_mode='MARKDOWN', reply_markup=choose_amount_keyboard())

@bot.message_handler(func=lambda message: message.text == "Назад⬅️")
def back_handler(message):
    stack.pop()
    menu_to_go_back = stack.top()
    bot.send_message(message.chat.id, "Прошлое меню: ", reply_markup=menu_to_go_back)
    set_integer_flag(0, "quantity_being_entered", "user", message.chat.id)

def check_for_quantity(chat_id, message):
    is_quantity = get_integer_flag("quantity_being_entered", "user", chat_id)
    if is_quantity == 1:
        if message.text.isnumeric() and int(message.text) > 0:
            product_id = get_product_from_user(chat_id)
            amount = int(message.text)
            insert_data_to_basket(chat_id, product_id, amount)
            bot.send_message(chat_id, "Добавлено в корзину!")
            stack.pop()
            keyboard = stack.top()
            bot.send_message(chat_id, "Хотите что то еще?", reply_markup=keyboard)
            set_integer_flag(0, "quantity_being_entered", "user", chat_id)
        else:
            bot.send_message(chat_id, "Количество может быть только положительным числовым значением.")


def basket_keyboard(basket_data):

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    for name, amount, price, id_ in basket_data:
        button = KeyboardButton(f"{name} - {amount} ❌")
        keyboard.add(button)

    back_button = KeyboardButton("Назад⬅️")
    order = KeyboardButton("Заказать")
    keyboard.add(back_button, order)

    return keyboard



@bot.message_handler(func=lambda message: message.text == 'Корзина🧺')
def basket_handler(message):
    basket_data = fetch_basket_data(chat_id=message.chat.id)

    if len(basket_data) == 0:
        bot.send_message(message.chat.id, "Корзина пуста")
        return

    reply_message = create_basket_data_message(basket_data)
    stack.push(basket_keyboard(basket_data))
    bot.send_message(message.chat.id, reply_message, parse_mode='MARKDOWN', reply_markup=basket_keyboard(basket_data))


def create_basket_data_message(basket_data):
    reply_message = ""
    total_price = 0
    for name, amount, price, _ in basket_data:
        reply_message += f"*{name}* - {amount} штук по {price} сум\n"
        total_price += price * amount
    reply_message += f"Общая сумма = *{total_price}*"
    return reply_message


@bot.message_handler(func=lambda message: message.text in [f"{name} - {amount} ❌" for name, amount, price, _ in fetch_basket_data(message.chat.id)])
def delete_product_handler(message):
    products = [(name, amount) for name, amount, _, _ in fetch_basket_data(message.chat.id) if f"{name} - {amount} ❌" == message.text]
    name, amount = products[0]
    delete_item_from_basket(message.chat.id, name, amount)

    basket_data = fetch_basket_data(message.chat.id)
    if len(basket_data) == 0:
        bot.send_message(message.chat.id, "Корзина пуста!", reply_markup=stack.top())
        return
    bot.send_message(message.chat.id, "Продукт удалён из корзины!", reply_markup=basket_keyboard(basket_data))
    reply_message = create_basket_data_message(basket_data)
    bot.send_message(message.chat.id, reply_message, parse_mode='MARKDOWN')

def order_keyboard():
     keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

     share_contact_button = KeyboardButton("Поделитесь номером телефона", request_contact=True)

     share_location_button = KeyboardButton("Скиньте локацию", request_location=True)

     back_button = KeyboardButton("Назад⬅️")
     keyboard.add(share_location_button)
     keyboard.add(share_contact_button)
     keyboard.add(back_button)

     return keyboard
@bot.message_handler(func=lambda message: message.text == "Заказать")
def order_message_handler(message):
    stack.push(order_keyboard())
    bot.send_message(message.chat.id, "Введите локацию и номер телефона: ", reply_markup=order_keyboard())


def check_for_order_being_entered(message):
    order_flag = get_integer_flag("order_being_made", "user", message.chat.id)
    if order_flag == 0:
        if message.content_type == "contact":
            phone_number = message.contact.phone_number
            phone_number = phone_number[1:]
            update_user_filed(message.chat.id, "phone_number", phone_number)
        if message.content_type == "location":
            location = message.location
            location = location.latitude, location.longitude
            update_user_filed(message.chat.id, "location", str(location))
            set_integer_flag(0, "order_being_made", "user", message.chat.id)
            create_order(message.chat.id)
            #clear_basket(message.chat.id)
            bot.send_message(message.chat.id, "Ваш заказ принят")

@bot.message_handler(content_types=['text' , 'contact' , 'location'])
def message_handler(message):

    chat_id = message.chat.id
    create_user(chat_id)
    check_phone_if_yes_update(chat_id, message)
    check_address_if_yes_update(chat_id, message)

    check_for_quantity(chat_id, message)
    check_for_order_being_entered(message)

    if message.text == "Меню🍔":
        bot.reply_to(message, 'Выбери пиццу:🍕', reply_markup=menu_keyboard())
    if message.text == "Настройки⚙️":
        bot.reply_to(message, '-Пока что это:💩-', reply_markup=back_keyboard())
    """if message.text == "Корзина🧺":
        bot.reply_to(message, '-Пока что это:💩-', reply_markup=back_keyboard())"""
    if message.text == "Доставка🚚":
        bot.reply_to(message,
                     'Если мы не успеем доставить заказ в течении 60 минут, то мы отправим вам промокод на бесплатную пиццу🎁\n\n'
                     '- Доставка бесплатная✅\n'
                     '- Доставим при заказе от 50.000 sum💴\n'
                     'P.S скопированно с тг бота додо пиццы')
    if message.text == "Отзывы и предложения📝":
        bot.reply_to(message, ':Дорогой клиент\n'
                              'Спасибо, что выбираете нас\n'
                              'Оцените работу нашей команды от 1 до 5', reply_markup=feedback_keyboard())

    if message.text == 'Назад🔙':
        bot.reply_to(message, f'Добро пожаловать<b>{message.from_user.first_name}💛</b>!\n'
                                f'Что желаете заказать?', parse_mode='html', reply_markup=main_menu_keyboard())

    if message.text == '😊 Мне все понравилось, 5 ❤️':
        bot.reply_to(message, 'Мы рады, что вы выбираете нас, надеемся на наше дальнейшее сотрудничество🤗\n ВашDodoPizza ❤️',
                    reply_markup=main_menu_keyboard())

    if message.text == '☺️Нормально, 4 ⭐️⭐️⭐️⭐️':
        bot.reply_to(message, 'Мы рады, что вам понравилось 😊. Что мы можем сделать, чтобы улучшить наш сервис?🤔',
                    reply_markup=back_keyboard())

    if message.text == 'Назад⬅️':
        bot.reply_to(message, 'Что желаете заказать?🍔', reply_markup=main_menu_keyboard())
    if message.text == '😐 Удовлетворительно, 3 ⭐️⭐️⭐️':
        bot.reply_to(message, 'Мы сожалеем, что нам не удалось оправдать ваших ожиданий.\n'
                              'Помогите нам стать лучше, оставьте свой комментарий или предложение для улучшения качества обслуживания  👇🏻.\n'
                              'Мы будем работать над вашими предложениями, чтобы стать лучше  🙏🏻', reply_markup=back_keyboard())

    if message.text == "☹️Мне не зашло, 2 ⭐️⭐️":
        bot.reply_to(message, 'Мы сожалеем, что разочаровали вас.\n'
                              'Помогите нам стать лучше, оставьте свой комментарий или предложение для улучшения качества обслуживания 👇🏻.\n'
                              'Мы будем работать над вашими предложениями, чтобы стать лучше 🙏🏻', reply_markup=back_keyboard())
    if message.text == 'Контакты☎️':
        bot.reply_to(message, '- Номер телефона: +998(97)157-79-97\n- Звонок бесплатный✅', reply_markup=main_menu_keyboard())

def menu_pizza_keyboard():
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    button1 = KeyboardButton('Пеперони')
    button2 = KeyboardButton('Маргарита')
    button3 = KeyboardButton('Гавайская')
    button4 = KeyboardButton('Комбо')
    button5 = KeyboardButton('четыре сыра')
    button6 = KeyboardButton('Цыпленок ранч')
    button7 = KeyboardButton('🔙')

    markup.add(button1,button2,button3)
    markup.add(button4,button5,button6)
    markup.add(button7)


    return markup

def feedback_keyboard():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    button1 = KeyboardButton('😊 Мне все понравилось, 5 ❤️')
    button2 = KeyboardButton('☺️Нормально, 4 ⭐️⭐️⭐️⭐️')
    button3 = KeyboardButton('😐 Удовлетворительно, 3 ⭐️⭐️⭐️')
    button4 = KeyboardButton('☹️Мне не зашло, 2 ⭐️⭐️')

    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    markup.add(button4)


    return markup



def back_keyboard():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    button = KeyboardButton('Назад⬅️')
    markup.add(button)

    return markup



'''WEBHOOK_HOST = '<ip/host where the bot is running>'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % TOKEN

try:
    # Python 2
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    # Python 3
    from http.server import BaseHTTPRequestHandler, HTTPServer


# WebhookHandler, process webhook calls
class WebhookHandler(BaseHTTPRequestHandler):
    server_version = "WebhookHandler/1.0"

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == WEBHOOK_URL_PATH and \
           'content-type' in self.headers and \
           'content-length' in self.headers and \
           self.headers['content-type'] == 'application/json':
            json_string = self.rfile.read(int(self.headers['content-length']))

            self.send_response(200)
            self.end_headers()

            update = Update.de_json(json_string)
            bot.process_new_messages([update.message])
        else:
            self.send_error(403)
            self.end_headers()


# Start server
httpd = HTTPServer((WEBHOOK_LISTEN, WEBHOOK_PORT),
                   WebhookHandler)

httpd.socket = ssl.wrap_socket(httpd.socket,
                               certfile=WEBHOOK_SSL_CERT,
                               keyfile=WEBHOOK_SSL_PRIV,
                               server_side=True)

httpd.serve_forever()'''
bot.infinity_polling()






















