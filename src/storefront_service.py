import storefront_recognizer

def generate_business_info(image, latitude, longitude):
    return storefront_recognizer.get_business_info(image, latitude, longitude)