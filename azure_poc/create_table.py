import mysql.connector
from mysql.connector import errorcode

# Obtain connection string information from the portal

config = {
    'host': 'poc.mysql.database.azure.com',
    'port': '3306',
    'user': '',
    'password': '',
    'database': 'poc-baza'
}

# Construct connection string

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

# # Drop previous table of same name if one exists
# cursor.execute("DROP TABLE IF EXISTS inventory;")
# print("Finished dropping table (if existed).")
#
# # Create table
# cursor.execute("CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
# print("Finished creating table.")

# Insert some data into table
cursor.execute("INSERT INTO USERS (name, token, bot_username, chat_id) VALUES (%s, %s, %s, %s);", ("banana", "tokenik", "bocik", 1))
print("Inserted", cursor.rowcount, "row(s) of data.")

# Cleanup
conn.commit()
cursor.close()
conn.close()
print("Done.")
