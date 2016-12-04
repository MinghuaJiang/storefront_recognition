import numpy as np
import cv2
import urllib
from yelp_parser import YelpParser
from google_street_view_parser import GoogleStreetViewParser
from collections import Counter

YELP_IMAGES_NUM = 4
GOOGLE_IMAGES_NUM = 2 # less than 3
MAX_RANK_WEIGHTS = [0.6, 0.3, 0.1]
PDF_LENGTH = 3

def get_nearby_images(yelpImages, googleImages):
    yelpImages = {key: yelpImages[key][0:YELP_IMAGES_NUM] for key in yelpImages.keys()}
    googleImages = {key: googleImages[key][0:GOOGLE_IMAGES_NUM] for key in googleImages.keys()}
    businessImages = Counter(yelpImages)+Counter(googleImages)
    return dict(businessImages)

def get_rankpdf(queryImage, businessImages):
    ranks = {key: get_businessrank(queryImage, businessImages[key], key) for key in businessImages.keys()}
    maxranks = dict(Counter(ranks).most_common(PDF_LENGTH))
    maxranks_pdf = {key: (maxranks[key] / float(sum(maxranks.values()))) for key in maxranks.keys()}
    print "max rank business pdf is %s" % (maxranks_pdf)
    return maxranks_pdf


def get_maxrank(queryImage, businessImages):
    ranks = {key: get_businessrank(queryImage, businessImages[key], key) for key in businessImages.keys()}
    maxrank = max(ranks, key=ranks.get)
    print "max rank business is %s, rank is %d" % (maxrank, ranks[maxrank])
    return maxrank


def get_businessrank(queryImage, businessImages, key):
    ranks = []
    for imageurl in businessImages:
        resp = urllib.urlopen(imageurl)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, 0)
        if image is not None:
            ranks.append(len(compare_image_orb(queryImage, image)))
    rank = compute_rank(ranks, key, 'weight')
    return rank


def compute_rank(ranks, key, method):
    if method == 'weight':
        max_ranks = sorted(ranks, reverse=True)[0:len(MAX_RANK_WEIGHTS)]
        rank = sum([a*b for a,b in zip(max_ranks, MAX_RANK_WEIGHTS)])
    elif method == 'avg':
        max_ranks = ranks
        rank = sum(ranks) / float(len(ranks))
    print(key, max_ranks, rank)
    return rank


def compare_image_sift(queryImage, trainImage):
    img1 = cv2.imread(queryImage, 0)
    img2 = trainImage

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)

    return good


def compare_image_orb(queryImage, trainImage):
    img1 = cv2.imread(queryImage, 0)
    img2 = trainImage

    # Initiate ORB detector
    orb = cv2.ORB_create()

    # find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img1,None)
    kp2, des2 = orb.detectAndCompute(img2,None)

    FLANN_INDEX_LSH = 6
    index_params= dict(algorithm = FLANN_INDEX_LSH,
                   table_number = 6, # 12
                   key_size = 12,     # 20
                   multi_probe_level = 1) #2
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m_n in matches:
        if len(m_n) != 2:
            continue
        (m,n) = m_n
        if m.distance < 0.7*n.distance:
            good.append(m)

    return good

if __name__ == '__main__':
    yelp_parser = YelpParser()
    yelp_response = yelp_parser.get_lexicon_names_by_bounding_box(0.15, latitude=38.0345394, longitude=-78.5000063)
    yelp_images = yelp_parser.get_outside_images_for_businesses(yelp_response)
    google_parser = GoogleStreetViewParser()
    google_images = google_parser.get_image_for_businesses(yelp_response)

    business_images = get_nearby_images(yelp_images, google_images)
    maxrank = get_rankpdf("cafe.jpg", business_images)