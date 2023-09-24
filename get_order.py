import telebot
from telebot import types
from config import bot
import random
from db import DatabaseHandler

db_handler = DatabaseHandler("delivery", "postgres", "postgres", "localhost", "5432")
db_handler.connect()


# receiving an order
@bot.callback_query_handler(func=lambda call: call.data == "make_order")
def make_order(call):
    # add a button for back to the main menu
    back = types.KeyboardButton("🔙 Back")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(back)
    bot.send_message(
        call.message.chat.id,
        "Please type what you want to order!",
        reply_markup=keyboard,
    )
    bot.register_next_step_handler(call.message, get_order)


# generate a new order ID
def generate_unique_order_id():
    while True:
        new_id = random.randint(100000, 999999)
        if not db_handler.check_order_id_exist(new_id):
            return new_id


def get_order(message):
    # get order
    order = message.text
    # get client's id
    client_id = message.chat.id
    # generate the order's id
    order_id = generate_unique_order_id()
    # set the order's status
    status = "Not confirmed"
    # pass all info to the db
    db_handler.insert_order_data(order_id, client_id, order, status)

    # send the order's info to a manager
    manager_chat_id = "901147319"
    manager_message = f'New Order:\nOrder ID: {order_id}\nClient ID: {client_id}\nOrder: {order}\nStatus: {status}'
    bot.send_message(manager_chat_id, manager_message)

    # add a button for back to the main menu
    back = types.KeyboardButton("🔙 Back")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(back)

    bot.send_message(
        message.chat.id,
        "Thank you! Our manager will contact you!",
        reply_markup=keyboard,
    )
