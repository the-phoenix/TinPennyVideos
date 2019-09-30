from django.core import validators

s3_path_validator = validators.RegexValidator(
    regex='^s3://([^/]+)/(.*?([^/]+)/?)$',
    message='Enter a valid S3 Path',
)