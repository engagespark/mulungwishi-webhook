#!/usr/bin/env python
import unittest

# This line is important so flake8 must ignore this one
from app import views # flake8: noqa
from app import mulungwishi_app


class LaunchingTest(unittest.TestCase):

    def setUp(self):
        self.client = mulungwishi_app.test_client()
        self.client.testing = True

    def test_invalid_url_page_not_found(self):
        result = self.client.get('/page/not/found')
        self.assertEqual(result.status_code, 404)
