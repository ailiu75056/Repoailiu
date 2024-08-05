from pyzbar.pyzbar import decode 
from PIL import Image
import requests as r
from io import BytesIO


def get_barcode_from_url(image_url):
    file = r.get(image_url)
    img = Image.open(BytesIO(file.content))
    out = decode(img)
    if len(out) == 0:
        return False
    else:
        return out[0].data.decode("utf-8")


