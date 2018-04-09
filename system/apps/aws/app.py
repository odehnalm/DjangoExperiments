from django.conf import settings

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError


def put_data_to_aws(filename, data):

    # Initialise the S3 client
    s3 = boto3.client(
        's3',
        region_name=settings.AWS_S3_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(s3={'addressing_style': 'path'}))

    s3.put_object(
        ACL='public-read',
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=filename,
        Body=data)


def check_data_on_aws(filename):

    file_exist = True

    # Initialise the S3 client
    s3 = boto3.client(
        's3',
        region_name=settings.AWS_S3_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(s3={'addressing_style': 'path'}))

    try:
        s3.head_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=filename)
    except ClientError:
        file_exist = False

    return file_exist


def get_data_url(filename):

    # Initialise the S3 client
    s3 = boto3.client(
        's3',
        region_name=settings.AWS_S3_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(s3={'addressing_style': 'path'}))

    presigned_url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': filename,
        },
        ExpiresIn=3600
    )

    return presigned_url
