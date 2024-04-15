# create a python function to create a gcp bucket

from google.cloud import storage 

def create_bucket(bucket_name):
  """Creates a new bucket in the US region with the coldline storage
  class"""
  # bucket_name = "your-new-bucket-name"

  storage_client = storage.Client()

  bucket = storage_client.bucket(bucket_name)
  bucket.location = "US"
  bucket.storage_class = "COLDLINE"

  bucket.create()

  print(f"Bucket {bucket.name} created.")


def list_buckets():
  """Lists all buckets in the project"""
  storage_client = storage.Client()

  buckets = storage_client.list_buckets()

  for bucket in buckets:
    print(bucket.name)

def delete_bucket(bucket_name):
  """Deletes a bucket"""
  # bucket_name = "your-bucket-name"

  storage_client = storage.Client()

  bucket = storage_client.bucket(bucket_name)
  bucket.delete()

  print(f"Bucket {bucket.name} deleted.")

if __name__ == "__main__":
  create_bucket("my-new-bucket")


