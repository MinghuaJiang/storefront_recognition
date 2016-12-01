
import json
import text_recognizer
from yelp_parser import YelpParser
from google_street_view_parser import GoogleStreetViewParser

yelp_parser = YelpParser()
google_parser = GoogleStreetViewParser()


def get_business_info_v1(image, latitude, longitude):
    result_dic = yelp_parser.get_lexicon_names_by_bounding_box(0.15, latitude=latitude, longitude=longitude)
    lexicons = generate_lexicons(result_dic)
    text_pdf = get_text_recognizer_pdf(image, lexicons)
    near_by_images = get_nearby_image_info(result_dic)
    image_pdf = get_image_recoginizer_pdf(image,near_by_images)
    business_id = combine_pdf(text_pdf, image_pdf)
    response = result_dic[business_id]
    return json.dumps(generate_parsed_response(response))


def get_business_info_v2(image, latitude, longitude):
    result_dic = yelp_parser.get_lexicon_names_by_bounding_box(0.15, latitude=latitude, longitude=longitude)
    business = get_business_from_trained_model(image)
    lexicons = generate_lexicons(result_dic)
    business_id = lexicons[business]
    response = result_dic[business_id]
    return json.dumps(generate_parsed_response(response))


def get_business_from_trained_model(image):
    return "Bodo's Bagels"


def generate_lexicons(businesses):
    lexicons = dict()
    for business_id in businesses.keys():
        lexicons[businesses[business_id].name] = business_id
    return lexicons


def get_nearby_image_info(businesses):
    return 1


def get_image_recoginizer_pdf(image, near_by_image_dict):
    return 1


def get_text_recognizer_pdf(image, lexicons):
    return text_recognizer.detect_and_recognize_text(image, lexicons)


def combine_pdf(text_pdf, image_pdf):
    return "bodos-bagels-charlottesville"


def generate_parsed_response(response):
    response_dict = dict()
    response_dict["name"] = response.name
    response_dict["address"] = ",".join(response.location.display_address)
    response_dict["rating"] = str(response.rating) + "/5.0"
    response_dict["category"] = ",".join([category[0] for category in response.categories])
    response_dict["phone"] = response.display_phone
    return response_dict

if __name__ == "__main__":
    print(get_business_info_v1("", 38.035440578, -78.5010249))
    print(get_business_info_v2("", 38.035440578, -78.5010249))