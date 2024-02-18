# aes-workshop-3

## .env file

To run the service locally or using docker, first create you `.env` file by running:

```shell
cp .env.example .env
```

## Docker

Make sure you have created the `.env` file as described above. Then, build the image by running:

```shell
docker-compose build
```

Note that you need to build the service everytime you make changes to the code. Then, you can run it with:

```shell
docker-compose up
```
