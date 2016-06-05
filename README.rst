app-store
=========

The app-store module is a simple Python module for interacting with Apple's public iTunes APIs. At the moment this only
involves fetching recent reviews from the App Store.

Project website: https://github.com/rrueth/app-store

Travis Continuous Integration: https://travis-ci.org/rrueth/app-store

Usage
-----

::

    import app_store.reviews

    app_store.reviews.fetch_reviews(app_id=383298204, page_num=1)

