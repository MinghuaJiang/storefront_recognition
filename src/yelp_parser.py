from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import json
import math
from bs4 import BeautifulSoup
import urllib
from google_street_view_parser import GoogleStreetViewParser


class YelpParser:
    def __init__(self):
        with open('yelp_config_secret.json') as cred:
            creds = json.load(cred)
            auth = Oauth1Authenticator(**creds)
            self.client = Client(auth)
        self.baseurl = "https://www.yelp.com/biz_photos/"

    def get_lexicon_names_by_bounding_box(self, distance, **coordinate):
        params = {'lang': 'en'}
        latitude_sw = coordinate['latitude'] + (distance * math.cos(-135 * math.pi / 180)) / 111
        longitude_sw = coordinate['longitude'] + (distance * math.sin(-135 * math.pi / 180)) / (
            111 * math.cos(coordinate['latitude'] * math.pi / 180))
        latitude_ne = coordinate['latitude'] + (distance * math.cos(45 * math.pi / 180)) / 111
        longitude_ne = coordinate['longitude'] + (distance * math.sin(45 * math.pi / 180)) / (
            111 * math.cos(coordinate['latitude'] * math.pi / 180))

        print("original coordinate (%s, %s)" % (str(coordinate['latitude']), str(coordinate['longitude'])))
        print("south west coordinate (%s, %s)" % (str(latitude_sw), str(longitude_sw)))
        print("north east coordinate (%s, %s)" % (str(latitude_ne), str(longitude_ne)))

        response = self.client.search_by_bounding_box(
            latitude_sw,
            longitude_sw,
            latitude_ne,
            longitude_ne,
            **params)
        result = dict()
        for business in response.businesses:
            result[business.id] = business
        return result

    def get_outside_images_for_businesses(self, businesses):
        result = dict()
        for business_id in businesses.keys():
            url_list = self.get_outside_images_for_business(business_id)
            result[business_id] = url_list
        return result

    def get_outside_images_for_business(self, business_id):
        url = self.baseurl + business_id + "?tab=outside"
        socket = urllib.urlopen(url)
        html = socket.read()
        soup = BeautifulSoup(html, 'html.parser')
        result = [link.get("src").replace("258s", "o") for link in soup.findAll("img", {"class": "photo-box-img"}) if
                  "258s" in link.get("src")]
        socket.close()
        return result


if __name__ == '__main__':
    yelp_parser = YelpParser()
    yelp_response = yelp_parser.get_lexicon_names_by_bounding_box(0.15, latitude=38.0354405, longitude=-78.5010249)
    print(yelp_parser.get_outside_images_for_businesses(yelp_response))
    google_parser = GoogleStreetViewParser()
    google_response = google_parser.get_image_for_businesses(yelp_response)
    print(google_response)
