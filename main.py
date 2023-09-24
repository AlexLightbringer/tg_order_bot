import telebot
from telebot import types
from registration import RegistrationHandler
from orders import OrdersListHandler
from config import bot


# handle start command
@bot.message_handler(commands=["start"])
def start(message):
    # add client's buttons
    order = types.KeyboardButton("🛒 Make an order")
    on_sale = types.KeyboardButton("🏷️ Sales")
    company_contacts = types.KeyboardButton("📱 About us")
    contact_manager = types.KeyboardButton("🕴️ Contact a manager")
    user_orders = types.KeyboardButton("📦 My orders")

    # add a client's keyboard
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(order, on_sale, company_contacts, contact_manager, user_orders)
    bot.send_message(
        message.chat.id,
        "Hello, {0}! Select the option.".format(message.from_user.first_name),
        reply_markup=keyboard,
    )


# handle "Make an order" option
@bot.message_handler(func=lambda message: message.text == "🛒 Make an order")
def handle_make_order(message):
    registration_handler = RegistrationHandler(bot)
    registration_handler.make_order_handler(message)


# handle "Sales" option
@bot.message_handler(func=lambda message: message.text == "🏷️ Sales")
def on_sale(message):
    # store a text
    sales = """
    text
    text
    text
    """

    # if the message too long
    if len(sales) > 4096:
        for x in range(0, len(sales), 4096):
            bot.send_message(message.chat.id, sales[x : x + 4096])

    # if the message normal size
    else:
        bot.send_message(message.chat.id, sales)


# handle "About us" option
@bot.message_handler(func=lambda message: message.text == "📱 About us")
def about_us(message):
    # store info about company
    company_contacts = """
    Your delivery
    Address: 132, My Street, Kingston, New York 12401
    Телефон: +1 (555) 123-4567
    Электронная почта: info@bestdelivery.com
    Веб-сайт: www.bestdelivery.com 
    """
    # if the message too long
    if len(company_contacts) > 4096:
        for x in range(0, len(company_contacts), 4096):
            bot.send_message(message.chat.id, company_contacts[x : x + 4096])

    # if the message normal size
    else:
        bot.send_message(message.chat.id, company_contacts)


# handle "Contact a manager" option
@bot.message_handler(func=lambda message: message.text == "🕴️ Contact a manager")
def contact_manager(message):
    manager_username = "Leontain_space_and_time"
    manager_phone = "+1234567890"
    manager_email = "manager@example.com"

    manager_info = f"Contact our manager:\nTelegram: [Manager](https://t.me/{manager_username})\nPhone: {manager_phone}\nEmail: {manager_email}"

    bot.send_message(message.chat.id, manager_info, parse_mode="Markdown")


# handle "My orders" option
@bot.message_handler(func=lambda message: message.text == "📦 My orders")
def display_orders(message):
    orders_list_handler = OrdersListHandler(bot)
    orders_list_handler.get_orders(message)


# handle a back command
@bot.message_handler(func=lambda message: message.text == "🔙 Back")
def back(message):
    # add client's buttons
    order = types.KeyboardButton("🛒 Make an order")
    on_sale = types.KeyboardButton("🏷️ Sales")
    company_contacts = types.KeyboardButton("📱 About us")
    contact_manager = types.KeyboardButton("🕴️ Contact a manager")
    user_orders = types.KeyboardButton("📦 My orders")

    # add a client's keyboard
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(order, on_sale, company_contacts, contact_manager, user_orders)
    bot.send_message(
        message.chat.id,
        "Hello, {0}! Select the option.".format(message.from_user.first_name),
        reply_markup=keyboard,
    )


# start the bot
bot.polling(non_stop=True)
