

class YelpServer(object):
    def __init__(self):
        self.user = "user_356"
        self.password = "user_356"
        self.host = "192.168.2.208"
        self.database = "YELP_DB"

    def execute_query(self, query):
        try:
            # replace user and password with credentials for mysql shell user with YELP_DB full access
            # replace host with VM IP address (VM network setup as bridged adapter from virtualbox)
            cnx = mysql.connector.connect(user=self.user, password=self.password,
                                            host=self.host, database=self.database)
            cursor = cnx.cursor()
            cursor.execute(query)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cnx.close()

    def post_review(self, user_id, restaurant_id, stars, text):
        query = ""
        self.execute_query(query)

    def post_tip(self, user_id, restaurant_id, text):
        query = ""
        self.execute_query(query)

    def follow_user(self, user_id, following_user_id):
        query = ""
        self.execute_query(query)

    def follow_business(self, user_id, business_id):
        query = ""
        self.execute_query(query)

    def follow_category(self, user_id, category):
        query = ""
        self.execute_query(query)

    def get_latest_posts(self, user_id):
        query = ""
        self.execute_query(query)

    def react_to_post(self, post):
        query = ""
        self.execute_query(query)

    def get_post(self, user, date):
        query = ""
        self.execute_query(query)

    def get_all_categories(self):
        query = ""
        self.execute_query(query)

    def get_all_users(self):
        query = ""
        self.execute_query(query)

    def search_user(self, firstname, lastname):
        query = ""
        self.execute_query(query)
    