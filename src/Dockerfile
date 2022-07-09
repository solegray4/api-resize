FROM python:3
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app/

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /usr/src/app/