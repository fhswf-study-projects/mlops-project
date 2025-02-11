import os
import boto3

from app.constants import EnvConfig


class S3Client:
    _instance = None

    def __new__(cls):
        """Returns the singleton instance or creates a new one if not existend"""
        if cls._instance is None:
            cls._instance = super(S3Client, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if os.environ.get(EnvConfig.ENVIRONMENT.value) == "local":
            self.s3_client = boto3.client(
                "s3",
                endpoint_url=os.environ[EnvConfig.S3_ENDPOINT_URL.value],
                aws_access_key_id=os.environ[EnvConfig.S3_ACCESS_KEY_ID.value],
                aws_secret_access_key=os.environ[EnvConfig.S3_SECRET_ACCESS_KEY.value],
            )
        else:
            self.s3_client = boto3.client("s3")

    def create_dir(self, bucket: str, dir_name: str):
        """Create a directory to a S3 bucket

        :param dir_name: directory name without concluding '/'
        :param bucket: Bucket to upload to
        :return: True if directory was created, else False
        """
        self.s3_client.put_object(Bucket=bucket, Key=(dir_name + "/"))