#!/usr/bin/env python

import sys

import ocropy


if __name__ == "__main__":
    # TODO: fancy option handling?
    if len(sys.argv) != 2:
        print "usage: hocr.py <img_location>"
        sys.exit(1)

    image_location = sys.argv[1]
    print ocropy.hocr(image_location)
