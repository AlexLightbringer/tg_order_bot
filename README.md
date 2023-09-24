# Telegram Bot for Order Management

This is a Telegram bot for managing customer orders. The bot allows customers to place orders, view their order history, access sales information, and contact a manager.

## Features

- **Start Command**: The bot greets users and provides a set of options to choose from.

- **Make an Order**: Customers can place an order by selecting the "🛒 Make an order" option. The bot guides them through the order process and sends the order details to a manager.

- **Sales**: Customers can access sales information by selecting the "🏷️ Sales" option. The bot provides details about ongoing sales.

- **About Us**: Customers can learn more about your company by selecting the "📱 About us" option. The bot provides information about your delivery service, address, phone number, email, and website.

- **Contact a Manager**: Customers can contact a manager by selecting the "🕴️ Contact a manager" option. The bot provides the manager's Telegram username, phone number, and email for easy communication.

- **My Orders**: Customers can view their order history by selecting the "📦 My orders" option. The bot displays a list of their orders and allows them to cancel orders with a "Not confirmed" status.

- **Cancel Order**: Customers can cancel orders with a "Not confirmed" status by clicking the "Cancel this order" button in the order details.

## Getting Started

1. Clone this repository to your local machine.

2. Create a PostgreSQL database with the name "delivery" and configure the database connection settings in the `db.py` file.

3. Create a Telegram bot on [BotFather](https://core.telegram.org/bots#botfather) and obtain your API token.

4. Install the required Python packages by running:
 pip install -r requirements.txt

5. Update the `config.py` file with your Telegram bot API token:

```bot = telebot.TeleBot("YOUR_API_TOKEN_HERE")```

6. Run the main.py script to start the bot

## Usage

1. Start a chat with your bot on Telegram.

2. Use the provided commands and options to interact with the bot:

- Use the "🛒 Make an order" option to place an order.
- Access sales information with "🏷️ Sales."
- Learn about a company with "📱 About us."
- Contact a manager with "🕴️ Contact a manager."
- View order history with "📦 My orders" and cancel orders with a "Not confirmed" status.

Enjoy using your Telegram bot for order management! If you have any questions or need further assistance, feel free to reach out.
