import storefront_recognizer
from flask import Flask
from flask import request

app = Flask(__name__)
app.debug = True


@app.route('/business', methods=['POST'])
def generate_business_info(image, latitude, longitude):
    return storefront_recognizer.get_business_info(image, latitude, longitude)