import mysql.connector
from mysql.connector import errorcode
import hashlib

config = {
    'host': 'poc.mysql.database.azure.com',
    'port': '3306',
    'user': '',
    'password': '',
    'database': 'poc-baza'
}

def connect_to_database(config):
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None

def hash_token(token):
    hashed_token = hashlib.sha256(token.encode()).hexdigest()
    return hashed_token

def insert_user(name, token, bot_username, chat_id):
    conn = connect_to_database(config)
    if conn:
        try:
            cursor = conn.cursor()
            hashed_token = hash_token(token)

            cursor.execute("INSERT INTO Users (name, token, bot_username, chat_id) VALUES (%s, %s, %s, %s);", (name, hashed_token, bot_username, chat_id))
            conn.commit()
            print("Inserted", cursor.rowcount, "row(s) of data.")

        except mysql.connector.Error as err:
            print("Error:", err)
            conn.rollback()

        finally:
            cursor.close()
            conn.close()
            print("Connection closed.")

def select_user(name, token):
    conn = connect_to_database(config)
    if conn:
        try:
            cursor = conn.cursor()
            hashed_token = hash_token(token)

            cursor.execute("SELECT * FROM Users WHERE name = %s AND token = %s LIMIT 1;", (name, hashed_token))
            result = cursor.fetchone()
            if result:
                print("User exists:", result)
            else:
                print("User does not exist.")

        except mysql.connector.Error as err:
            print("Error:", err)

        finally:
            cursor.close()
            conn.close()
            print("Connection closed.")

insert_user("Kate", "secret123", "kate12", 1)

name_input = input("Enter name: ")
token_input = input("Enter token: ")
select_user(name_input, token_input)