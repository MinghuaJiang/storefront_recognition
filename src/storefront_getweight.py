
import json
import text_recognizer
from yelp_parser import YelpParser
import urllib
from collections import Counter
import pickle
import yelp_parser
import storefront_recognizer
import image_comparer
import os.path

yelp_parser = YelpParser()

datapath = 'outside_all_s'

def get_testresults(image, name, address):
    lat, lng = get_position(address)
    result_dic = yelp_parser.get_lexicon_names_by_bounding_box(0.15, latitude=lat, longitude=lng)
    lexicons = storefront_recognizer.generate_lexicons(result_dic)
    text_result = text_recognizer.detect_and_recognize_text_for_training(image, lexicons)
    near_by_images = storefront_recognizer.get_nearby_image_info(result_dic)
    image_result = image_comparer.get_maxrank(image, near_by_images)
    # print(name, image_result, text_result)
    text_name, image_name = yelp_parser.get_businessname(text_result), yelp_parser.get_businessname(image_result)
    return [name_euqal(image_name, name), name_euqal(text_name, name)]

def name_euqal(name1, name2):
    return name1 == name2 or name1 == name2 + ' '


def get_position(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+ address +'&key=AIzaSyC5BG3tKK5d_5c5g94vRqQi3rVT5ox1mZw'
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data['results'][0]['geometry']['location']['lat'], data['results'][0]['geometry']['location']['lng']

def get_weight(result):
    r00, r01, r11, r10 = 0,0,0,0
    for x in result:
        if x[0] == 0 and x[1] == 0:
            r00 += 1
        elif x[0] == 0 and x[1] == 1:
            r01 += 1
        elif x[0] == 1 and x[1] == 1:
            r11 += 1
        elif x[0] == 1 and x[1] == 0:
            r10 += 1
    print 'both wrong: %d, text right: %d, image right: %d, both right: %d' % (r00, r01, r10, r11)
    if r10 + r01 == 0:
        return 0, 0
    else:
        return [r10/float(r10+r01), r01/float(r10+r01)]

if __name__ == "__main__":
    image_dict = pickle.load( open( "test_dict.p", "rb" ) )
    # image_dict = {k: image_dict[k] for k in image_dict.keys()}
    results = []
    counter = 0
    res_dict = dict()

    for k, v in image_dict.iteritems():
        image = k+'.jpg'
        imagepath = datapath+'/'+image
        if os.path.exists(imagepath):
            counter += 1
            name = v[0]
            address = v[1]
            print(counter, imagepath)
            result = get_testresults(imagepath, name, address)
            results.append(result)
            res_dict[image] = result
            print(name, result)
            print(get_weight(results))

            if counter % 30 == 0:
                pickle.dump( res_dict, open( "weight.p", "wb" ) )

    weight = get_weight(results)
    pickle.dump( res_dict, open( "weight.p", "wb" ) )
