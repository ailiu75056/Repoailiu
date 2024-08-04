from pyzbar.pyzbar import decode 
from PIL import Image
import requests as r
from io import BytesIO


def get_barcode_from_url(image_url):
    file = r.get(image_url)
    img = Image.open(BytesIO(file.content))
    out = decode(img)
    if len(out) == 0:
        return "No barcode found"
    else:
        return out[0].data.decode("utf-8")
    
print(get_barcode_from_url('https://api.telegram.org/file/bot7356202275:AAGnTYB1q63URoBJ64nzXTPkUp--OB61-h0/photos/file_6.jpg'))