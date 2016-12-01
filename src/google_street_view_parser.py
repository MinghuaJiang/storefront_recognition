import json
import urllib


class GoogleStreetViewParser:
    def __init__(self):
        url = "https://maps.googleapis.com/maps/api/streetview?"
        with open('google_config_secret.json') as cred:
            creds = json.load(cred)
            key = creds["api_key"]
            self.base_url = url + "key=" + key

    def get_image_for_businesses(self, businesses):
        result = dict()
        for business_id in businesses.keys():
            image_list = []
            business = businesses[business_id]
            location = business.location.coordinate
            latitude = location.latitude
            longitude = location.longitude
            fov = [70, 80, 90]
            for each in fov:
                image_url = self.base_url + "&size=640x640&location="+str(latitude)+","+str(longitude)+"&fov="+str(each)
                image_list.append(image_url)
            result[business_id] = image_list
        return result
