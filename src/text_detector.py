#!/usr/bin/python

from PIL import Image
import sys
import pytesseract


def detect_text(image_file):
    im = Image.open(image_file)
    return pytesseract.image_to_string(im)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python text_detector.py image_path"
        sys.exit()
    image_path = sys.argv[1]
    text = detect_text(image_path)
    print text

