import mysql.connector
from mysql.connector import errorcode

try:
    cnx = mysql.connector.connect(user="root", password="user_356",
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