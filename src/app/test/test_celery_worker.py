import pytest
from app.celery_worker import resize_image_task

@pytest.fixture()
def original_image():
    return {
        'filename': 'image1.jpg', 
        'image_size': '(266, 216)'
        }

@pytest.fixture()
def resized_image_test():
    return {
        'filename': 'image1.jpg', 
        'image_size': '(100, 81)'
        }

def test_resize_image( original_image, resized_image_test):
    resized_image = resize_image_task(original_image)
    result = resized_image
    expected = resized_image_test
    assert result == expected

