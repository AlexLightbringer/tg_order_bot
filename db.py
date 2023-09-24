import psycopg2


class DatabaseHandler:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
        return self.conn

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def table_exists(self, table_name):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')"
        )
        table_exists = cursor.fetchone()[0]
        cursor.close()
        return table_exists

    def create_table(self, table_name, create_table_query):
        conn = self.connect()
        cursor = conn.cursor()

        if not self.table_exists(table_name):
            cursor.execute(create_table_query)
            conn.commit()
            print(f"Table '{table_name}' has been created.")
        else:
            print(f"Table '{table_name}' already exists.")

        cursor.close()

    def check_client_exist(self, phone):
        query = "SELECT id FROM clients WHERE phone = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (phone,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def check_client_id_exist(self, client_id):
        query = "SELECT id FROM clients WHERE id = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (client_id,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def insert_client_data(self, client_id, client_name, phone_number):
        query = "INSERT INTO clients (id, client_name, phone) VALUES (%s, %s, %s)"
        cursor = self.conn.cursor()
        cursor.execute(query, (client_id, client_name, phone_number))
        self.conn.commit()
        cursor.close()

    def check_order_id_exist(self, order_id):
        query = "SELECT id FROM orders WHERE id = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def insert_order_data(self, order_id, client_id, order_detail, order_status):
        query = "INSERT INTO orders (id, client_id, order_detail, status) VALUES (%s, %s, %s, %s)"
        cursor = self.conn.cursor()
        cursor.execute(query, (order_id, client_id, order_detail, order_status))
        self.conn.commit()
        cursor.close

    def get_orders_for_client(self, client_id):
        query = "SELECT * FROM orders WHERE client_id = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (client_id,))
        orders = cursor.fetchall()
        cursor.close
        return orders

    def get_order_status(self, order_id):
        query = "SELECT status FROM orders WHERE id = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def delete_order(self, order_id):
        try:
            delete_query = "DELETE FROM orders WHERE id = %s"
            cursor = self.conn.cursor()
            cursor.execute(delete_query, (order_id,))
            self.conn.commit()
            cursor.close()
            print(f"Order {order_id} deleted successfully")
            return True

        except Exception as e:
            self.conn.rollback()
            print(f"Error deleting order: {str(e)}")
            return False


dbname = "delivery"
user = "postgres"
password = "postgres"
host = "localhost"
port = "5432"

db_handler = DatabaseHandler(dbname, user, password, host, port)

# create the 'clients' table
create_users_table_query = """
    CREATE TABLE clients (
        id BIGSERIAL PRIMARY KEY,
        "client_name" VARCHAR(64),
        phone VARCHAR(50)
    )
"""

db_handler.create_table("clients", create_users_table_query)

# create the 'orders' table
create_orders_table_query = """
    CREATE TABLE orders (
        id BIGSERIAL PRIMARY KEY,
        client_id BIGINT REFERENCES clients(id),
        "order_detail" VARCHAR(500),
        "status" VARCHAR(50)
    )
"""

db_handler.create_table("orders", create_orders_table_query)
