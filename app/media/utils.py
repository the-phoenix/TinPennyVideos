import logging
import boto3
import json
from botocore.exceptions import ClientError


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
    except ClientError as e:
        logging.error(e)
        return None

    # Return the list of retrieved messages
    return msgs['Messages']


def delete_sqs_message(sqs_queue_url, msg_receipt_handle):
    """Delete a message from an SQS queue

    :param sqs_queue_url: String URL of existing SQS queue
    :param msg_receipt_handle: Receipt handle value of retrieved message
    """

    # Delete the message from the SQS queue
    sqs_client = boto3.client('sqs')
    sqs_client.delete_message(QueueUrl=sqs_queue_url,
                              ReceiptHandle=msg_receipt_handle)


def parse_sqs_message(msg, logger):
    # logging.info(f'SQS: Message ID: {msg["MessageId"]}, '
    #              f'Contents: {msg["Body"]}')

    try:
        mediaConvertResponse = json.loads(msg["Body"])
        detail = mediaConvertResponse["detail"]

        video_duration = None
        output_video_paths = None
        poster_thumbnail = None
        source_path = detail["userMetadata"]["fileInput"]

        for output in detail["outputGroupDetails"]:
            if output["type"] == "CMAF_GROUP":  # Video output
                video_duration = output["outputDetails"][0]["durationInMs"]
                output_video_paths = output["playlistFilePaths"]

            elif output["type"] == "FILE_GROUP":
                poster_thumbnail = output["outputDetails"][0]["outputFilePaths"][0]

    except json.JSONDecodeError as e:
        logger.error(e)
        return None

    return source_path, video_duration, poster_thumbnail, output_video_paths


def is_existing_in_bucket(filename_in_bucket, bucket_name):
    s3 = boto3.client('s3')

    try:
        s3.head_object(Bucket=bucket_name, Key=filename_in_bucket)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        else:
            raise


def remove_in_bucket(filename_in_bucket, bucket_name):
    s3 = boto3.client('s3')

    s3.delete_object(Bucket=bucket_name, Key=filename_in_bucket)


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