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

post - Post a review to a business.
    usage:
        post review <stars> <business-id> <text>

    <stars> is an integer from 1 to 5

follow - Follow a user, business or category
    usage:
        follow <follow-type> <id>

    <category-type> can be either "user", "business", or "category"
    <id> can be a user id, business id, or category

feed - Returns the latest feed content from the last time the user signed in
       A sign in is recorded for a user every time the CLI is run.
    usage:
        feed <?num_posts?>
    
    <?num_posts?> is an optional argument, indicating the number of posts to show on the feed

react - Adds a reaction to the review specified as the argument (only for reviews)
    usage:
        react <review-id> <reaction-type>

    For a review:
        <reaction-type> can be "useful", "funny", "cool"

        """

        print(help_string)

    def post_review(self, stars, restaurant_id, text):
        self.ys.post_review(self.user_id, restaurant_id, stars, text)

    def follow_user(self, following_user_id):
        self.ys.follow_user(self.user_id, following_user_id)

    def follow_business(self, business_id):
        self.ys.follow_business(self.user_id, business_id)

    def follow_category(self, category):
        self.ys.follow_category(self.user_id, category)

    def feed(self, num_posts = 0):
        self.ys.get_latest_posts(self.user_id, num_posts)

    def react_to_review(self, review_id, reaction):
        self.ys.react_to_review(self.user_id, review_id, reaction)

    def client_interface(self):

        print('Welcome to the Yelp Client. Please enter your login user_id.')

        while(True):
            user_login = raw_input().split(" ")[0]
            if len(user_login) == 22:
                if self.ys.login_user(user_login) == 0:
                    self.user_id = user_login
                    break
                else:
                    print("The user ID you entered is not registered. Please try again...")
            else:
                print("User ID must be 22 characters. Please try again...")
            
        print('Login successful!\nFor a list of commands, type the command "help".')

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

                    if not stars.isdigit() or int(stars) > 5 or int(stars) < 1:
                        print("Invalid input for stars. Stars should be between 1 and 5. Please try again.")
                        continue

                    restaurant_id = input_list[3]
                    text = input_list[4]

                    result = self.post_review(stars, restaurant_id, text)

                    if result == 0:
                        print("Review posted successfully.")
                    elif result == -2:
                        print("Invalid business ID. The business does not exist.")

                else:
                    print('Invalid post type. Valid post types currently include "review"')
                    continue

            elif command == "follow":

                if len(input_list) != 3:
                    print("Invalid input. Please add follow type and either a user ID, business ID, or category.")
                    continue

                follow_type = input_list[1]

                if follow_type == "user":
                    user_id = input_list[2]
                    self.follow_user(user_id)
                    if result == 0:
                        print("User {} followed successfully.".format(user_id))
                    elif result == -2:
                        print("Invalid user ID. The user does not exist.")

                elif follow_type == "business":
                    business_id = input_list[2]
                    self.follow_business(business_id)
                    if result == 0:
                        print("Business {} followed successfully.".format(business_id))
                    elif result == -2:
                        print("Invalid business ID. The business does not exist.")

                elif follow_type == "category":
                    category = input_list[2]
                    self.follow_category(category)
                    if result == 0:
                        print("{} followed successfully.".format(category))
                    elif result == -2:
                        print("Invalid category. The category does not exist.")
                else:
                    print('Invalid follow type. Valid follow types are "user", "business", or "category".')

            elif command == "feed":
                if len(input_list) == 2 and input_list[1].isdigit():
                    self.feed(input_list[1])
                elif len(input_list) == 1:
                    self.feed()
                else:
                    print("Invalid input. The feed command takes at most 1 argument.")
                    continue

            elif command == "react":
                if len(input_list) != 3:
                    print("Invalid input. Please add a review ID and a reaction.")
                    continue
                
                review_id = input_list[1]
                reaction = input_list[2]

                if reaction != "useful" and \
                    reaction != "funny" and \
                    reaction != "cool":
                    print("Invalid reaction type.")
                    continue

                self.react_to_review(review_id, reaction)
                if result == 0:
                    print("Reacted to review {} successfully.".format(review_id))
                elif result == -2:
                    print("Invalid review_id. The review does not exist.")

            else:
                print('Invalid input. Please try again. For more information type "help".')
                continue


if __name__ == '__main__':
    c = Client()

    c.client_interface()

