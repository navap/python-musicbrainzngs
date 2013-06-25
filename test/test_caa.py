import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import StringIO

from musicbrainzngs import caa
from musicbrainzngs import compat
import musicbrainzngs
from test import _common

class CaaTest(unittest.TestCase):

    def test_get_list(self):
        # check the url and response for a listing
        resp = '{"images":[]}'
        self.opener = _common.FakeOpener(resp)
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        res = caa.get_coverart_list("8ec178f4-a8e8-4f22-bcba-1964466ef214")
        self.assertEqual("http://coverartarchive.org/release/8ec178f4-a8e8-4f22-bcba-1964466ef214", self.opener.myurl)
        self.assertEqual(1, len(res))
        self.assertTrue("images" in res)

    def test_list_none(self):
        """ When CAA gives a 404 error, return None"""
        
        # urllib2.HTTPError(self, url, code, msg, hdrs, fp)
        exc = compat.HTTPError("", 404, "", "", StringIO.StringIO(""))
        self.opener = _common.FakeOpener(exception=musicbrainzngs.ResponseError(cause=exc))
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        res = caa.get_coverart_list("8ec178f4-a8e8-4f22-bcba-1964466ef214")
        self.assertEqual(None, res)

    def test_list_baduuid(self):
        # urllib2.HTTPError(self, url, code, msg, hdrs, fp)
        exc = compat.HTTPError("", 400, "", "", StringIO.StringIO(""))
        self.opener = _common.FakeOpener(exception=musicbrainzngs.ResponseError(cause=exc))
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        try:
            res = caa.get_coverart_list("8ec178f4-a8e8-4f22-bcba-19644XXXXXX")
            self.assertTrue(False, "Expected an exception")
        except musicbrainzngs.ResponseError as e:
            self.assertEqual(e.cause.code, 400)

    def test_set_useragent(self):
        """ When a useragent is set it is sent with the request """
        musicbrainzngs.set_useragent("caa-test", "0.1")

        resp = '{"images":[]}'
        self.opener = _common.FakeOpener(resp)
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        res = caa.get_coverart_list("8ec178f4-a8e8-4f22-bcba-1964466ef214")

        headers = dict(self.opener.headers)
        self.assertTrue("User-agent" in headers)
        self.assertEqual("caa-test/0.1 python-musicbrainz-ngs/0.5dev", headers["User-agent"])

    def test_coverid(self):
        resp = 'some_coverart'
        self.opener = _common.FakeOpener(resp)
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        res = caa.download_coverart("8ec178f4-a8e8-4f22-bcba-1964466ef214", "1234")

        self.assertEqual("http://coverartarchive.org/release/8ec178f4-a8e8-4f22-bcba-1964466ef214/1234", self.opener.myurl)
        self.assertEqual(resp, res)

    def test_get_size(self):
        resp = 'some_coverart'
        self.opener = _common.FakeOpener(resp)
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        res = caa.download_coverart("8ec178f4-a8e8-4f22-bcba-1964466ef214", "1234", 250)

        self.assertEqual("http://coverartarchive.org/release/8ec178f4-a8e8-4f22-bcba-1964466ef214/1234-250", self.opener.myurl)
        self.assertEqual(resp, res)

    def test_front(self):
        resp = 'front_coverart'
        self.opener = _common.FakeOpener(resp)
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        res = caa.download_coverart_front("8ec178f4-a8e8-4f22-bcba-1964466ef214")

        self.assertEqual("http://coverartarchive.org/release/8ec178f4-a8e8-4f22-bcba-1964466ef214/front", self.opener.myurl)
        self.assertEqual(resp, res)

    def test_back(self):
        resp = 'back_coverart'
        self.opener = _common.FakeOpener(resp)
        musicbrainzngs.compat.build_opener = lambda *args: self.opener
        res = caa.download_coverart_back("8ec178f4-a8e8-4f22-bcba-1964466ef214")

        self.assertEqual("http://coverartarchive.org/release/8ec178f4-a8e8-4f22-bcba-1964466ef214/back", self.opener.myurl)
        self.assertEqual(resp, res)
