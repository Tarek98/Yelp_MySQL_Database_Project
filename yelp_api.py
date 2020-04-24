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

    def login_user(self, user_id):
        # validate that current user exists in User table
        q1 = self.execute_query(\
            "select count(*) from User where user_id = '{}'".format(user_id))
        if q1[0][0] == 0:
            # user_id doesn't exist! Please login with a valid user_id...
            return -1
        return 0

    def post_review(self, user_id, business_id, stars, text):
        # validate business exists
        qV = self.execute_query(\
            "select count(*) from Business where business_id = '{}'".format(business_id))
        if qV[0][0] == 0:
            return -2

        today_date = datetime.date.today().isoformat()
        self.execute_query("insert into Review (user_id, business_id, stars, date, text)" +\
            "values ('{}', '{}', '{}', '{}', '{}')".format(\
            user_id, business_id, stars, today_date, text))

        return 0

    def follow_user(self, user_id, following_user_id):
        # validate that both user being followed exists
        qV = self.execute_query(\
            "select count(*) from User where user_id = '{}'".format(following_user_id))
        if qV[0][0] == 0:
            return -2

        self.execute_query("insert into UserFollowers (user_id, follower_id)" +\
            "values ('{}', '{}')".format(following_user_id, user_id))

        return 0

    def follow_business(self, user_id, business_id):
        # validate business exists
        qV = self.execute_query(\
            "select count(*) from Business where business_id = '{}'".format(business_id))
        if qV[0][0] == 0:
            return -2

        self.execute_query("insert into BusinessFollowers (business_id, user_id)" +\
            "values ('{}', '{}')".format(business_id, user_id))

        return 0

    def follow_category(self, user_id, category):
         # validate category exists
        qV = self.execute_query(\
            "select count(*) from BusinessCategories where category = '{}'".format(category))
        if qV[0][0] == 0:
            return -2

        self.execute_query("insert into CategoryFollowers (category, user_id)" +\
            "values ('{}', '{}')".format(category, user_id))

        return 0

    # returns review_ids if num_posts_limit is 0, and 
    #  otherwise returns the limited number of full reviews
    def get_latest_posts(self, user_id, num_posts_limit = 0):
        # determine when user was last online (when they last read from all topics)
        last_online = self.execute_query(\
            "select last_online from User where user_id = '{}'".format(user_id))
        last_online = last_online[0][0]

        # find all users user follows
        users_followed = self.execute_query(\
            "select user_id from UserFollowers where follower_id = '{}'".format(user_id))
        if not users_followed:
            users_followed = "('')"
        else:
            users_followed = tuple(str(x[0]) for x in users_followed)
            if len(users_followed) == 1:
                # single element tuple has string form of "(e,)"; remove comma
                users_followed = str(users_followed).replace(",", "")
            else:
                users_followed = str(users_followed)
                
        # find all businesses user follows (or within categories user is interested in)
        query1 = "select distinct business_id from BusinessCategories where category in"+\
                " (select category from CategoryFollowers where user_id = '{}')".format(user_id)
        query2 = "select business_id from BusinessFollowers where user_id = '{}'".format(user_id)
        union_query = "select * from ( "+query1+" )bizInLikedCategory union ( "+query2+" )"
        businesses_followed = self.execute_query(union_query)
        if not businesses_followed:
            businesses_followed = "('')"
        else:
            businesses_followed = tuple(str(x[0]) for x in businesses_followed)
            if len(businesses_followed) == 1:
                # single element tuple has string form of "(e,)"; remove comma
                businesses_followed = str(businesses_followed).replace(",", "")
            else:
                businesses_followed = str(businesses_followed)
        
        # find latests posts from all followed topics/users since last read
        posts_query = "select distinct * from Review where date > '{}' and (user_id in {} or business_id in {})".format(\
            last_online, users_followed, businesses_followed)
            
        if num_posts_limit == 0:
            posts_query = self.execute_query(posts_query)
            # return list of review_ids
            return [p[0] for p in posts_query] if posts_query else []
        else:
            posts_query = self.execute_query(posts_query + " limit {}".format(num_posts_limit))
            # return list of review items (dictionaries)
            posts = []
            for p in posts_query:
                posts.append({"review_id": p[0], "user_id": p[1], "business_id": p[2], "stars": p[3], "date": p[4],
                    "text": p[5], "useful": p[6], "funny": p[7], "cool": p[8]})
            return posts

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
    # print(S.follow_business('1UnZiZiuDLYxDmE2uzvB4A', '4JNXUYY8wbaaDmk3BPzlWw'))
    print(S.get_latest_posts('1UnZiZiuDLYxDmE2uzvB4A', 10))
    