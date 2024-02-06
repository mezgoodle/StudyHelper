import logging

import boto3
from botocore.exceptions import NoCredentialsError


class Storage:
    def __init__(self, access_id: str, access_key: str):
        try:
            self.s3 = boto3.resource(
                service_name="s3",
                region_name="eu-central-1",
                aws_access_key_id=access_id,
                aws_secret_access_key=access_key,
            )
            self.set_bucket("studyhelper")
        except NoCredentialsError:
            logging.error("Credentials not found")

    def print_buckets(self):
        try:
            for bucket in self.s3.buckets.all():
                print(bucket.name)
        except Exception as e:
            logging.error(f"Error while listing buckets: {e}")

    def set_bucket(self, bucket_name):
        try:
            self.bucket = self.s3.Bucket(bucket_name)
        except Exception as e:
            logging.error(f"Error while setting bucket: {e}")

    def get_bucket(self):
        return self.bucket

    def print_objects(self):
        try:
            for obj in self.bucket.objects.all():
                print(obj.key)
        except Exception as e:
            logging.error(f"Error while listing objects: {e}")

    def add_file(self, file_name: str, name: str) -> bool:
        try:
            self.bucket.upload_file(file_name, name)
            logging.info(
                f"File '{file_name}' successfully uploaded as '{name}'"
            )
            return True
        except Exception as e:
            logging.error(f"Error while uploading file: {e}")
            return False

    def download_file(self, file_name) -> bool:
        try:
            self.bucket.download_file(file_name, file_name)
            logging.info(f"File '{file_name}' successfully downloaded")
            return True
        except Exception as e:
            logging.error(f"Error while downloading file: {e}")
            return False
