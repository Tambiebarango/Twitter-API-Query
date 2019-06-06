import oauth2
import constants
import urllib.parse as urlparse

consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)


def get_request_token():
    client = oauth2.Client(consumer)
    # use the client to perform a post request for the request token
    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')

    # check if response is valid
    if response.status != 200:
        print("Error while requesting request token!")

    request_token = dict(urlparse.parse_qsl(content.decode('utf-8')))
    return request_token


def get_oauth_verifier(request_token):
    print('Go to the following website:')

    print(get_oauth_verifier_url(request_token))
    return input("Please enter the pin received from the authorization website: ")


def get_oauth_verifier_url(request_token):
    return ('{}?oauth_token={}'.format(constants.AUTHORIZATION_URL,
                                       request_token['oauth_token']))


def get_access_token(request_token, oauth_verifier):
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)

    client = oauth2.Client(consumer, token)

    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')

    if response.status != 200:
        print("Error while requesting access token!")

    access_token = dict(urlparse.parse_qsl(content.decode('utf-8')))
    return access_token
