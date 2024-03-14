import google.cloud.storage


# Function to create blob
def create_blob_root_container(self, blob_service_client: BlobServiceClient):
    container_client = blob_service_client.get_container_client(container="$root")

    # Create the root container if it doesn't already exist
    if not container_client.exists():
        container_client.create_container()

# Function to upload a file to GCS

import google.cloud.storage


# Function to create a GCS   

def create_bucket(bucket_name):
    """Creates a new bucket."""
    # bucket_name = "your-new-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.create_bucket(bucket_name)

    print(f"Bucket {bucket.name} created")

    return bucket  


# Function to upload a file to GCS

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Optional: set a generation-match precondition to avoid potential race
    # conditions and data corruptions. The request to upload is aborted if the
    # object's generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0

    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

    return blob  

# generate python function to list buckets   
def list_buckets():
    """Lists all buckets."""
    storage_client = storage.Client()

    # Note: Client.list_buckets requires at least package version 1.17.0.
    buckets = list(storage_client.list_buckets())

    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)

    return buckets  


# generate python function to delete a bucket   

def delete_bucket(bucket_name):
    """Deletes a bucket. The bucket must be empty."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    bucket.delete()

    print(f"Bucket {bucket.name} deleted")

    return bucket  

 