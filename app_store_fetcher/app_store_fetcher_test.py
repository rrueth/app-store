import json
import unittest
try:
    import unittest.mock as mock
except ImportError:
    import mock

import requests

import app_store_fetcher

# The FEED_TEMPLATE requires the user to supply a 'reviews_json_str' parameter with format.
FEED_TEMPLATE = """{{"feed":{{"author":{{"name":{{"label":"iTunes Store"}}, "uri":{{"label":"http://www.apple.com/itunes/"}}}}, "entry":[
{{"im:name":{{"label":"shopkick - Rewards & Free Gift Cards for Shopping plus Deals & Discounts"}}, "rights":{{"label":"© 2016 shopkick, Inc."}}, "im:price":{{"label":"Get", "attributes":{{"amount":"0.00000", "currency":"USD"}}}}, "im:image":[
{{"label":"http://is4.mzstatic.com/image/thumb/Purple49/v4/35/b2/6d/35b26d92-82f4-356c-8c7b-2600f0e204b3/mzl.kfiuakmi.png/53x53bb-85.png", "attributes":{{"height":"53"}}}},
{{"label":"http://is1.mzstatic.com/image/thumb/Purple49/v4/35/b2/6d/35b26d92-82f4-356c-8c7b-2600f0e204b3/mzl.kfiuakmi.png/75x75bb-85.png", "attributes":{{"height":"75"}}}},
{{"label":"http://is5.mzstatic.com/image/thumb/Purple49/v4/35/b2/6d/35b26d92-82f4-356c-8c7b-2600f0e204b3/mzl.kfiuakmi.png/100x100bb-85.png", "attributes":{{"height":"100"}}}}], "im:artist":{{"label":"shopkick", "attributes":{{"href":"https://itunes.apple.com/us/developer/shopkick/id337824568?mt=8&uo=2"}}}}, "title":{{"label":"shopkick - Rewards & Free Gift Cards for Shopping plus Deals & Discounts - shopkick"}}, "link":{{"attributes":{{"rel":"alternate", "type":"text/html", "href":"https://itunes.apple.com/us/app/shopkick-rewards-free-gift/id383298204?mt=8&uo=2"}}}}, "id":{{"label":"https://itunes.apple.com/us/app/shopkick-rewards-free-gift/id383298204?mt=8&uo=2", "attributes":{{"im:id":"383298204", "im:bundleId":"com.shopkick.shopkick"}}}}, "im:contentType":{{"attributes":{{"term":"Application", "label":"Application"}}}}, "category":{{"attributes":{{"im:id":"6024", "term":"Shopping", "scheme":"https://itunes.apple.com/us/genre/ios-shopping/id6024?mt=8&uo=2", "label":"Shopping"}}}}, "im:releaseDate":{{"label":"2010-08-16T00:00:00-07:00", "attributes":{{"label":"August 16, 2010"}}}}}},
{reviews_json_str}
{{"attributes":{{"rel":"alternate", "type":"text/html", "href":"https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewGrouping?cc=us&id=38"}}}},
{{"attributes":{{"rel":"self", "href":"https://itunes.apple.com/us/rss/customerreviews/page=1/id=383298204/sortby=mostRecent/json"}}}},
{{"attributes":{{"rel":"first", "href":"https://itunes.apple.com/us/rss/customerreviews/page=1/id=383298204/sortby=mostrecent/xml?urlDesc=/customerreviews/page=1/id=383298204/sortby=mostRecent/json"}}}},
{{"attributes":{{"rel":"last", "href":"https://itunes.apple.com/us/rss/customerreviews/page=10/id=383298204/sortby=mostrecent/xml?urlDesc=/customerreviews/page=1/id=383298204/sortby=mostRecent/json"}}}},
{{"attributes":{{"rel":"previous", "href":"https://itunes.apple.com/us/rss/customerreviews/page=1/id=383298204/sortby=mostrecent/xml?urlDesc=/customerreviews/page=1/id=383298204/sortby=mostRecent/json"}}}},
{{"attributes":{{"rel":"next", "href":"https://itunes.apple.com/us/rss/customerreviews/page=2/id=383298204/sortby=mostrecent/xml?urlDesc=/customerreviews/page=1/id=383298204/sortby=mostRecent/json"}}}}], "id":{{"label":"https://itunes.apple.com/us/rss/customerreviews/page=1/id=383298204/sortby=mostRecent/json"}}}}}}
"""

# The REVIEW_ENTRY requires the user to supply a 'title' parameter with format.
REVIEW_ENTRY = """{{
  "im:version": {{"label": "4.8.1"}},
  "title": {{"label": "{title}"}},
  "author": {{"label": "",
             "uri": {{"label": "https://itunes.apple.com/us/reviews/id171860631"}},
             "name": {{"label": "Awesome he"}}}},
  "im:voteCount": {{"label": "0"}},
  "content": {{"attributes": {{"type": "text"}},
              "label": "I love this but it does not have a lot of stuff that in our area on it."}},
  "link": {{"attributes": {{"href": "https://itunes.apple.com/us/review?id=383298204&type=Purple%20Software",
                          "rel": "related"}}}},
  "im:rating": {{"label": "5"}},\
  "im:contentType": {{"attributes": {{"term": "Application",
                                    "label": "Application"}}}},
  "id": {{"label": "1330930867"}},
  "im:voteSum": {{"label": "0"}}
}}
"""

def _create_review_json_str(title="Shop kick"):
    return REVIEW_ENTRY.format(title=title)

def _review(json_dict=None):
    json_dict = json_dict or json.loads(_create_review_json_str())
    return app_store_fetcher.Review(json_dict)


class TestReview(unittest.TestCase):
    # TODO - Ryan - add test for is_review function

    def test_should_evaluate_the_review_objects_as_equalivalent(self):
        self.assertEqual(_review(json_dict=json.loads(_create_review_json_str(title="Ryan's great review"))),
                         _review(json_dict=json.loads(_create_review_json_str(title="Ryan's great review"))))

    def test_should_evaluate_the_review_objects_as_not_equivalent(self):
        self.assertNotEqual(_review(json_dict=json.loads(_create_review_json_str(title="Bo's bad review"))),
                            _review(json_dict=json.loads(_create_review_json_str(title="Ryan's better review"))))

    def test_should_return_false_for_json_that_is_not_a_review(self):
        self.assertFalse(app_store_fetcher.Review.is_review(
            json.loads('{'
              '"label":"http://is4.mzstatic.com/image/thumb/Purple49/v4/35/b2/6d/'
                       '35b26d92-82f4-356c-8c7b-2600f0e204b3/mzl.kfiuakmi.png/53x53bb-85.png",'
              '"attributes":{"height":"53"}}')
        ))

    def test_should_return_true_for_json_that_is_a_review(self):
        self.assertTrue(app_store_fetcher.Review.is_review(_create_review_json_str()))

    def test_should_return_author_name(self):
        review = _review()
        self.assertEqual("Awesome he", review.author_name())

    def test_should_return_content(self):
        review = _review()
        self.assertEqual("I love this but it does not have a lot of stuff that in our area on it.",
                         review.content())

    def test_should_return_rating(self):
        review = _review()
        self.assertEqual(5, review.rating())

    def test_should_return_title(self):
        review = _review()
        self.assertEqual("Shop kick", review.title())

    def test_should_return_version(self):
        review = _review()
        self.assertEqual("4.8.1", review.version())


class TestFetchReviews(unittest.TestCase):
    APP_ID = 1234

    def setUp(self):
        super(TestFetchReviews, self).setUp()

        # Create the mock Response object. Each test can override the json.return_value as needed.
        self.response_mock = mock.MagicMock(spec=requests.Response)
        self.response_mock.json.return_value = self._get_feed_json()

        # Setup the requests.get mock.
        self.requests_get_mock = mock.MagicMock(spec=requests.get)
        self.requests_get_mock.return_value = self.response_mock

    def _get_feed_json(self, reviews_json_str=""):
        return json.loads(FEED_TEMPLATE.format(reviews_json_str=reviews_json_str))

    def test_should_create_url_with_app_id_and_page_num(self):
        with mock.patch("requests.get", self.requests_get_mock) as requests_get_mock:
            app_store_fetcher.fetch_reviews(app_id=self.APP_ID, page_num=1)

            requests_get_mock.assert_called_once_with(
                "https://itunes.apple.com/us/rss/customerreviews/page=1/id=1234/sortBy=mostRecent/json",
            )

    def test_should_not_return_any_reviews_if_no_reviews_found(self):
        with mock.patch("requests.get", self.requests_get_mock):
            reviews = app_store_fetcher.fetch_reviews(app_id=self.APP_ID, page_num=1)

            self.assertEqual([], reviews)

    def test_should_return_multiple_reviews(self):
        review_str1 = _create_review_json_str(title="Bo's bad review")
        review_str2 = _create_review_json_str(title="Ryan's better review")
        self.response_mock.json.return_value = self._get_feed_json(
            reviews_json_str=",".join([review_str1, review_str2 + ","]),
        )
        with mock.patch("requests.get", self.requests_get_mock) as requests_get_mock:
            reviews = app_store_fetcher.fetch_reviews(app_id=self.APP_ID, page_num=1)

            self.assertEqual([_review(json_dict=json.loads(review_str1)),
                              _review(json_dict=json.loads(review_str2))],
                             reviews)


if __name__ == "__main__":
    unittest.main()
