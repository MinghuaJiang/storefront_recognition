
import operator


def detect_and_recognize_text(image, lexicons):
    detectedText = ""
    edit_distance = dict()
    for business_name in lexicons.keys():
        edit_distance[business_name] = calculate_edit_distance(detectedText, business_name)
    return lexicons[min(edit_distance.iteritems(), key=operator.itemgetter(1))[0]]

def calculate_edit_distance(str1, str2):
    return 1