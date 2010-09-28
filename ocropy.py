#!/usr/bin/env python

import os
import shutil
import urllib 
import logging
import tempfile
import urlparse
import cStringIO
import subprocess

import Image


def hocr(img_location):
    """returns hOCR for an image
    """
    return hocr_with_image(img_location)[0]


def hocr_with_image(img_location):
    """returns hOCR for an image, and the PIL Image object to 
    save you from re-reading it if you need it for something else
    """
    log = logging.getLogger()
    tmp_dir = tempfile.mkdtemp()

    try:
        log.debug("loading image %s" % img_location)
        img_file = cStringIO.StringIO(_open(img_location).read())
        img = Image.open(img_file)

        # note: ocroscript uses file extension to determine format
        grayscale_filename = os.path.join(tmp_dir, "image." + img.format)
        log.debug("creating grayscale for %s at %s" % (img_location, 
                                                       grayscale_filename))
        img = img.convert("L")
        img.save(grayscale_filename, format=img.format)

        log.debug("generating hocr for %s" % grayscale_filename)
        cmd = ["ocroscript", "recognize", grayscale_filename]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        html = p.communicate()[0]
        html = _replace_tmp_filename(html, grayscale_filename, img_location)
        
        return html, img

    except Exception, e:
        log = logging.error("unable to perform hocr: %s" % e)
        raise HOCRException(e)

    finally:
        shutil.rmtree(tmp_dir)


class HOCRException(Exception):
    pass


def _which(program):
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)
    for path in os.environ["PATH"].split(os.pathsep):
        exe_file = os.path.join(path, program)
        if is_exe(exe_file):
            return exe_file
    return None


def _open(path_or_url):
    """returns a filehandle for a file or url
    """
    log = logging.getLogger()
    try:
        return urllib.urlopen(path_or_url)
    except Exception, e:
        log.error("unable to open %s" % path_or_url)
        return None

def _replace_tmp_filename(html, tmp, orig):
    # <div class="ocr_page" title="bbox 0 0 1786 1169; image /tmp/tmpIjQeAz/image.TIFF">
    return html.replace("image %s" % tmp, "image %s" % orig)


ocropus_installed = True if _which("ocroscript") else False
