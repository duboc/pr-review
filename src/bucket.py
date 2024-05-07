## generate a python function to create a gcs bucket

from google.cloud import storage

def create_bucket(bucket_name):
    """Creates a new bucket in the US region with the coldline storage
    class"""
    # bucket_name = "your-new-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "COLDLINE"
    new_bucket = storage_client.create_bucket(bucket, location="us")

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )

create_bucket("my-new-bucket")

def list_buckets():
    """Lists all buckets in the project"""
    storage_client = storage.Client()

    buckets = storage_client.list_buckets()

    for bucket in buckets:
        print(bucket.name)

list_buckets()

def delete_bucket(bucketName):
    """Deletes a bucket"""
    # bucketName = "your-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucketName)
    bucket.delete()

    print("Bucket {} deleted".format(bucket.name))
