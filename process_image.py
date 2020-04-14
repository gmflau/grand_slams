import sys
from PIL import Image

def resize_image(filename):
    image = Image.open(filename)
    image = image.resize((image_size, image_size), Image.ANTIALIAS)
    image.save(filename)

resize_image(sys.argv[1])
