from yelp_parser import YelpParser


def generate_lexicon_by_position(distance, **coordinate):
    result = list()
    yelp_parser = YelpParser()
    result.extend(yelp_parser.get_lexicon_names_by_position(distance, **coordinate))
    return result

if __name__ == '__main__':
    print(generate_lexicon_by_position(0.15, latitude=38.0345168, longitude=-78.5010693))

