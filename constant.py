def get_products_query():
    sql = "SELECT name from products"
    return sql


def create_new_user_query(id):
    sql = f"INSERT INTO user (id) VALUES ({id})"
    return sql


def get_phone_number_sql(chat_id):
    sql = f"""SELECT phone_number
              FROM user 
              WHERE id = {chat_id}"""
    return sql


def get_address_sql(chat_id):
    sql = f"""SELECT location
              FROM user
              WHERE id = {chat_id}"""
    return sql



def set_integer_flag_sql(value, column_name, table_name, chat_id):
    sql = f"UPDATE {table_name} SET {column_name} = {value} WHERE id = {chat_id}"
    return sql


def get_integer_flag_sql(column_name, table_name, chat_id):
    sql = f"SELECT {column_name} FROM {table_name} WHERE id = {chat_id}"
    return sql


def update_user_filed_sql(chat_id, filed_name, value):
    sql = f"UPDATE user SET {filed_name} = '{value}' WHERE id = {chat_id}"
    return sql

def get_product_data_sql(product_name):
    sql = f"SELECT id, description, price from products WHERE name = '{product_name}'"
    return sql

def get_product_id_from_user_sql(chat_id):
    sql = f"SELECT chosen_product FROM user WHERE id = {chat_id}"
    return sql

def get_basket_from_user(chat_id):
    sql = f"SELECT products.name, basket.amount, products.price, basket.id FROM basket JOIN products on basket.product_id = products.id WHERE user_id = {chat_id}"
    return sql

def get_basket_for_basket_item(chat_id, product_name, amount):

    sql = f"SELECT basket.id FROM basket JOIN products on basket.product_id = products.id WHERE user_id = {chat_id} AND products.name = '{product_name}' AND basket.amount = {amount}"
    return sql
def delete_product_from_basket(chat_id, product_name, amount):
    sub_sql = get_basket_for_basket_item(chat_id, product_name, amount)
    sql = f"DELETE FROM basket WHERE basket.user_id = {chat_id} AND basket.id in ({sub_sql})"

    return sql

def create_order_sql(chat_id):
    sql = f"INSERT INTO 'order' (user_id) VALUES ({chat_id});"
    return sql

def get_order_id(chat_id):
    sql = f"SELECT id from 'order' WHERE user_id = {chat_id};"
    return sql