# basic python image
FROM python:3.11-slim

# install pika to access rabbitmq
RUN pip install pika

# Install psycopg2
RUN pip install psycopg2-binary

# declare the source directory
WORKDIR /usr/src/app/write-db

# copy the file
COPY write-db.py .

# start command
CMD [ "python", "write-db.py" ]