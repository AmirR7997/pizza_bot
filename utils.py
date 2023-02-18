class MenuStack:

    def __init__(self, default_menu):
        self.elements = list()
        self.default_menu = default_menu

    def push(self, element):
        self.elements.append(element)

    def pop(self):
        if len(self.elements) == 0:
            return self.default_menu

        popped_element = self.elements[-1]
        del self.elements[-1]
        return popped_element

    def top(self):
        if len(self.elements) == 0:
            return self.default_menu
        return self.elements[-1]
    def __str__(self):
        return str(self.elements)


from constant import (get_address_sql,
                      get_phone_number_sql, set_integer_flag_sql, get_integer_flag_sql, update_user_filed_sql,
                      get_product_data_sql, get_product_id_from_user_sql, get_basket_from_user,
                      delete_product_from_basket, create_order_sql, get_order_id)
import sqlite3


def check_phone_number(chat_id):
    try:
        sql = get_phone_number_sql(chat_id)
        conn = sqlite3.connect("Pizza_db")
        cursor = conn.cursor()

        cursor.execute(sql)
        conn.commit()
        result = cursor.fetchone()
        if result is not None:
            return True
        return False
    except Exception as e:
        print("Database error")
        print(e)


def check_address(chat_id):
    try:
        sql = get_address_sql(chat_id)
        conn = sqlite3.connect("Pizza_db")
        cursor = conn.cursor()

        cursor.execute(sql)
        conn.commit()
        result = cursor.fetchone()
        if result is not None:
            return True
        return False
    except Exception as e:
        print("Database error")
        print(e)


def set_integer_flag(value, column_name, table_name, chat_id):
    sql = set_integer_flag_sql(value, column_name, table_name, chat_id)

    conn = sqlite3.connect("Pizza_db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()


def get_integer_flag(column_name, table_name, chat_id):
    sql = get_integer_flag_sql(column_name, table_name, chat_id)
    conn = sqlite3.connect("Pizza_db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    flag = cursor.fetchall()[0][0]

    return flag


def update_user_filed(chat_id, filed_name, value):
    sql = update_user_filed_sql(chat_id, filed_name, value)

    conn = sqlite3.connect("Pizza_db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

def get_product_data(product_name):
    sql = get_product_data_sql(product_name)

    conn = sqlite3.connect("Pizza_db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    data = cursor.fetchone()
    id_ = data[0]
    description = data[1]
    price = data[2]

    return description, price, id_

def start_getting_quantity(chat_id, product):
    set_integer_flag(1, "quantity_being_entered", "user", chat_id)
    _, __, id_ = get_product_data(product)
    update_user_filed(chat_id, "chosen_product", id_)

def get_product_from_user(chat_id):
    sql = get_product_id_from_user_sql(chat_id)

    conn = sqlite3.connect("Pizza_db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    product_id = cursor.fetchone()[0]
    return product_id

def insert_data_to_basket(chat_id, product_id, amount):
    sql = f"INSERT INTO basket (user_id, product_id, amount) VALUES ({chat_id},{product_id},{amount})"

    conn = sqlite3.connect("Pizza_db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()


def fetch_basket_data(chat_id):
    sql = get_basket_from_user(chat_id)
    conn = sqlite3.connect("Pizza_db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    basket_data = cursor.fetchall()
    return basket_data

def delete_item_from_basket(chat_id, product_name, amount):
    sql = delete_product_from_basket(chat_id,product_name,amount)
    conn = sqlite3.connect("Pizza_db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

def create_order(chat_id):
    sql = create_order_sql(chat_id)
    conn = sqlite3.connect("Pizza_db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()


def move_products_from_basket_to_order(chat_id):
    basket_data = get_basket_from_user(chat_id)
    create_order_id_sql = create_order_sql(chat_id)
    conn = sqlite3.connect("Pizza_db")
    cursor = conn.cursor()
    cursor.execute(create_order_id_sql)
    conn.commit()

    order_id_sql = get_order_id(chat_id)
    conn = sqlite3.connect("Pizza_db")
    cursor = conn.cursor()
    cursor.execute(order_id_sql)
    conn.commit()
    order_id = cursor.fetchone()[0]

    sql = "INSERT INTO order_product (order_id, product_id) VALUES (? ? ?)"
    order_products_pairs = []
    for _, amount, _, product_id in basket_data:
        order_products_pairs.append((order_id, product_id, amount))
    cursor.execute(sql, order_products_pairs)

if __name__ == '__main__':
    my_stack = MenuStack(9)
    my_stack.push(3)
    my_stack.push(5)
    my_stack.push(-1)
    print(my_stack)
    print(my_stack.elements)
    popped = my_stack.pop()
    print("Popped element:", popped)
    print(my_stack)