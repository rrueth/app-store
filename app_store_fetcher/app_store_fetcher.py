import requests


class Review(object):
    """A JSON review is made up of:
    - author:
        - uri
            - label (What exactly does this point to?)
        - name
            - label (user name writing the review)
        - label (Seems to be empty)
    - im:version:
        - label (version string)
    - im:rating:
        - label (1 - 5 representing the number of stars given by the reviewer)
    - id:
        - label (string representing the ID of the review?)
    - title:
        - label (review title)
    - content:
        - label (the primary review)
        - attributes:
            - type ("text", when would this be anything other than "text?")
    - link
        - attributes
            - rel ("related")
            - href (links to something? related apps in this case?)
    - im:voteSum:
        - label ("0", not sure what the vote sum is yet)
    - im:contentType:
        - attributes:
            - term ("Application")
            - label ("Application")
    - im:voteCount:
        - label ("0", not sure what this is yet)
    """
    def __init__(self, json_dict):
        self._json_dict = json_dict

    def __eq__(self, other):
        return bool(self._json_dict == other._json_dict)

    @staticmethod
    def is_review(json_dict):
        """
        :param json_dict: A JSON object represented as a dictionary.
        :return: True if the json_dict represents a review.
        """
        return bool("im:rating" in json_dict)

    def author_name(self):
        return self._json_dict["author"]["name"]["label"]

    def content(self):
        return self._json_dict["content"]["label"]

    def rating(self):
        """
        :return: An integer from 1 to 5 denoting the number of stars given by the reviewer.
        """
        return int(self._json_dict["im:rating"]["label"])

    def title(self):
        return self._json_dict["title"]["label"]

    def version(self):
        return self._json_dict["im:version"]["label"]


def fetch_reviews(app_id, page_num):
    """Fetch a single page of reviews for a given app_id.

    :param app_id: The ID of the app in the app store.
    :param page_num: The page of reviews to fetch.
    :return: A list of Review objects.
    """
    # page=1 is the same as if the "page" param was left off.
    url = "https://itunes.apple.com/us/rss/customerreviews/page={page_num}/id={app_id}/sortBy=mostRecent/json".format(
        page_num=page_num,
        app_id=app_id,
    )
    r = requests.get(url)
    feed_json = r.json()["feed"]

    return [Review(entry) for entry in feed_json["entry"] if Review.is_review(entry)]


if __name__ == "__main__":
    # TODO - Ryan - Eventually break this down and pass the url parameters properly
    # TODO - Ryan - Implement following next/previous links.
    content_strings = []
    urls = ["https://itunes.apple.com/us/rss/customerreviews/id=383298204/sortBy=mostRecent/json"]
    for i in range(1, 11):
        urls.append(
            "https://itunes.apple.com/us/rss/customerreviews/page={page_num}/id=383298204/sortby=mostrecent/json".format(
                page_num=i,
            ))
    # urls =[]
    for url in urls:
        print(url)
        r = requests.get(url)

        # TODO - Ryan:
        # - Parse the JSON
        feed_json = r.json()["feed"]
        # print(feed_json)
        for entry in feed_json["entry"]:
            if Review.is_review(entry):
                content_strings.append(Review(entry).content())
