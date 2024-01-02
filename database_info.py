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
        print("LOGGER - INFO - Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("LOGGER - INFO - Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("LOGGER - INFO - Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

    conn.commit()
    cursor.close()
    conn.close()
    print("LOGGER - INFO - Data base action is DONE.")


def get_database_information():
    user_information = {}

    user_id = 1

    try:
        conn = mysql.connector.connect(**config)
        print("LOGGER - INFO - Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("LOGGER - INFO - Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("LOGGER - INFO - Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

    query = "SELECT name, token, bot_username, chat_id, configuration_chat_id, password, openai FROM users WHERE id = %s;"
    cursor.execute(query, (user_id,))
    user_row = cursor.fetchone()

    if user_row:
        user_information['name'] = user_row[0]
        user_information['token'] = user_row[1]
        user_information['bot_username'] = user_row[2]
        user_information['chat_id'] = user_row[3]
        user_information['configuration_chat_id'] = user_row[4]
        user_information['password'] = user_row[5]
        user_information['openai'] = user_row[6]

    # Fetch data from the 'high_priority_mail' table
    query = "SELECT high_priority_mail FROM high_priority_mail WHERE user_id = %s;"
    cursor.execute(query, (user_id,))
    priority_emails_rows = cursor.fetchall()
    user_information['priority_emails'] = [row[0] for row in priority_emails_rows]

    # Fetch data from the 'mail' table
    query = "SELECT username, password, imap_host, imap_port FROM mail WHERE user_id = %s;"
    cursor.execute(query, (user_id,))
    mail_row = cursor.fetchone()

    if mail_row:
        user_information['user'] = {
            'username': mail_row[0],
            'password': mail_row[1],
            'imap_host': mail_row[2],
            'imap_port': mail_row[3]
        }

    # Fetch data from the 'twilio' table
    query = "SELECT account_sid, auth_token, receiver_number, sender_number FROM twilio WHERE user_id = %s;"
    cursor.execute(query, (user_id,))
    twilio_row = cursor.fetchone()

    if twilio_row:
        user_information['account_sid'] = twilio_row[0]
        user_information['auth_token'] = twilio_row[1]
        user_information['receiver_number'] = twilio_row[2]
        user_information['sender_number'] = twilio_row[3]

    conn.commit()
    cursor.close()
    conn.close()

    return user_information


def add_priority_mail(mail):
    user_id = 1

    try:
        conn = mysql.connector.connect(**config)
        print("LOGGER - INFO - Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("LOGGER - INFO - Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("LOGGER - INFO - Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

    query = "INSERT INTO high_priority_mail (user_id, high_priority_mail) VALUES (%s, %s);"
    cursor.execute(query, (user_id, mail,))
    conn.commit()
    cursor.close()
    conn.close()

    return 0


def delete_priority_mail(mail):
    user_id = 1

    try:
        conn = mysql.connector.connect(**config)
        print("LOGGER - INFO - Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("LOGGER - INFO - Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("LOGGER - INFO - Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

    query = "DELETE FROM high_priority_mail WHERE user_id = %s AND high_priority_mail = %s;"
    cursor.execute(query, (user_id, mail,))
    conn.commit()
    cursor.close()
    conn.close()

    return 0
