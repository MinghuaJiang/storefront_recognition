import operator
import editdistance


def detect_and_recognize_text(image, lexicons):
    detectedText = ""
    edit_distance = dict()
    for business_name in lexicons.keys():
        edit_distance[lexicons[business_name]] = calculate_edit_distance(detectedText, business_name)
    return lexicons[min(edit_distance.iteritems(), key=operator.itemgetter(1))[0]]


def calculate_edit_distance(str1, str2):
    return editdistance.eval(str1, str2)

