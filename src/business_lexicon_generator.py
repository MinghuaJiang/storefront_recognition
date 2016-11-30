from yelp_parser import YelpParser


def generate_lexicon_by_bounding_box(distance, **coordinate):
    yelp_parser = YelpParser()
    return yelp_parser.get_lexicon_names_by_bounding_box(distance, **coordinate)

if __name__ == '__main__':
    response = generate_lexicon_by_bounding_box(0.15, latitude=38.0345394, longitude=-78.5000063)
    print(response["id"])
    print(response["name"])

