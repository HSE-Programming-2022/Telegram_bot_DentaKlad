import pymysql
from config import host, user, password, db_name, port


def all_rows():
    with connection.cursor() as cursor:
        select_all_rows = "SELECT * FROM Clients"
        cursor.execute(select_all_rows)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        connection.commit()


def add_comment(text, number):
    with connection.cursor() as cursor:
        cursor.execute("SELECT Id FROM Clients WHERE PhoneNumber = " + str(number))
        rows = cursor.fetchall()
        id = ''
        try:
            id = rows[0]['Id']
        except Exception:
            print('anon comment')
        add_new_comment = "INSERT INTO Comments (Message, Client_Id) VALUES ('" + str(text) + "', '" + str(id) + "')"
        cursor.execute(add_new_comment)
        connection.commit()


def add_row(name, phone):
    with connection.cursor() as cursor:
        add_new_row = "INSERT INTO Clients (Name, PhoneNumber) VALUES ('" + str(name) + "', '" + str(phone) + "')"
        cursor.execute(add_new_row)
        connection.commit()


def delete_row_by_id(id):
    with connection.cursor() as cursor:
        delete_row = "DELETE FROM Clients WHERE ID = " + str(id)
        cursor.execute(delete_row)
        connection.commit()


def delete_row_by_phone(phone):
    with connection.cursor() as cursor:
        delete_row = "DELETE FROM Clients WHERE PhoneNumber = " + str(phone)
        cursor.execute(delete_row)
        connection.commit()


try:
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print('connected successfully')
except Exception as ex:
    print('Failed')
    print(ex)
