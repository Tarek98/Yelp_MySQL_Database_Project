import datetime
import mysql.connector
from mysql.connector import errorcode

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
            res = [x for x in cursor]
            cnx.commit()
            cursor.close()
            
            return res
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cnx.close()

    # In all API functions below, we return -n for an error in the nth argument passed
    #   to the function, return 0 for success, and an error message is thrown by the 
    #   execute_query() helper above if there is a database exception.

    def post_review(self, user_id, business_id, stars, text):
        # validate that user and business exist
        q1 = self.execute_query(\
            "select count(*) from User where user_id = '{}'".format(user_id))
        if q1[0][0] == 0:
            return -1
        q2 = self.execute_query(\
            "select count(*) from Business where business_id = '{}'".format(business_id))
        if q2[0][0] == 0:
            return -2

        today_date = datetime.date.today().isoformat()
        self.execute_query("insert into Review (user_id, business_id, stars, date, text)" +\
            "values ('{}', '{}', '{}', '{}', '{}')".format(\
            user_id, business_id, stars, today_date, text))

        return 0

    def post_tip(self, user_id, business_id, text):
        # validate that user and business exist
        q1 = self.execute_query(\
            "select count(*) from User where user_id = '{}'".format(user_id))
        if q1[0][0] == 0:
            return -1
        q2 = self.execute_query(\
            "select count(*) from Business where business_id = '{}'".format(business_id))
        if q2[0][0] == 0:
            return -2

        today_date = datetime.date.today().isoformat()
        self.execute_query("insert into Tip (user_id, business_id, date, text)" +\
            "values ('{}', '{}', '{}', '{}')".format(\
            user_id, business_id, today_date, text))

        return 0

    def follow_user(self, user_id, following_user_id):
        # validate that both users exists
        q1 = self.execute_query(\
            "select count(*) from User where user_id = '{}'".format(user_id))
        if q1[0][0] == 0:
            return -1
        q2 = self.execute_query(\
            "select count(*) from User where user_id = '{}'".format(following_user_id))
        if q2[0][0] == 0:
            return -2

        self.execute_query("insert into UserFollowers (user_id, follower_id)" +\
            "values ('{}', '{}')".format(following_user_id, user_id))

        return 0

    def follow_business(self, user_id, business_id):
        # validate that user and business exist
        q1 = self.execute_query(\
            "select count(*) from User where user_id = '{}'".format(user_id))
        if q1[0][0] == 0:
            return -1
        q2 = self.execute_query(\
            "select count(*) from Business where business_id = '{}'".format(business_id))
        if q2[0][0] == 0:
            return -2

        self.execute_query("insert into BusinessFollowers (business_id, user_id)" +\
            "values ('{}', '{}')".format(user_id, business_id))

        return 0

    def follow_category(self, user_id, category):
         # validate that user and category exist
        q1 = self.execute_query(\
            "select count(*) from User where user_id = '{}'".format(user_id))
        if q1[0][0] == 0:
            return -1
        q2 = self.execute_query(\
            "select count(*) from BusinessCategories where category = '{}'".format(category))
        if q2[0][0] == 0:
            return -2

        self.execute_query("insert into CategoryFollowers (category, user_id)" +\
            "values ('{}', '{}')".format(category, user_id))

        return 0

    def get_latest_posts(self, user_id):
        ## validate that current user exists (should be moved to query at client login!)
        q1 = self.execute_query(\
            "select count(*) from User where user_id = '{}'".format(user_id))
        if q1[0][0] == 0:
            return -1

        # determine when user was last online (when they last read from all topics)
        last_online = self.execute_query(\
            "select last_online from User where user_id = '{}'".format(user_id))
        last_online = last_online[0][0]
        # find all users user follows
        users_followed = self.execute_query(\
            "select user_id from UserFollowers where follower_id = '{}'".format(user_id))
        if len(users_followed) == 
        users_followed = tuple(str(x[0]) for x in users_followed)\
            if users_followed else "('')"

        [[('tarek',)],[('lefteris',)]]
        x = ('tarek', 'lefteris')
        "select from dssd where user_id in ('tarek', 'left')"

        # find all businesses user follows or within categories user is interested in
        categories_followed = self.execute_query(\
            "select category from CategoryFollowers where user_id = '{}'".format(user_id))
        businesses_followed = self.execute_query(\
            "select business_id from BusinessFollowers where user_id = '{}'".format(user_id))
        businesses_interested = self.execute_query(\
            "select distinct business_id from Business where business_id in"
            + " (select * from CategoryFollowers where user_id = '{0}') union (select business_id from BusinessFollowers where user_id = '{0}')".format(user_id))
        
        # find all businesses corresponding with categories the user follows

        
        
        # find latests post IDs (tips and reviews) from all followed topics/users since last read
        
        businesses_followed = tuple(str(x[0]) for x in businesses_followed)\
            if businesses_followed else "('')"
        categories_followed = tuple(str(x[0]) for x in categories_followed)\
            if len(categories_followed) > 1 else "('')"

            user_posts = self.execute_query(\
            "select review_id from Review where user_id in {} and date > '{}'".format(\
            users_followed, last_online))
        if businesses_followed:
            businesses_followed = tuple(str(x[0]) for x in businesses_followed)
        if categories_followed:
            categories_followed = tuple(str(x[0]) for x in categories_followed)

        ## find all posts (tips and reviews) from topics followed since last read
        

        # return 0

    def react_to_review(self, user_id, review_id, reaction):
        ## validate that current user exists (should be moved to query at client login!)
        q1 = self.execute_query(\
            "select count(*) from User where user_id = '{}'".format(user_id))
        if q1[0][0] == 0:
            return -1

        q2 = self.execute_query(\
            "select count(*) from Review where review_id = '{}'".format(review_id))
        if q2[0][0] == 0:
            return -2

        cur_reaction = self.execute_query(\
            "select react_type from ReviewReacts where user_id='{}'' and review_id='{}';".format())

        if len(cur_reaction) != 0:
            self.execute_query(\
                "update ReviewReacts set reaction = '{}' where user_id='{}' and review_id='{}';".format())



        #increment post's reaction counters
        

    # def like_tip(self, user_id, tip_id):
    #     query = ""
    #     self.execute_query(query)

    # def get_post(self, user, date):
    #     query = ""
    #     self.execute_query(query)

    # def get_all_categories(self):
    #     query = ""
    #     self.execute_query(query)

    # def get_all_users(self):
    #     query = ""
    #     self.execute_query(query)

if __name__ == '__main__':
    S = YelpServer()

    # testing
    # S.post_review('___DPmKJsBF2X6ZKgAeGqg', '__1uG7MLxWGFIv2fCGPiQQ', '4.0', 'Good physio')
    S.get_latest_posts('___I9ZYdYGkZ6dMYxwJEIQ')
    