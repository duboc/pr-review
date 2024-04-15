# python function to create a gcp bucket 
def create_bucket(bucket_name):
  """Creates a new bucket in the US region with the coldline storage
  class"""
  # The ID to give your GCS bucket
  # bucket_name = "your-new-bucket-name"

  from google.cloud import storage

  # The ID of your GCP project
  # project_id = "your-project-id"

  storage_client = storage.Client()

  bucket = storage_client.bucket(bucket_name)
  bucket.storage_class = "COLDLINE"
  new_bucket = storage_client.create_bucket(bucket, location="us")

  print(
      "Created bucket {} in {} with storage class {}".format(
          new_bucket.name, new_bucket.location, new_bucket.storage_class
      )
  )

def list_buckets():
  """Lists all buckets in the project"""   
  from google.cloud import storage

  # The ID of your GCP project
  # project_id = "your-project-id"

  storage_client = storage.Client()

  buckets = storage_client.list_buckets()

  for bucket in buckets:
    print(bucket.name)

def delete_bucket(bucket_name):
  """Deletes a bucket"""
  # The ID to give your GCS bucket
  # bucket_name = "your-bucket-name"

  from google.cloud import storage

  # The ID of your GCP project
  # project_id = "your-project-id"

  storage_client = storage.Client()

  bucket = storage_client.bucket(bucket_name)
  bucket.delete()

  print("Bucket {} deleted".format(bucket.name))
  