import os

from django.conf import settings
from celery.decorators import task
from celery.utils.log import get_task_logger
from urllib.parse import urlparse

from .utils import remove_in_bucket, get_matching_s3_keys

logger = get_task_logger(__name__)


@task(name="remove_video_files")
def remove_video_files(origin_video_name, poster_thumbnail_uri):
    """ Remove the original video and poster_thumbnail_uri from S3 """
    origin_video_bucket = settings.AWS_STORAGE_BUCKET_NAME

    if origin_video_name is not None:
        remove_in_bucket(bucket=origin_video_bucket, key=origin_video_name)
        logger.info("Removed origin video named {}".format(origin_video_name))

    if poster_thumbnail_uri is not None:

        parsed = urlparse(poster_thumbnail_uri)
        poster_thumbnail_bucket = parsed.netloc
        poster_thumbnail_key = parsed.path.strip('/')

        logger.info("Removing poster frame {}/{}".format(poster_thumbnail_bucket, poster_thumbnail_key))
        remove_in_bucket(bucket=poster_thumbnail_bucket, key=poster_thumbnail_key)


@task(name="remove_stream_files")
def remove_stream_files(stream_uri):
    """ Remove stream related files from S3 """
    parsed = urlparse(stream_uri)

    stream_bucket = parsed.netloc
    stream_key = parsed.path.strip('/')

    filename, file_extension = os.path.splitext(stream_key)

    if file_extension == ".m3u8":
        suffix = ".m3u8"
    elif file_extension == ".mpd":
        suffix = (".mpd", ".cmfv", ".cmfa")
    else:
        suffix = file_extension

    logger.info("Removing files for stream {}/{}".format(stream_bucket, stream_key))

    for key in get_matching_s3_keys(bucket=stream_bucket, prefix=filename, suffix=suffix):
        logger.info("Removing file: {}".format(key))
        remove_in_bucket(bucket=stream_bucket, key=key)
