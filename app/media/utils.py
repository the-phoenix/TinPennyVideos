import logging
import boto3
import json
import os

from urllib.parse import urlparse
from botocore.exceptions import ClientError
from uuid import uuid4


def retrieve_sqs_messages(sqs_queue_url, num_msgs=1, wait_time=0, visibility_time=5):
    """Retrieve messages from an SQS queue

    The retrieved messages are not deleted from the queue.

    :param sqs_queue_url: String URL of existing SQS queue
    :param num_msgs: Number of messages to retrieve (1-10)
    :param wait_time: Number of seconds to wait if no messages in queue
    :param visibility_time: Number of seconds to make retrieved messages
        hidden from subsequent retrieval requests
    :return: List of retrieved messages. If no messages are available, returned
        list is empty. If error, returns None.
    """

    # Validate number of messages to retrieve
    if num_msgs < 1:
        num_msgs = 1
    elif num_msgs > 10:
        num_msgs = 10

    # Retrieve messages from an SQS queue
    sqs_client = boto3.client('sqs')
    try:
        msgs = sqs_client.receive_message(QueueUrl=sqs_queue_url,
                                          MaxNumberOfMessages=num_msgs,
                                          WaitTimeSeconds=wait_time,
                                          VisibilityTimeout=visibility_time)

        # Return the list of retrieved messages
        return msgs['Messages']
    except ClientError as e:
        logging.error(e)
        return None
    except KeyError:
        return []


def delete_sqs_message(sqs_queue_url, msg_receipt_handle):
    """Delete a message from an SQS queue

    :param sqs_queue_url: String URL of existing SQS queue
    :param msg_receipt_handle: Receipt handle value of retrieved message
    """

    # Delete the message from the SQS queue
    sqs_client = boto3.client('sqs')
    try:
        sqs_client.delete_message(QueueUrl=sqs_queue_url,
                                  ReceiptHandle=msg_receipt_handle)
    except ClientError as e:
        logging.error(e)


def parse_sqs_message(msg, logger):
    # logging.info(f'SQS: Message ID: {msg["MessageId"]}, '
    #              f'Contents: {msg["Body"]}')

    try:
        mediaConvertResponse = json.loads(msg["Body"])
        detail = mediaConvertResponse["detail"]

        video_duration = None
        output_video_paths = None
        poster_thumbnail = None
        src_key = detail["userMetadata"]["srcKey"]

        for output in detail["outputGroupDetails"]:
            if output["type"] == "CMAF_GROUP":  # Video output
                video_duration = output["outputDetails"][0]["durationInMs"]
                output_video_paths = output["playlistFilePaths"]

            elif output["type"] == "FILE_GROUP":
                poster_thumbnail = output["outputDetails"][0]["outputFilePaths"][0]

    except json.JSONDecodeError as e:
        logger.error(e)
        return None

    return src_key, video_duration, poster_thumbnail, output_video_paths


def is_existing_in_bucket(bucket, key):
    s3 = boto3.client('s3')

    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        else:
            raise


def remove_in_bucket(bucket, key):
    s3 = boto3.client('s3')

    try:
        s3.delete_object(Bucket=bucket, Key=key)
        return True
    except ClientError:
        return False


def get_matching_s3_objects(bucket, prefix="", suffix=""):
    """
    Generate objects in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch objects whose key starts with
        this prefix (optional).
    :param suffix: Only fetch objects whose keys end with
        this suffix (optional).
    """
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")

    kwargs = {'Bucket': bucket}

    # We can pass the prefix directly to the S3 API.  If the user has passed
    # a tuple or list of prefixes, we go through them one by one.
    if isinstance(prefix, str):
        prefixes = (prefix, )
    else:
        prefixes = prefix

    for key_prefix in prefixes:
        kwargs["Prefix"] = key_prefix

        for page in paginator.paginate(**kwargs):
            try:
                contents = page["Contents"]
            except KeyError:
                return

            for obj in contents:
                key = obj["Key"]
                if key.endswith(suffix):
                    yield obj


def get_matching_s3_keys(bucket, prefix="", suffix=""):
    """
    Generate the keys in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """
    for obj in get_matching_s3_objects(bucket, prefix, suffix):
        yield obj["Key"]


def td_format(td_object):
    seconds = int(td_object.total_seconds())
    periods = [
        ('year',        60*60*24*365),
        ('month',       60*60*24*30),
        ('day',         60*60*24),
        ('hour',        60*60),
        ('min',      60),
        ('sec',      1)
    ]

    strings=[]
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value , seconds = divmod(seconds, period_seconds)
            has_s = 's' if period_value > 1 else ''
            strings.append("%s %s%s" % (period_value, period_name, has_s))

    return " ".join(strings)


def path_and_rename(instance, filename):
    upload_to = instance.category.name.lower() if instance.category is not None else 'default'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4(), ext)

    return os.path.join(upload_to, filename)