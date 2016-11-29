from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import json
import math


class YelpParser:
    def __init__(self):
        with open('config_secret.json') as cred:
            creds = json.load(cred)
            auth = Oauth1Authenticator(**creds)
            self.client = Client(auth)

    def get_lexicon_names_by_bounding_box(self, distance, **coordinate):
        params = {'lang': 'en'}
        latitude_sw = coordinate['latitude'] + (distance * math.cos(-135 * math.pi / 180)) / 111
        longitude_sw = coordinate['longitude'] + (distance * math.sin(-135 * math.pi / 180)) / (
            111 * math.cos(coordinate['latitude'] * math.pi / 180))
        latitude_ne = coordinate['latitude'] + (distance * math.cos(45 * math.pi / 180)) / 111
        longitude_ne = coordinate['longitude'] + (distance * math.sin(45 * math.pi / 180)) / (
            111 * math.cos(coordinate['latitude'] * math.pi / 180))

        print("original coordiate (%s, %s)" % (str(coordinate['latitude']), str(coordinate['longitude'])))
        print("south west coordiate (%s, %s)" % (str(latitude_sw), str(longitude_sw)))
        print("north east coordiate (%s, %s)" % (str(latitude_ne), str(longitude_ne)))

        response = self.client.search_by_bounding_box(
            latitude_sw,
            longitude_sw,
            latitude_ne,
            longitude_ne,
            **params)
        return [business.name for business in response.businesses]
