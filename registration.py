import telebot
from telebot import types
from db import DatabaseHandler
from get_order import make_order


class RegistrationHandler:
    def __init__(self, bot):
        self.bot = bot
        self.db_handler = DatabaseHandler(
            "delivery", "postgres", "postgres", "localhost", "5432"
        )
        self.db_handler.connect()

    def make_order_handler(self, message):
        # add a button for share the contact
        send_number = types.KeyboardButton(
            text="📲 Share my number", request_contact=True
        )
        # add a button for back to the main menu
        back = types.KeyboardButton("🔙 Back")
        # add keyboard for share contact
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(send_number, back)

        self.bot.send_message(
            message.chat.id, "Please sign up to continue", reply_markup=keyboard
        )
        self.bot.register_next_step_handler(message, self.get_phone)

    # get a client's phone
    def get_phone(self, message):
        # handle the case where the user did share their contact
        if message.contact is not None:
            # store the client's number
            phone = message.contact.phone_number

            # check if the client exists in the database
            if self.db_handler.check_client_exist(phone):
                # client already exists in the database, proceed to order
                keyboard = types.InlineKeyboardMarkup()
                start_shopping = types.InlineKeyboardButton(
                    text="🧺 Start shopping", callback_data="make_order"
                )
                keyboard.add(start_shopping)
                self.bot.send_message(
                    message.chat.id,
                    "We are glad to see you again! Ready to take your order!",
                    reply_markup=keyboard,
                )
            # client doesn't exist, store the phone number
            else:
                # store the phone number in the class instance
                self.phone = phone
                # ask for the client's name
                self.ask_for_name(message)

        # handle the case where the user didn't share their contact
        else:
            # add a button for back to the main menu
            back = types.KeyboardButton("🔙 Back")
            self.bot.send_message(message.chat.id, "❌ Couldn't get your number")

    # ask for client's name
    def ask_for_name(self, message):
        self.bot.send_message(message.chat.id, "Please type your name")
        self.bot.register_next_step_handler(message, self.get_name)

    # get a client's name
    def get_name(self, message):
        # store the client's name
        name = message.text
        # store both phone and name in the database
        self.store_client_data(message, name, self.phone)

        # add the button for redirect to the next step
        keyboard = types.InlineKeyboardMarkup()
        start_shopping = types.InlineKeyboardButton(
            text="🧺 Start shopping", callback_data="make_order"
        )
        keyboard.add(start_shopping)

        self.bot.send_message(
            message.chat.id,
            "Registration is complete! You can start shopping!",
            reply_markup=keyboard,
        )

    def store_client_data(self, message, name, phone):
        client_id = message.chat.id
        self.db_handler.insert_client_data(client_id, name, phone)
