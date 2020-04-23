import yelp_api

class Client(object):
    def __init__(self):
        self.ys = yelp_api.YelpServer()
        self.user_id = None

    def help(self):
        help_string = """

Help documentation

Commands List:

help - Get help on CLI usage.
    usage:
        help

post - Post a review or tip to a restaurant.
    usage:
        post review <stars> <restaurant-id> <text>

        or

        post tip <restaurant-id> <text>

    <stars> is an integer from 1 to 5

follow - Follow a user, business or category
    usage:
        follow <user-id>

    <id> can be a user id, business id, or category id

feed - Returns the latest feed content from the last time the user signed in
       A sign in is recorded for a user every time the CLI is run.
    usage:
        feed

react - Adds a reaction to the review specified as the argument
    usage:
        react <review-id> <reaction-type>

        or

        react <tip-id> <reaction-type>

    For a review:
        <reaction-type> can be "useful", "funny", "cool"

    For a tip:
        <reaction-type> can be "like"

get - Gets either a post, all categories, or all users
    usage:
        get <get-type>

    <get-type> is either "post", "categories" or "users"

search - Search for a post, category, user, or business
    usage:
        search <search-type> <search-query>

    <search-type> is either "post", "category", "user", or "business"
    <search-query> is all or part of the word to be matched


        """

        print(help_string)

    def post_review(self, stars, restaurant_id, text):
        self.ys.post_review(self.user_id, restaurant_id, stars, text)

    def post_tip(self, restaurant_id, text):
        self.ys.post_tip(self.user_id, restaurant_id, text)

    def follow_user(self, following_user_id):
        self.ys.follow_user(self.user_id, following_user_id)

    def follow_business(self, business_id):
        self.ys.follow_business(self.user_id, business_id)

    def follow_category(self, category):
        self.ys.follow_category(self.user_id, category)

    def feed(self):
        self.ys.get_latest_posts(self.user_id)

    def client_interface(self):

        print('Welcome to the Yelp Client. For a list of commands, type the command "help".')

        while(True):

            command_string = raw_input()

            input_list = command_string.split(" ")

            command = input_list[0]

            if command == "help":
                self.help()
            elif command == "post":
                if len(input_list) < 2:
                    print("Invalid input. Please add review type and review text")
                    continue

                post_type = input_list[1]

                if post_type == "review":
                    input_list = command_string.split(" ", 4)

                    if len(input_list) < 3:
                        print("Invalid input. Please add stars")
                        continue
                    elif len(input_list) < 4:
                        print("Invalid input. Please add restaruant-id")
                        continue
                    elif len(input_list) < 5:
                        print("Invalid input. Please add review text")
                        continue

                    stars = input_list[2]

                    if int(stars) > 5 or int(stars) < 1:
                        print("Invalid input for stars. Stars should be between 1 and 5. Please try again.")
                        continue

                    restaurant_id = input_list[3]
                    text = input_list[4]

                    self.post_review(stars, restaurant_id, text)

                elif post_type == "tip":
                    input_list = command_string.split(" ", 3)

                    if len(input_list) < 3:
                        print("Invalid input. Please add restaruant-id")
                        continue
                    elif len(input_list) < 4:
                        print("Invalid input. Please add review text")
                        continue

                    restaurant_id = input_list[2]
                    text = input_list[3]

                    self.post_tip(restaurant_id, text)

                else:
                    print('Invalid post type. Valid post types are "tip" and "review"')
                    continue


                

            elif command == "follow":

                if len(input_list) != 3:
                    print("Invalid input. Please add follow type and either a user ID, business ID, or category.")
                    continue

                follow_type = input_list[1]

                if follow_type == "user":
                    user_id = input_list[2]
                    self.follow_user(user_id)

                elif follow_type == "business":
                    business_id = input_list[2]
                    self.follow_business(business_id)

                elif follow_type == "category":
                    category = input_list[2]
                    self.follow_category(category)
                else:
                    print('Invalid follow type. Valid follow types are "user", "business", or "category".')




            elif command == "feed":
                if len(input_list) != 1:
                    print("Invalid input. The feed command takes no arguments.")
                    continue
                self.feed()
            elif command == "react":
                self.react()
            elif command == "get":
                self.get()
            elif command == "search":
                self.search()
            else:
                print('Invalid input. Please try again. For more information type "help".')
                continue




if __name__ == '__main__':
    c = Client()

    c.client_interface()

