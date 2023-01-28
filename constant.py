
def get_products_query():
    sql = "SELECT name from products"
    return sql

def create_new_user_query(id):

    sql = f"INSERT INTO user (id) VALUES ({id})"
    return sql

def get_phone_number_sql(chat_id):
    sql = f"""SELECT phone_number FROM user WHERE id = {chat_id}"""
    return sql


def get_address_sql(chat_id):
    sql = f"""SELECT location FROM user WHERE id = {chat_id}"""
    return sql