import unittest
from unittest.mock import MagicMock
from prometheus_sanic.endpoint import fn_by_type, get_from_url


def mk_request(url):
    req = MagicMock()
    req.path = url
    return req


def az_url():
    return "/".join('abcdefghijklmnopqrstuvwxyz')


class TestUrlEndpoint(unittest.TestCase):
    def test_just_url(self):
        fn = fn_by_type('url', None)
        url = '/check/this/url'
        self.assertEqual(fn(mk_request(url)), url)

    def test_url_with_limit(self):
        fn = fn_by_type('url:3', None)
        self.assertEqual(fn(mk_request('/check/this/awesome/url')),
                         '/check/this/awesome')
        self.assertEqual(fn(mk_request('/check/this')), '/check/this')

    def test_url_bad_limit(self):
        self.assertRaises(ValueError, fn_by_type, 'url:lakdh', None)

    def test_get_endpoint_fn_argument_is_ignored(self):
        should_be_ignored = lambda x: x
        self.assertNotEqual(fn_by_type('url', should_be_ignored),
                            should_be_ignored)


class TestGetFromUrl(unittest.TestCase):
    def test_no_limit_set_by_default(self):
        test_url = az_url()
        self.assertEqual(get_from_url(mk_request(test_url)), test_url)

    def test_zero_or_negative_limit_eq_default_behaviour(self):
        test_url = az_url()
        self.assertEqual(get_from_url(mk_request(test_url), lim=0), test_url)

    def test_lim_works_as_expected(self):
        self.assertEqual(get_from_url(mk_request('/a'), lim=1), '/a')
        self.assertEqual(get_from_url(mk_request('/a/b/c'), lim=1), '/a')
        self.assertEqual(get_from_url(mk_request('/a'), lim=2), '/a')
        self.assertEqual(get_from_url(mk_request('/a/'), lim=1), '/a')
