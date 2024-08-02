from google.cloud import storage

def create_bucket(project_id, bucket_name):
  """Creates a new bucket in the project"""

  # Create a client.
  storage_client = storage.Client()

  # Create a new bucket.
  bucket = storage_client.create_bucket(bucket_name, project=project_id)

  print(f"Created bucket {bucket.name} in project {project_id}.")

  return bucket

def list_buckets(project_id):
  """Lists all buckets in the project"""

  # Create a client.
  storage_client = storage.Client()

  # List all buckets.
  buckets = storage_client.list_buckets(project=project_id)

  for bucket in buckets:
    print(f"Bucket: {bucket.name}")

def delete_bucket(project_id, bucket_name):
  """Deletes a bucket in the project"""

  # Create a client.
  storage_client = storage.Client()

  # Delete the bucket.
  bucket = storage_client.bucket(bucket_name)
  bucket.delete(force=True)

  print(f"Deleted bucket {bucket_name} in project {project_id}.")
