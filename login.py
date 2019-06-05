from database import Database
from user import User
from twitter_utils import get_request_token, get_oauth_verifier, get_access_token

Database.initialise(database="Learning", user="postgres",
                    password=" ", host="Localhost")

user_first_name = str(input("Please enter your first name: "))
user_last_name = str(input("Please enter your last name: "))
user_email = str(input("Please enter your email: "))


user = User.load_from_db_by_email(user_email)

if not user:
    request_token = get_request_token()
    oauth_verifier = get_oauth_verifier(request_token)

    access_token = get_access_token(request_token, oauth_verifier)

    user = User(user_email, user_first_name, user_last_name, access_token['oauth_token'],
                access_token['oauth_token_secret'], None)

    user.save_to_db()

search_result = user.twitter_requests('https://api.twitter.com/1.1/search/tweets.json?q=%23UCL&result_type=recent')

for tweet in search_result['statuses']:
    print("{} tweeted: {}.\n".format(tweet['user']['screen_name'], tweet['text']))
