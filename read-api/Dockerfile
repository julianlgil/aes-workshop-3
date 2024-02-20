# basic python image
FROM python:3.11-slim

# install pika to access rabbitmq
RUN pip install pika

# install pika to access spotify
RUN pip install spotipy

# declare the source directory
WORKDIR /usr/src/app/read-api

# copy the file
COPY read-api.py .

# start command
CMD [ "python", "read-api.py" ]