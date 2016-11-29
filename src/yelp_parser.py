from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import json

with open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)
    response = client.get_business('mcdonalds-austin-12')
    print(response.business.name)
