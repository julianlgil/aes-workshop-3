# basic python image
FROM python:3.11-slim

# install pika to access rabbitmq
RUN pip install pika

# declare the source directory
WORKDIR /usr/src/app/filter

# copy the file
COPY filter.py .

# start command
CMD [ "python", "filter.py" ]