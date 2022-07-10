from PIL import Image

from app.files import PATH_SAMPLE_IMAGES

def test_ping(test_app):
    response = test_app.get('/ping')

    assert response.status_code == 200
    assert response.json() == "pong"

def test_resize_image(test_app):
    for path in (PATH_SAMPLE_IMAGES).glob("*"):
        try:
            img = Image.open(path)
        except:
            img = None

        response = test_app.post('/resize/image', files= {'file':open(path, 'rb')})

        if img is not None:
            assert response.status_code == 200
            assert path.name in response.json()['message']
            assert response.json()['task_status'] == "Processing"
        else:
            assert response.status_code == 400
            assert response.json()['detail'] == {"error": "Invalid image"}