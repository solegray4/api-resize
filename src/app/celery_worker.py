import os
import time
from PIL import Image

from celery import Celery
from dotenv import load_dotenv

from app.core.files import PATH_FILES_ORIGINAL, PATH_FILES_RESIZED

celery = Celery(__name__, backend='redis://redis:6379/0', broker='redis://redis:6379/0')
celery.conf.update(
   result_extended=True
)

@celery.task(name="resize_image_task")
def resize_image_task(filename):
    size = {
        "width": 100,
        "height": 100
        }
    size_defined = size['width'], size['height']
    img = Image.open(f"{PATH_FILES_ORIGINAL}{filename}", mode="r")
    img.thumbnail(size_defined)
    img.save(PATH_FILES_RESIZED + filename)
    return  {'filename': filename, "image_size": str(img.size)}