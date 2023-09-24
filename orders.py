import telebot
from telebot import types
from config import bot
from db import DatabaseHandler


class OrdersListHandler:
    def __init__(self, bot):
        self.bot = bot
        self.db_handler = DatabaseHandler(
            "delivery", "postgres", "postgres", "localhost", "5432"
        )
        self.db_handler.connect()

    def get_orders(self, message):
        # get the list of orders
        client_id = message.chat.id
        if client_id is not None:
            orders = self.db_handler.get_orders_for_client(client_id)

            if orders is not None and len(orders) > 0:
                for order in orders:
                    order_id = order[0]
                    order_detail = order[2]
                    order_status = order[3]

                    # display order details to the user
                    order_text = f"Order №{order_id}\nDetails: {order_detail}\nStatus: {order_status}"

                    # create an inline keyboard with the "Cancel this order" button
                    inline_keyboard = types.InlineKeyboardMarkup()
                    cancel_button = types.InlineKeyboardButton(
                        text="Cancel this order",
                        callback_data=f"cancel_order_{order_id}",
                    )
                    inline_keyboard.add(cancel_button)

                    # send the order message with the inline keyboard
                    order_message = self.bot.send_message(
                        message.chat.id, order_text, reply_markup=inline_keyboard
                    )

                # create a separate reply keyboard for the "Back" button
                back_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("🔙 Back")
                back_keyboard.add(back)

                # send the "Back" button separately as a reply keyboard
                self.bot.send_message(
                    message.chat.id, "You can go back:", reply_markup=back_keyboard
                )

            # handle the case where no orders were found
            else:
                back_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("🔙 Back")
                back_keyboard.add(back)
                self.bot.send_message(
                    message.chat.id, "You have no orders.", reply_markup=back_keyboard
                )

        # handle the case where the user's client ID is not found
        else:
            back_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("🔙 Back")
            back_keyboard.add(back)
            self.bot.send_message(
                message.chat.id, "Something went wrong...", reply_markup=back_keyboard
            )

    # delete an order after press the button
    def handle_callback(self, query):
        order_id_str = query.data.split("_")[2]
        # get order's status, because a client shouldn't delete confermed orders
        try:
            order_id = int(order_id_str)
            order_status = self.db_handler.get_order_status(order_id)
            if order_status == "Not confirmed":
                deleted = self.db_handler.delete_order(order_id)
                if deleted:
                    bot.send_message(
                        query.message.chat.id, f"Order {order_id} has been canceled."
                    )
                else:
                    bot.send_message(
                        query.message.chat.id, f"Failed to cancel order {order_id}."
                    )
            else:
                bot.send_message(
                    query.message.chat.id,
                    f"Order {order_id} cannot be canceled. Please contact a manager.",
                )

            self.get_orders(query.message)

        except ValueError:
            bot.send_message(query.message.chat.id, "Invalid order ID.")


orders_handler = OrdersListHandler(bot)


@bot.callback_query_handler(func=lambda query: query.data.startswith("cancel_order_"))
def handle_cancel_order(query):
    orders_handler.handle_callback(query)
