class MenuStack():

    def __init__(self,default_menu):
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

    def __str__(self):
        return self.elements

from constant import (get_address_sql, get_phone_number_sql)
import sqlite3
def check_phone_number(chat_id):
    try:
        sql = get_phone_number_sql(chat_id)
        conn = sqlite3.connect("Pizza_db")
        cursor = conn.cursor()

        cursor.execute(sql)
        if cursor.rowcount < 1:
            return False
        return True
    except Exception as e:
        print("Database error")
        print(e)

def check_address(chat_id):
    try:
        sql = get_address_sql(chat_id)
        conn = sqlite3.connect("Pizza_db")
        cursor = conn.cursor()

        cursor.execute(sql)
        if cursor.rowcount < 1:
            return False
        return True
    except Exception as e:
        print("Database error")
        print(e)

if __name__ == '__main__':
    my_stack = MenuStack()
    my_stack.push(3)

    my_stack.push(5)
    my_stack.push(-1)
    print(my_stack.elements)
    popped = my_stack.pop()
    print("Popped element:", popped)
    print(my_stack.elements)