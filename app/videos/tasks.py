import json
import os
import os.path

from django.conf import settings
from celery.decorators import task, periodic_task
from celery.utils.log import get_task_logger

from .models import Video
from .utils import delete_sqs_message, retrieve_sqs_messages, parse_sqs_message

logger = get_task_logger(__name__)


@task(name="save_converted_video_urls")
def save_converted_video_urls():
    """Load convert result from SQS and save into database"""

    msgs = retrieve_sqs_messages(settings.AWS_MEDIACONVERT_SQS_URL, 10, 5, 60)
    if msgs is None:
        return

    for msg in msgs:
        parsed = parse_sqs_message(msg, logger)
        if parsed is None:
            continue

        source_url, duration_in_ms, playlist_paths, poster_thumbnail = parsed

        #print("What we have: {}, {}, {}, {}".format(source_url, duration_in_ms,
        #                                            playlist_paths, poster_thumbnail))

        try:
            video = Video.objects.get(source_url=source_url)
        except Video.DoesNotExist:
            logger.info("Video not found for {}".format(source_url))
            return

        video.duration_in_ms = duration_in_ms
        video.poster_thumbnail = poster_thumbnail
        video.mc_status = "SUCCEEDED"
        video.save()

