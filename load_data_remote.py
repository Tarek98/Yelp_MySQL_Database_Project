import mysql.connector
from mysql.connector import errorcode

try:
    # replace user and password with credentials for mysql shell user with YELP_DB full access
    # replace host with VM IP address (VM network setup as bridged adapter from virtualbox)
    cnx = mysql.connector.connect(user="user_356", password="user_356",
                                    host='192.168.2.208', database='YELP_DB')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()