#!/usr/bin/env python

import re
import unittest

import ocropy

class OcropyTests(unittest.TestCase):

    def test_tif(self):
        html = ocropy.hocr("test-data/0001.tif")
        expected = open("test-data/0001.html").read()
        self.assertEqual(html, expected)

if __name__ == '__main__':
    unittest.main()
