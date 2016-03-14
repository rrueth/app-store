import json
import unittest

import app_store_fetcher

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


if __name__ == "__main__":
    unittest.main()