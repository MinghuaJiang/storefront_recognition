import operator
import editdistance
import subprocess
from collections import Counter


def detect_and_recognize_text(image, lexicons):
    args = ("text-recognizer/text_recognizer", image)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    (output, err) = popen.communicate()
    popen.wait()
    detected_text = [word for word in output.split("\n") if len(word) > 4]
    print(detected_text)
    counter = Counter()
    for text in detected_text:
        for business_name in lexicons.keys():
            if business_name in counter:
                if 20 - calculate_edit_distance(text, business_name) > counter[business_name]:
                    counter[business_name] = 20 - calculate_edit_distance(text, business_name)
            else:
                counter[business_name] = 20 - calculate_edit_distance(text, business_name)

    result = counter.most_common(5)
    print(result)
    dist_sum = 0
    final_result = dict()
    for k, v in result:
        if v > 0:
            dist_sum += v

    for k, v in result:
        if v > 0:
            final_result[lexicons[k]] = float(v) / dist_sum

    print(final_result)


def calculate_edit_distance(str1, str2):
    return editdistance.eval(str1, str2)


if __name__ == '__main__':
    detect_and_recognize_text("/home/cutehuazai/test.png", {"yuan ho carry out":"123", "fry spring":"234"})

