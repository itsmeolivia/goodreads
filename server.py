from flask import Flask
from rauth.service import OAuth1Service, OAuth1Session
from bs4 import BeautifulSoup
import os

CONSUMER_KEY = os.environ['GOODREADSKEY']
CONSUMER_SECRET = os.environ['GOODREADSSECRET']

goodreads = OAuth1Service(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    name='goodreads',
    request_token_url='http://www.goodreads.com/oauth/request_token',
    authorize_url='http://www.goodreads.com/oauth/authorize',
    access_token_url='http://www.goodreads.com/oauth/access_token',
    base_url='http://www.goodreads.com/'
    )

request_token, request_token_secret = goodreads.get_request_token(header_auth=True)

authorize_url = goodreads.get_authorize_url(request_token)

session = goodreads.get_auth_session(request_token, request_token_secret)

response = session.get('https://www.goodreads.com/api/auth_user')
soup = BeautifulSoup(response.text)
user_id = soup.find('user').get('id')

# these values are what you need to save for subsequent access.
ACCEESS_TOKEN = session.access_token
ACCESS_TOKEN_SECRET = session.access_token_secret

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
