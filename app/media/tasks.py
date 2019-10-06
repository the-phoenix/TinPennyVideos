from django.conf import settings
from celery.decorators import task, periodic_task
from celery.utils.log import get_task_logger
from datetime import timedelta

from .models import Video, Stream
from .utils import delete_sqs_message, retrieve_sqs_messages, parse_sqs_success_message, parse_sqs_failure_message

logger = get_task_logger(__name__)


@periodic_task(name="save_converted_video_urls", run_every=timedelta(minutes=1), ignore_result=True)
def save_converted_video_urls():
    """Load convert result from SQS and save into database"""

    sqs_url = settings.AWS_MEDIACONVERT_SQS_SUCCESS_URL
    msgs = retrieve_sqs_messages(sqs_url, 10, 5, 60)
    if msgs is None:
        return

    for msg in msgs:
        parsed = parse_sqs_success_message(msg, logger)
        if parsed is None:
            continue

        src_key, duration_in_ms, poster_thumbnail, playlist_paths = parsed

        try:
            video = Video.objects.get(origin=src_key)

        except Video.DoesNotExist:
            logger.info("Video not found for {}".format(src_key))
            delete_sqs_message(sqs_url, msg['ReceiptHandle'])
            continue

        for stream_path in playlist_paths:
            Stream.objects.create(path=stream_path, origin=video)

        video.duration_in_ms = duration_in_ms
        video.poster_thumbnail = poster_thumbnail
        video.mc_status = Video.SUCCEEDED
        video.save()

        delete_sqs_message(sqs_url, msg['ReceiptHandle'])
        logger.info("Successfully updated media convert success result for {}".format(src_key))


@periodic_task(name="save_failed_videos", run_every=timedelta(minutes=1), ignore_result=True)
def save_failed_videos():
    """Load convert result from SQS and save into database"""

    sqs_url = settings.AWS_MEDIACONVERT_SQS_FAILURE_URL
    msgs = retrieve_sqs_messages(sqs_url, 10, 5, 60)
    if msgs is None:
        return

    for msg in msgs:
        parsed = parse_sqs_failure_message(msg, logger)
        if parsed is None:
            continue

        src_key, error_msg = parsed

        try:
            video = Video.objects.get(origin=src_key)
        except Video.DoesNotExist:
            logger.info("Video not found for {}".format(src_key))
            delete_sqs_message(sqs_url, msg['ReceiptHandle'])
            continue

        video.failure_reason = error_msg
        video.mc_status = Video.FAILED
        video.save()

        delete_sqs_message(sqs_url, msg['ReceiptHandle'])
        logger.info("Successfully updated media convert failure result for {}".format(src_key))