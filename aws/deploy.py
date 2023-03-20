import os
import zipfile
from uuid import uuid4

import boto3

aws_elasticbeanstalk_service_role = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "elasticbeanstalk.amazonaws.com"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": "elasticbeanstalk"
                }
            }
        }
    ]
}


def create_zip():
    exclude_file = ['.elasticbeanstalk', '.git', '.idea', 'aws', 'venv']
    with zipfile.ZipFile("output.zip", "w") as zip_file:
        for file in os.listdir():
            if file in exclude_file:
                continue
            zip_file.write(file, compress_type=zipfile.ZIP_DEFLATED)


def upload_bucket(bucket_name: str, version: str):
    client = boto3.client('s3')
    resp = client.upload_file('output.zip', bucket_name, f'app/{version}-app.zip')
    print(resp)


def create_storage_location():
    client = boto3.client('elasticbeanstalk')
    resp = client.create_storage_location()
    return resp['S3Bucket']


def if_exist_delete():
    if os.path.exists('output.zip'):
        os.remove('output.zip')


def create_eb(app_name: str):
    client = boto3.client('elasticbeanstalk')
    response = client.create_application(
        ApplicationName=app_name,
        ResourceLifecycleConfig={
            'ServiceRole': 'string',
            'VersionLifecycleConfig': {
                'MaxCountRule': {
                    'Enabled': True | False,
                    'MaxCount': 123,
                    'DeleteSourceFromS3': True | False
                },
                'MaxAgeRule': {
                    'Enabled': True | False,
                    'MaxAgeInDays': 123,
                    'DeleteSourceFromS3': True | False
                }
            }
        },
        Tags=[
            {
                'Key': 'string',
                'Value': 'string'
            },
        ]
    )


if __name__ == '__main__':
    try:
        create_zip()
        bucket = create_storage_location()
        upload_bucket(str(uuid4()), bucket)
    finally:
        if_exist_delete()
