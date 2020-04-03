# TinPennyVideos 

## Description

Youtube like video sharing website. It utilizes AWS services to store/transcode/stream videos.

## How Run

### Development

Uses the default Django development server.

1. Update the environment variables in the *docker-compose.yml* file.
1. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```

    Test it out at [http://localhost:8000](http://localhost:8000). The "app" folder is mounted into the container and your code changes apply automatically.

### Production

Uses gunicorn + nginx.

1. Rename *.env-sample* to *.env* and *.env.db-sample* to *.env.db*. Update the environment variables.
1. Build the images and run the containers:

    ```sh
    $ docker-compose -f docker-compose.prod.yml up -d --build
    ```

    Test it out at [http://localhost:1337](http://localhost:1337). No mounted folders. To apply changes, the image must be re-built.
