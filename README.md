# api-resize

FastAPI api used to resize images on request

## Run app:

    $ docker-compose build
	$ docker-compose up -d

## View running application:
View monitoring of celery task:

    $ http://localhost:5556

View running app documentation on swagger endpoint:

    $ http://0.0.0.0:8000/docs

one can also view all the endpoints available here.

## Sample app running:

One can make use of swagger UI created and upload image from the sample images:
    $ visit http://localhost:8000/docs
    
    $ try application by uploading image from app/core/media/sample_images directory

## Running Tests:

With application running in one can run following test command:
    $ docker-compose exec app pytest -v

## Possible improvements:

some things to consider for future features or improvements
- functionality to check if image has already be resized before and stored
- functionality to remove images from api after a given time or on request
- introduce health monitor to check api is functioning well
- introduce logging functionality for api
- introduce feature to get all outstanding celery tasks
- reduce the privileges of the celery worker from super user
- create continuous integration workflows and pipelines

some features that can be implemented to extend current functionality:
- create endpoint for batch upload as well as batch celery task. 
- Can be implemented by uploading list of images and create appropriate celery task

improvements in testing:
    $ could mock out test calls to and from celery work in order to better test endpoints
    $ clean up of directory after testing
    $ edge scenario not tested in size where there might be error in upload

## Architecture design:
this entire application is containerized  with the following architecture
- core api is designed with python FastAPI framework
    - very high performance and on par with Go
    - designed for easy of use
    - based on open standards

- makes use of celery workers for data heavy task:
    - choose celery instead of native fastapi functionality to freeze api resources for other task

- make use of redis messaging queue and results backend:
    - rather simple to implement but has some limitations 
    - could make use of different options in future such as mongodb 

## Scaling considerations:

- given whole application is containerize and can have it running in Kubernetes
- would have Kubernetes spin up containers of api as need be
- Would then introduce a load balancing architecture where traffic would be directed to available container

## Service monitoring:

- would need to introduce adequate logging into the service
- monitor of api with the use of Dynatrace and Kibana
