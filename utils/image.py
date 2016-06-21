import hashlib
import requests
from StringIO import StringIO
from PIL import Image
import logging
import zbarlight
from settings import Debug, REDIS_URL
from redis import Redis, from_url



headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36"
           }
image_service_key = "service:news:image:md5"


def download_image(url):
    r = requests.get(url, headers=headers)
    if not r:
        return None
    if r.status_code >= 400:
        # _logger.warn("download image error: %s" % r.status_code)
        print 'download image error: %s' % r.status_code
        return None
    else:
        return r.content


def is_qr_image(fd):
    qrs = list()
    try:
        image = Image.open(fd)
        image.load()
    except IOError as e:
        print e.message
        # _logger.warn("qr %s" % e.message)
    else:
        qrs = zbarlight.scan_codes("qrcode", image)
        if qrs is None:
            return False
    return len(qrs) > 0


def is_ad_image(raw):
    value = hashlib.md5(raw).hexdigest()
    if Debug == True:
        r = Redis()
    else:
        r = from_url(REDIS_URL, max_connections=3)
    return r.sismember(image_service_key, value)


def is_dirty_image(url):
    raw = download_image(url)
    if raw is None:
        return False
    else:
        return is_qr_image(StringIO(raw)) or is_ad_image(raw)