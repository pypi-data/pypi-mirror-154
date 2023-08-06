from shapely.geometry import shape, box

BBox = list[float]


def check_tweet_location_inside_bbox(tweet, bbox: BBox, accuracy: int = 0):
    polygon = None

    if accuracy == 0:
        return True

    if tweet.coordinates:
        polygon = shape(tweet._json["coordinates"])
    elif tweet.place:
        polygon = shape(tweet._json["place"]["bounding_box"])
    else:
        return False

    container = box(*bbox, ccw=True)

    contains = container.contains(polygon)
    overlaps = container.overlaps(polygon)

    if accuracy == 1:
        return contains or overlaps

    return contains
