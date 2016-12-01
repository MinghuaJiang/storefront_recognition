import storefront_recognizer
from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)
app.debug = True


@app.route('/map')
def home():
    return render_template('index.html')


@app.route('/business_v1', methods=['POST'])
def generate_business_info_v1():
    image = request.form['image']
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    return storefront_recognizer.get_business_info_v1(image, latitude, longitude)


@app.route('/business_v2', methods=['POST'])
def generate_business_info_v2():
    image = ""
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    return storefront_recognizer.get_business_info_v2(image, latitude, longitude)


if __name__ == "__main__":
    app.run()
