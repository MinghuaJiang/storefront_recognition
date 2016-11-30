from yelp_parser import YelpParser


def generate_lexicon_by_bounding_box(distance, **coordinate):
    yelp_parser = YelpParser()
    return yelp_parser.get_lexicon_names_by_bounding_box(distance, **coordinate)

