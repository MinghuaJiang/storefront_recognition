
import json
import text_recognizer
from yelp_parser import YelpParser
from google_street_view_parser import GoogleStreetViewParser
import image_comparer
import urllib
from collections import Counter

yelp_parser = YelpParser()
google_parser = GoogleStreetViewParser()


def get_business_info_v1(image_url, latitude, longitude):
    image = get_image_from_url(image_url)
    result_dic = yelp_parser.get_lexicon_names_by_bounding_box(0.15, latitude=latitude, longitude=longitude)
    lexicons = generate_lexicons(result_dic)
    text_pdf = get_text_recognizer_pdf(image, lexicons)
    near_by_images = get_nearby_image_info(result_dic)
    image_pdf = get_image_recoginizer_pdf(image, near_by_images)
    business_id = combine_pdf(text_pdf, image_pdf)
    response = result_dic[business_id]
    return json.dumps(generate_parsed_response(response))


def get_business_info_v2(image_url, latitude, longitude):
    image = get_image_from_url(image_url)
    result_dic = yelp_parser.get_lexicon_names_by_bounding_box(0.15, latitude=latitude, longitude=longitude)
    business = get_business_from_trained_model(image)
    lexicons = generate_lexicons(result_dic)
    business_id = lexicons[business]
    response = result_dic[business_id]
    return json.dumps(generate_parsed_response(response))


def get_image_from_url(image_url):
    image_name = "scene.jpg"
    urllib.urlretrieve(image_url, image_name)
    return image_name


def get_business_from_trained_model(image):
    return "Bodo's Bagels"


def generate_lexicons(businesses):
    lexicons = dict()
    for business_id in businesses.keys():
        lexicons[businesses[business_id].name] = business_id
    return lexicons


def get_nearby_image_info(businesses):
    yelp_images = yelp_parser.get_outside_images_for_businesses(businesses)
    google_images = google_parser.get_image_for_businesses(businesses)
    return image_comparer.get_nearby_images(yelp_images, google_images)


def get_image_recoginizer_pdf(image, near_by_image_dict):
    return image_comparer.get_maxrank(image, near_by_image_dict)


def get_text_recognizer_pdf(image, lexicons):
    return text_recognizer.detect_and_recognize_text(image, lexicons)


def combine_pdf(text_pdf, image_pdf):
    text_weight, image_weight = get_trained_weight()
    combined_dict = Counter()
    for key in text_pdf.keys():
        combined_dict[key] += text_pdf[key] * text_weight
    for key in image_pdf.keys():
        combined_dict[key] += image_pdf[key] * image_weight
    return combined_dict.most_common(1)[0][0]


def get_trained_weight():
    return 0.6, 0.4


def generate_parsed_response(response):
    response_dict = dict()
    response_dict["name"] = response.name
    response_dict["address"] = ",".join(response.location.display_address)
    response_dict["rating"] = str(response.rating) + "/5.0"
    response_dict["category"] = ",".join([category[0] for category in response.categories])
    response_dict["phone"] = response.display_phone
    return response_dict


if __name__ == "__main__":
    print(get_business_info_v1("bodo.jpg", 38.035440578, -78.5010249))
    print(get_business_info_v2("", 38.035440578, -78.5010249))