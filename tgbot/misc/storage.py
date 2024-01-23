import boto3


class Storage:
    def __init__(self, access_id: str, access_key: str):
        self.s3 = boto3.resource(
            service_name="s3",
            region_name="eu-central-1",
            aws_access_key_id=access_id,
            aws_secret_access_key=access_key,
        )
        self.set_bucket("studyhelper")

    def print_buckets(self):
        for bucket in self.s3.buckets.all():
            print(bucket.name)

    def set_bucket(self, bucket_name):
        self.bucket = self.s3.Bucket(bucket_name)

    def get_bucket(self):
        return self.bucket

    def print_objects(self):
        for obj in self.bucket.objects.all():
            print(obj)

    def add_file(self, file_name):
        print(self.bucket.upload_file(file_name, file_name))

    def download_file(self, file_name):
        self.bucket.download_file(file_name, file_name)
