import sys
import distutils.core

import ocropy

if not ocropy.ocropus_installed:
    print "please install ocropus first: e.g. apt-get install ocropus"
    sys.exit()

distutils.core.setup( 
    name = 'ocropy',
    version = '0.1',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    py_modules = ['ocropy',],
    scripts = ['scripts/hocr.py'],
    description = "extract hOCR from an image path or url",
    platforms = ['POSIX'],
    install_requires = ["pil"],
)
