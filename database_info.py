import mysql.connector
from mysql.connector import errorcode


config = {
    'host': 'poc.mysql.database.azure.com',
    'port': '3306',
    'user': '',
    'password': '',
    'database': 'poc-baza'
}

def create_database_connection():
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()   

    cursor.execute("INSERT INTO USERS (name, token, bot_username, chat_id) VALUES (%s, %s, %s, %s);", ("banana", "tokenik", "bocik", 1))
    print("Inserted", cursor.rowcount, "row(s) of data.")

    conn.commit()
    cursor.close()
    conn.close()
    print("Done.")

def get_database_information():
    user_information = {}

    user_information['token'] = '###'
    user_information['bot_username'] = '###'
    user_information['chat_id'] = '###'
    user_information['configuration_chat_id'] = '###'
    user_information['priority_emails'] = [
        '###',
        '###'
    ]
    user_information['user'] = {
        'username': '###',
        'password': '###',
        'imap_host': '###',
        'imap_port': '###'
    }

    user_information['account_sid'] = '###'
    user_information['auth_token'] = '###'
    user_information['receiver_number'] = '###'
    user_information['sender_number'] = '###'

    user_information['name'] = '###'
    user_information['password'] = '###'

    user_information['openai'] = '###'

    return user_information
