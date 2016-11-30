from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import json
import math
from bs4 import BeautifulSoup
import urllib


class YelpParser:
    def __init__(self):
        with open('config_secret.json') as cred:
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

        print("original coordiate (%s, %s)" % (str(coordinate['latitude']), str(coordinate['longitude'])))
        print("south west coordiate (%s, %s)" % (str(latitude_sw), str(longitude_sw)))
        print("north east coordiate (%s, %s)" % (str(latitude_ne), str(longitude_ne)))

        response = self.client.search_by_bounding_box(
            latitude_sw,
            longitude_sw,
            latitude_ne,
            longitude_ne,
            **params)
        result = dict()
        result["id"] = [business.id for business in response.businesses]
        result["name"] = [business.name for business in response.businesses]
        return result

    def get_outside_images_for_businesses(self, businesses):
        result = dict()
        for i in range(0, len(businesses["id"])):
            url_list = self.get_outside_images_for_business(businesses["id"][i])
            result[businesses["name"][i]] = url_list
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
    response = yelp_parser.get_lexicon_names_by_bounding_box(0.15, latitude=38.0345394, longitude=-78.5000063)
    print(response["id"])
    print(response["name"])
    print(yelp_parser.get_outside_images_for_businesses(response))
